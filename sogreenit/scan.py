# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from jsonschema import ValidationError, validate
from browsermobproxy import Server
from flask import request, jsonify

from sogreenit.db.manager import DBConnection
from sogreenit.tests import tests, ecoindex
from sogreenit import app, input_schema

# Starting BrowserMob Proxy server
browsermob_server = None
browsermob_proxy = None

if os.name == 'nt':
    browsermob_server = Server('{}\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat'.format(os.getcwd()))
else:
    browsermob_server = Server('{}\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy'.format(os.getcwd()))

browsermob_server.start()
browsermob_proxy = browsermob_server.create_proxy()

# Setting browser profile
profile = webdriver.FirefoxProfile()
profile.set_preference('app.update.enabled', False)
profile.set_preference('browser.cache.disk.enable', False)
profile.set_preference('browser.cache.disk.free_space_hard_limit', False)
profile.set_preference('browser.cache.disk.free_space_soft_limit', False)
profile.set_preference('browser.cache.disk.max_chunks_memory_usage', False)
profile.set_preference('browser.cache.disk.max_entry_size', False)
profile.set_preference('browser.cache.disk.max_priority_chunks_memory_usage', False)
profile.set_preference('browser.cache.disk.metadata_memory_limit', False)
profile.set_preference('browser.cache.disk.preload_chunk_count', False)
profile.set_preference('browser.cache.disk.smart_size.enabled', False)
profile.set_preference('browser.cache.disk.smart_size.first_run', False)
profile.set_preference('browser.cache.disk.smart_size_cached_value', False)
profile.set_preference('browser.cache.disk.smart_size.use_old_max', False)
profile.set_preference('browser.cache.disk_cache_ssl', False)
profile.set_preference('browser.cache.memory.enable', False)
profile.set_preference('browser.cache.memory.max_entry_size', False)
profile.set_preference('browser.cache.offline.enable', False)
profile.set_preference('browser.cache.use_new_backend', False)
profile.set_preference('browser.cache.use_new_backend_temp', False)
profile.set_preference('dom.caches.enabled', False)
profile.set_preference('dom.requestcache.enabled', False)
profile.set_preference('image.cache.size', False)
profile.set_preference('media.cache_size', False)
profile.set_proxy(browsermob_proxy.selenium_proxy())

# DB connection
# db = DBConnection(host=os.getenv('SOGREEN_DB_HOST'))

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
            'applicationCacheEnabled': False, # Subject to change: modern web application trends to use those functionalities
            'webStorageEnabled': False,
            'databaseEnabled': False
        },
        browser_profile=profile
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
        if rule_id not in user_params['excludeRules']:
            results[rule_id] = tests[rule_id].run(har, dom, cpu, mem)

    # Closing browser
    driver.quit()

    # Returning the result of the scan
    return jsonify({
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
