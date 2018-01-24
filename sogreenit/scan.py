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
from flask import request, jsonify

from sogreenit.db.manager import DBConnection
from sogreenit.tests import tests, ecoindex
from sogreenit import app, input_schema

# Setting constant for loggin directory
HAR_LOG_DIR = None
if os.name == 'nt':
    HAR_LOG_DIR = '{}\\logs'.format(os.getcwd())
else:
    HAR_LOG_DIR = '{}/logs'.format(os.getcwd())

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
profile.set_preference('devtools.netmonitor.har.defaultLogDir', HAR_LOG_DIR)
profile.set_preference('devtools.netmonitor.har.enableAutoExportToFile', True)
profile.set_preference('devtools.netmonitor.har.forceExport', True)
profile.set_preference('dom.caches.enabled', False)
profile.set_preference('dom.requestcache.enabled', False)
profile.set_preference('image.cache.size', False)
profile.set_preference('media.cache_size', False)

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
    profile.set_preference('devtools.netmonitor.har.defaultFileName', '{}.archive'.format(user_params['url']))
    
    browser = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities={
            'applicationCacheEnabled': False, # Subject to change: modern web application trends to use those functionalities
            'webStorageEnabled': False,
            'databaseEnabled': False
        },
        browser_profile=profile
    )
    ActionChains(browser).key_down(Keys.F12).key_up(Keys.F12).perform()

    # Loading input URL
    try:
        browser.get(user_params['url'])
        WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    except TimeoutException as err:
        raise err
    
    # Closing browser
    browser.quit()

    # Opening HAR archive and parsing it
    d = datetime.now()
    path = None
    har = None

    if os.name == 'nt':
        path = '{}\\{}.archive.har'.format(HAR_LOG_DIR, user_params['url'])
    else:
        path = '{}/{}.archive.har'.format(HAR_LOG_DIR, user_params['url'])

    with open(path) as f:
        har = json.load(f)

    # Retrieving DOM from the page
    dom = browser.find_element_by_tag_name('html')

    # Retrieving CPU informations
    cpu = None # TODO

    # Retrieving memory informations
    mem = None # TODO

    # Computing Ecoindex grade
    grade = ecoindex.run(har, dom, cpu, mem)

    # Computing tests
    rules_set = None
    results = {}

    if user_params['includeRules'] == []:
        rules_set = range(len(tests))
    else:
        rules_set = user_params['includeRules']

    for rule_id in rules_set:
        if rule_id not in user_params['excludeRules']:
            results[rule_id] = tests[rule_id].run(har, dom, cpu, mem)

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
