#TODO child class from test using arguments har, cpu and mem to calculate the ecoindex

from sogreenit.tests.test import Test
from sogreenit.utils import compute_dom_size
from sogreenit.utils import compute_requests_weight
from sogreenit import db

class EcoindexTest(Test):
    @staticmethod
    def run(har, dom, cpu, mem):
        #param har is a dictionary with the content of the har file
        count_request = 0
        log = har['log']
        count_request = len(log['entries'])

        total_weight = compute_requests_weight(har)

        #param dom is the information about the size of the dom
        dom_size = compute_dom_size(dom)

        #calculate the ecoindex
        #TODO fetch the average in the sql
        averages = db['connection'].make_request(
            """SELECT AVG(dom_size) AS average_dom_size, AVG(weight) AS average_weight, AVG(nbr_requests) AS average_nbr_requests
            FROM pages_results"""
        )[0]

        # Compute the difference between the averages and this analyse
        # Coefficients for each variables are :
        #  - 3 for DOM size
        #  - 1 for Total weight
        #  - 2 for the number of HTTP requests

        dom_gap = 3 * (dom_size / averages['average_dom_size']) * 3
        weight_gap = (total_weight / averages['average_weight'])
        req_gap = 2 * (count_request / averages['average_nbr_requests'])
        eco_index = (dom_gap + weight_gap + req_gap) / 6

        #attribution of a note depending of the result of ecoIndex
        grade = None
        if eco_index < 0.2:
            grade = 'A'
        elif eco_index < 0.5:
            grade = 'B'
        elif eco_index < 0.75:
            grade = 'C'
        elif eco_index < 1:
            grade = 'D'
        elif eco_index < 1.5:
            grade = 'E'
        elif eco_index < 2:
            grade = 'F'
        else:
            grade = 'G'

        return grade
