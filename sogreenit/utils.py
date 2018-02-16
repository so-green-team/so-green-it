"""
Utilities function to compute DOM size and page weight
"""

def compute_dom_size(dom):
    """
    Computes the number of elements in a DOM document
    """
    elements = dom.find_elements_by_css_selector('*')
    size = 1

    if len(elements) > 1:
        for element in elements:
            size += compute_dom_size(element)

    return size

def compute_requests_weight(har):
    """
    Compute the whole weight loaded for a web page
    """
    weight = 0

    for entry in har['log']['entries']:
        weight += entry['response']['headersSize'] + entry['response']['bodySize']

    return weight
    