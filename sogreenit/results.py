from sogreenit import app, db

@app.route('/results/<project_id:int>')
def retrieve_project_results(project_id):
    pass

@app.route('/results/<page_id:int>')
def retrieve_page_results(page_id):
    pass
