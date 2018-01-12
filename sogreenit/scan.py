# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from flask import request, jsonify
from jsonschema import ValidationError, validate

from sogreenit.db.manager import DBConnection
from sogreenit.tests import tests, ecoindex
from sogreenit import app, input_schema

# Setting browser profile
profile = webdriver.FirefoxProfile()
profile.set_preference('app.update.enabled', 0)
profile.set_preference('browser.cache.disk.enable', 0)
profile.set_preference('browser.cache.disk.free_space_hard_limit', 0)
profile.set_preference('browser.cache.disk.free_space_soft_limit', 0)
profile.set_preference('browser.cache.disk.max_chunks_memory_usage', 0)
profile.set_preference('browser.cache.disk.max_entry_size', 0)
profile.set_preference('browser.cache.disk.max_priority_chunks_memory_usage', 0)
profile.set_preference('browser.cache.disk.metadata_memory_limit', 0)
profile.set_preference('browser.cache.disk.preload_chunk_count', 0)
profile.set_preference('browser.cache.disk.smart_size.enabled', 0)
profile.set_preference('browser.cache.disk.smart_size.first_run', 0)
profile.set_preference('browser.cache.disk.smart_size_cached_value', 0)
profile.set_preference('browser.cache.disk.smart_size.use_old_max', 0)
profile.set_preference('browser.cache.disk_cache_ssl', 0)
profile.set_preference('browser.cache.memory.enable', 0)
profile.set_preference('browser.cache.memory.max_entry_size', 0)
profile.set_preference('browser.cache.offline.enable', 0)
profile.set_preference('browser.cache.use_new_backend', 0)
profile.set_preference('browser.cache.use_new_backend_temp', 0)
profile.set_preference('devtools.netmonitor.har.defaultLogDir', '/var/sogreenit/har')
profile.set_preference('devtools.netmonitor.har.enableAutoExportToFile', 1)
profile.set_preference('devtools.netmonitor.har.forceExport', 1)
profile.set_preference('dom.caches.enabled', 0)
profile.set_preference('dom.requestcache.enabled', 0)
profile.set_preference('image.cache.size', 0)
profile.set_preference('media.cache_size', 0)

# Instantiate browser into memory
browser = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities={
        'applicationCacheEnabled': False,
        'webStorageEnabled': False,
        'databaseEnabled': False
    },
    browser_profile=profile
)
browser.implicitly_wait(2)
browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + 'K')

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

    # Loading input URL
    browser.get(user_params['url'])

    # Opening HAR archive and parsing it
    d = datetime.today()
    har = None
    with open('/var/sogreenit/har/Archive {}'.format(d.strftime('%Y-%M-d %I-%m-%S'))) as f:
        har = json.load(f)

    # Retrieving DOM from the page
    dom = browser.find_element_by_tag_name('html')

    # Retrieving CPU informations
    cpu = None # TODO

    # Retrieving memory informations
    mem = None

    # Computing Ecoindex grade
    grade = ecoindex.run(har, dom, cpu, mem)

    # Returning the result of the scan
    return jsonify({
        'url': user_params['url'],
        'ecoindex': grade
    })

@app.route('/scan/app', methods=['POST'])
def scan_app():
    """
    Launch a global scan of a web page
    """
    pass
