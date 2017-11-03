# -*- coding: utf-8 -*-
# pylint: skip-file

from flask import Flask

VERSION_MAJOR = 0
VERSION_MINOR = 1
app = Flask(__name__)

import sogreenit.scan
import sogreenit.results

