#TODO child class from test using arguments har, cpu and mem to calculate the ecoindex

from test import Test

class Ecoindex(Test):
    def __init__(self):
        tests_list.append("Ecoindex")

    def run(har, dom, cpu, mem):
        #TODO reimplement the calculate_ecoIndex function

        #param har is a dictionary with the content of the har file
        countRequest = 0
        log = har['log']
        countRequest = len(log['entries'])
        totalSize = 0
        for entry in log['entries']:
            totalSize += entry['response']['headersSize'] + entry['response']['bodySize']
        #param dom is the information about the size of the dom

        #param cpu is the information about the utilisation of the cpu
        #param mem is the information about the utilisation of the memory

        #calculate the ecoindex
        coef_dom = 3
        coef_poids = 1
        coef_req = 2

        #TODO fetch the average in the sql
        average_dom = 0
        average_poids = 0
        average_nbr_req = 0

        ecart_dom = (domSize / average_dom) * coef_dom
        ecart_poids = (totalSize / average_poids) * coef_poids
        ecart_req = (countRequest / average_nbr_req) * coef_req
        ecoIndex = (ecart_dom + ecart_poids + ecart_req) / (coef_dom + coef_poids + coef_req)

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
