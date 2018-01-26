# -*- coding: utf-8 -*-
# pylint: skip-file

from flask import Flask

VERSION_MAJOR = 0
VERSION_MINOR = 1
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

import sogreenit.scan
import sogreenit.results

