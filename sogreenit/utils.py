# -*- coding: utf-8 -*-

"""
Utilities function to compute DOM size and page weight
"""

def compute_dom_size(dom):
    """
    Computes the number of elements in a DOM document
    """
    # Weird things happens with this algorithm when it's used with Selenium API
    # So, we just go with an estimation based on the root element of the DOM document

    #elements = dom.find_elements_by_xpath('.//*')
    #size = 1
    
    #print(len(elements))
    #if len(elements) > 0:
    #    for element in elements:
    #        size += compute_dom_size(element)

    #return size
    return len(dom.find_elements_by_css_selector('*'))

def compute_requests_weight(har):
    """
    Compute the whole weight loaded for a web page
    """
    weight = 0

    for entry in har['log']['entries']:
        weight += entry['response']['headersSize'] + entry['response']['bodySize']

    return weight
    