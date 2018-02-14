# -*- coding: utf-8 -*-
# pylint: skip-file

from sogreenit.db.connection import DBConnection
from flask import Flask
import json
import os

VERSION_MAJOR = 0
VERSION_MINOR = 5
app = Flask(__name__)

input_schema = {
    'type': 'object',
    'required': ['url'],
    'properties': {
        'url': {
            "type": 'string',
            'format': 'uri'
        },
        'project': {
            'type': 'string'
        },
        'includeRules': {
            'type': 'array',
            'items': {
                'type': 'integer',
                'minimum': 0,
                'uniqueItems': True
            },
            'default': []
        },
        'excludeRules': {
            'type': 'array',
            'items': {
                'type': 'integer',
                'minimum': 0,
                'uniqueItems': True
            },
            'default': []
        }
    }
}

# Preparing database connection
db = {
    'config': None,
    'connection': None
}

# Loading database connection configuration
db['config'] = None
if os.name == 'nt':
    with open('{}\\config.json'.format(os.getcwd())) as config_file:
        db_config = json.load(config_file)
else:
    with open('{}/config.json'.format(os.getcwd())) as config_file:
        db_config = json.load(config_file)

# Setting up database connection
db['connection'] = DBConnection(
    db_type=db_config['type'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['db'],
    user=db_config['user'],
    passwd=db_config['passwd']
)

import sogreenit.scan
import sogreenit.results
import sogreenit.views
