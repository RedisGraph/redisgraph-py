from util import *

class Node(object):
    """
    A node within the garph.
    """
    def __init__(self, node_id=None, alias=None, label=None, properties=None):
        """
        Create a new node
        """
        self.id = node_id
        self.alias = alias
        self.label = label
        self.properties = {} or properties

    def toString(self):
        res = ""
        if self.properties:
            props = ','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items())
            res += '{' + props + '}'

        return res

    def __str__(self):

        res = '('
        if self.alias:
            res += self.alias
        if self.label:
            res += ':' + self.label
        if self.properties:
            props = ','.join(key+':'+str(quote_string(val)) for key, val in self.properties.items())
            res += '{' + props + '}'
        res += ')'

        return res
