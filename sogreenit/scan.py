# -*- coding: utf-8 -*-

from datetime import date
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from jsonschema import ValidationError, validate
from browsermobproxy import Server
from flask import request, jsonify

from sogreenit.db.connection import DBConnection
from sogreenit.tests import tests, ecoindex
from sogreenit import app, input_schema

# Starting BrowserMob Proxy server
browsermob_server = None
browsermob_proxy = None

if os.name == 'nt':
    browsermob_server = Server(
        '{}\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat'.format(os.getcwd())
    )
else:
    browsermob_server = Server(
        '{}/browsermob-proxy-2.1.4/bin/browsermob-proxy'.format(os.getcwd())
    )

browsermob_server.start()
browsermob_proxy = browsermob_server.create_proxy()

# Setting browser profile
browser_profile = webdriver.FirefoxProfile()
browser_profile.set_preference('app.update.enabled', False)
browser_profile.set_preference('browser.cache.disk.enable', False)
browser_profile.set_preference('browser.cache.disk.free_space_hard_limit', False)
browser_profile.set_preference('browser.cache.disk.free_space_soft_limit', False)
browser_profile.set_preference('browser.cache.disk.max_chunks_memory_usage', False)
browser_profile.set_preference('browser.cache.disk.max_entry_size', False)
browser_profile.set_preference('browser.cache.disk.max_priority_chunks_memory_usage', False)
browser_profile.set_preference('browser.cache.disk.metadata_memory_limit', False)
browser_profile.set_preference('browser.cache.disk.preload_chunk_count', False)
browser_profile.set_preference('browser.cache.disk.smart_size.enabled', False)
browser_profile.set_preference('browser.cache.disk.smart_size.first_run', False)
browser_profile.set_preference('browser.cache.disk.smart_size_cached_value', False)
browser_profile.set_preference('browser.cache.disk.smart_size.use_old_max', False)
browser_profile.set_preference('browser.cache.disk_cache_ssl', False)
browser_profile.set_preference('browser.cache.memory.enable', False)
browser_profile.set_preference('browser.cache.memory.max_entry_size', False)
browser_profile.set_preference('browser.cache.offline.enable', False)
browser_profile.set_preference('browser.cache.use_new_backend', False)
browser_profile.set_preference('browser.cache.use_new_backend_temp', False)
browser_profile.set_preference('dom.caches.enabled', False)
browser_profile.set_preference('dom.requestcache.enabled', False)
browser_profile.set_preference('image.cache.size', False)
browser_profile.set_preference('media.cache_size', False)
browser_profile.set_proxy(browsermob_proxy.selenium_proxy())

# DB connection
db = DBConnection()

@app.route('/scan', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def scan_help():
    """
    Return an little help about this namespace
    """
    return jsonify(
        help={
            '/scan/static': {
                'method': 'POST',
                'body': 'Your scanning parameters in JSON (go see ...)',
                'description': 'Launch a eco-scan of one webpage only specified by the input URL'
            },
            '/scan/app': {
                'method': 'POST',
                'body': 'Your scanning parameters in JSON (go see ...)',
                'description': 'Launch an eco-scan of a web application specified by the input URL'
            }
        }
    )

@app.route('/scan/static', methods=['POST'])
def scan_static():
    """
    Launch a static scan of one web page
    """

    # Retrieving user parameters
    user_params = request.get_json()

    try:
        validate(user_params, input_schema)
    except ValidationError as err:
        raise err

    # Instantiating browser
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities={
            # Subject to change: modern web application trends to use those functionalities
            'applicationCacheEnabled': False,
            'webStorageEnabled': False,
            'databaseEnabled': False
        },
        browser_profile=browser_profile
    )

    # Loading input URL
    browsermob_proxy.new_har(title=user_params['url'])
    driver.get(user_params['url'])
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    except TimeoutException as err:
        raise err
    
    # Retrieving HAR content
    har = browsermob_proxy.har

    # Retrieving DOM from the page
    dom = driver.find_element_by_tag_name('html')

    # Retrieving CPU informations
    cpu = None # TODO

    # Retrieving memory informations
    mem = None # TODO

    # Computing Ecoindex grade
    grade = ecoindex.run(har=har, dom=dom, cpu=cpu, mem=mem)

    # Setting up rules testing environment
    rules_set = None
    excluded_rules = None
    results = {}

    # Retrieving used rules
    try:
        if type(user_params['includeRules']) is list and len(user_params['includeRules']) > 0:
            rules_set = user_params['includeRules']
        else:
            rules_set = range(len(tests))
    except KeyError:
        rules_set = range(len(tests))

    # Retrieving excluded rules
    try:
        excluded_rules = user_params['excludeRules']
    except KeyError:
        excluded_rules = []

    # Computing tests
    for rule_id in rules_set:
        if rule_id not in excluded_rules:
            results[rule_id] = tests[rule_id].run(har, dom, cpu, mem)

    # Closing browser
    driver.quit()

    # Retrieving the project ID from the user parameters
    project_id = None
    try:
        project_id = user_params['project']
    except KeyError:
        # If the project ID is not specified, we'll create a new one
        db.make_request("""INSERT INTO projects (name) VALUES (%s)""", (user_params['url']))
        project_id = db.make_request("""SELECT MAX(id) FROM projects WHERE name = %s""", (user_params['url']))[0]

    # Now adding a new entry to the results in the database
    db.make_request(
        """INSERT INTO projects_results (date, project_id)
        VALUES (%s, %s)""",
        (
            date.today(),
            project_id
        )
    )
    results_id = db.make_request(
        """SELECT MAX(id)
        FROM projects_results
        WHERE project_id = %s""",
        (
            project_id
        )
    )[0]

    # Registering the results of the page
    db.make_request(
        """INSERT INTO pages_results (date, url, ecoindex, projects_results_id)
        VALUES (%s, %s, %s, %s)""",
        (
            date.today(),
            user_params['url'],
            grade,
            results_id
        )
    )
    page_id = db.make_request(
        """SELECT MAX(id)
        FROM pages_results
        WHERE projects_results_id = %s""",
        (
            results_id
        )
    )[0]

    for test_id in results:
        db.make_request(
            """INSERT INTO steps_results (result, bp_id, pages_results_id)
            VALUES (%s, %s, %s)""",
            (
                results[test_id],
                test_id,
                page_id
            )
        )

    # Returning the result of the scan
    return jsonify({
        'project': project_id,
        'url': user_params['url'],
        'ecoindex': grade,
        'results': results
    })

@app.route('/scan/app', methods=['POST'])
def scan_app():
    """
    Launch a global scan of a web page
    """
    pass
