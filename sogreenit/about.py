# -*- coding: utf-8 -*-

from sogreenit import VERSION_MAJOR, VERSION_MINOR, app
from flask import jsonify

@app.route('/version')
def version():
    """
    Returns the version and the copyright of the projet
    """
    return jsonify(
        project='So Green IT',
        copyright='So Green Team © 2017-2018',
        license='MIT',
        version=('%d.%d' % VERSION_MAJOR, VERSION_MINOR)
    )

@app.route('/about')
def about():
    """
    About this project
    """
    return jsonify(
        project='So Green IT',
        description='So Green IT is a Web API which aims to help web developers to respect the Green IT best practices.'
    )
