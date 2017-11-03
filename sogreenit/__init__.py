# -*- coding: utf-8 -*-
# pylint: skip-file

from flask import Flask

app = Flask(__name__)

import sogreenit.scan
import sogreenit.results

