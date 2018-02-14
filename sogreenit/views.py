# -*- coding: utf-8 -*-

from flask import render_template
from sogreenit import app

@app.route('/')
def demo_view():
    return render_template('demo.html')
