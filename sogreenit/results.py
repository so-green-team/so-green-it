# -*- coding: utf-8 -*-

from flask import jsonify
from sogreenit import app, db

@app.route('/results', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def results_help():
    """A little help for the use of this resource"""
    return jsonify(
        help={
            '/results/project/\{project_id\}': {
                'method': 'GET',
                'parameters': {
                    'project_id': 'The identifiant of your project in the database of So Green IT'
                },
                'description': 'Retrieves all the results computed and stored by So Green IT for a given project'
            },
            '/results/page/\{page_id\}': {
                'method': 'GET',
                'parameters': {
                    'page_id': 'The identifiant of your page in the database of So Green IT'
                },
                'description': 'Retrieves the results computed and stored by So Green IT of a web page'
            }
        }
    )

@app.route('/results/project/<int:project_id>', methods=['GET'])
def retrieve_project_results(project_id):
    # First we retrieve all the results attached to the project
    results = db['connection'].make_request(
        """SELECT pg.id AS page_id, pr.date, pg.ecoindex
        FROM projects p
        JOIN projects_results pr ON p.id = pr.project_id
        JOIN pages_results pg ON pr.id = pg.projects_results_id
        WHERE p.id = %s""",
        (
            project_id,
        )
    )

    # TODO: handle the case where no projects were found

    # Then, we prepare the sets of results
    output = []
    for result in results:
        output_result = {
            'date': result['date'],
            'ecoindex': result['ecoindex'],
            'stepResults': []
        }

        # Retrieving step results
        step_results = db['connection'].make_request(
            """SELECT bp_id AS bp, result
            FROM steps_results
            WHERE pages_results_id = %s""",
            (
                result['page_id'],
            )
        )
        for step_result in step_results:
            output_result['stepResults'].append({
                'bp': step_result['bp'],
                'result': step_result['result']
            })

        # Appending the result to the output
        output.append(output_result)

    return jsonify({
        'id': project_id,
        'results': output
    })

@app.route('/results/page/<int:page_id>', methods=['GET'])
def retrieve_page_results(page_id):
    # First, we retrieve the results of the page from the database
    page_result = db['connection'].make_request(
        """SELECT pr.date, pg.ecoindex
        FROM projects_results pr
        JOIN pages_results pg ON pr.id = pg.projects_results_id
        WHERE pg.id = %s""",
        (
            page_id,
        )
    )[0]

    # TODO: handle the case where no page results were found

    # Then, we retrieve the step results of the page
    step_results = db['connection'].make_request(
        """SELECT bp_id AS bp, result
        FROM steps_results
        WHERE pages_results_id = %s""",
        (
            page_id,
        )
    )

    # After, we format the step results for the output
    output = []
    for step_result in step_results:
        output.append({
            'bp': step_result['bp'],
            'result': step_result['result']
        })

    return jsonify({
        'id': page_id,
        'date': page_result['date'],
        'ecoindex': page_result['ecoindex'],
        'stepResults': output
    })
