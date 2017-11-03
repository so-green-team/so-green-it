# -*- coding: utf-8 -*-

from sogreenit import app

@app.route('/scan/static')
def scan_static():
    """
    Launch a static scan of one web page
    """
    return 'static'

@app.route('/scan/app')
def scan_app():
    """
    Launch a global scan of a web page
    """
    return 'app'
