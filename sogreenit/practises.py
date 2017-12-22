# -*- coding: utf-8 -*-

from sogreenit import app

@app.route('/practices')
def get_practices():
    """
    Return all the practices availables to the test
    """
    pass

@app.route('/practices/<int:practice_id>')
@app.route('/practices/<string:practice_id>')
def get_practice(practice_id):
    """
    Return the practice identified by the given identifier
    """
    pass
