#TODO child class from test using arguments har, cpu and mem to calculate the ecoindex

from test import Test

class Ecoindex(Test):
    def __init__(self):
        tests_list.append("Ecoindex")

    def compute_dom_size(dom):
        elements = dom.find_elements()

        if len(elements) == 0:
            return 1
        else:
            size = 1
            for el in elements:
                size += compute_dom_size(el)
            return size

    def run(har, dom, cpu, mem):

        #param har is a dictionary with the content of the har file
        countRequest = 0
        log = har['log']
        countRequest = len(log['entries'])
        totalSize = 0
        for entry in log['entries']:
            totalSize += entry['response']['headersSize'] + entry['response']['bodySize']
        #param dom is the information about the size of the dom
        domSize = compute_dom_size(dom)

        #calculate the ecoindex
        #coeficient used for the computation
        coef_dom = 3
        coef_weight = 1
        coef_req = 2

        #TODO fetch the average in the sql
        average_dom = 1
        average_weight = 1
        average_nbr_req = 1

        #compute the difference between the averages and this analyse
        dom_gap = (domSize / average_dom) * coef_dom
        weight_gap = (totalSize / average_weight) * coef_weight
        req_gap = (countRequest / average_nbr_req) * coef_req
        ecoIndex = (dom_gap + weight_gap + req_gap) / (coef_dom + coef_weight + coef_req)

        #attribution of a note depending of the result of ecoIndex
        note = ""
        if ecoIndex < 0.2:
            note = "A"
        elif ecoIndex < 0.5:
            note = "B"
        elif ecoIndex < 0.75:
            note = "C"
        elif ecoIndex < 1:
            note = "D"
        elif ecoIndex < 1.5:
            note = "E"
        elif ecoIndex < 2:
            note = "F"
        else:
            note = "G"

        return note
