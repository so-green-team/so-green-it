#TODO child class from test using arguments har, cpu and mem to calculate the ecoindex

from tests.test import Test

class EcoindexTest(Test):
    def compute_dom_size(self, dom):
        elements = dom.find_elements()

        if len(elements) == 0:
            return 1
        else:
            size = 1
            for el in elements:
                size += self.compute_dom_size(el)
            return size

    def run(self, har, dom, cpu, mem):
        #param har is a dictionary with the content of the har file
        count_request = 0
        log = har['log']
        count_request = len(log['entries'])
        total_size = 0
        for entry in log['entries']:
            total_size += entry['response']['headersSize'] + entry['response']['bodySize']

        #param dom is the information about the size of the dom
        dom_size = self.compute_dom_size(dom)

        #calculate the ecoindex
        #TODO fetch the average in the sql
        average_dom = 1
        average_weight = 1
        average_nbr_req = 1

        # Compute the difference between the averages and this analyse
        # Coefficients for each variables are :
        #  - 3 for DOM size
        #  - 1 for Total Size
        #  - 2 for the number of HTTP requests

        dom_gap = 3 * (dom_size / average_dom) * 3
        weight_gap = (total_size / average_weight)
        req_gap = 2 * (count_request / average_nbr_req)
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
