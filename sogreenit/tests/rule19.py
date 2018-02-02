#Child class from test testing 19th best practice
#Rule 19: Delete <img> where the src attribute is empty

from sogreenit.tests.test import Test

class rule19(Test):
    @staticmethod
    def run(har, dom, cpu, mem):
        images = dom.find_elements_by_tag_name('img')
        for img in images:
            if img.get_attribute('src') == '':
                return False
        return True
    