"""NCBI Taxonomies read NCBI's taxonomy dumps"""

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"


from collections import OrderedDict

class DoubleRelies(Exception):
    def __init__(self, taxid, parent_taxid):
        self.taxid = taxid
        self.parent_taxid = parent_taxid

    def __str__(self):
        return repr("Double rely in the database for pair %s:%s"
                    % (self.taxid, self.parent_taxid))


def read_name_dump(file_path):
    """Reads names from a dump file.

    Params:
        file_path (str): Path to a name dmp file.

    Returns:
        names (dict): Dictionary with {taxid: name} pairs.

    e.g.:
    >>> filename = '/Work/code/BioTaxIDMapper/tmp/ncbi_taxonomy_test.dmp'
    >>> read_name_dump(filename)
    {'2': ['Bacteria', 'Monera', 'Procaryotae', 'Prokaryota']}

    """

    names = {}

    with open(file_path, 'r') as in_file:
        for node in in_file:
            node = node.split('\t|\t')
            taxid = node[0]
            name = node[1]

            if taxid not in names:
                names[taxid] = []

            names[taxid].append(name)

    return names

def read_node_dumps(file_path):
    """Reads node from a dump file.

    Params:
        file_path (str): Path to a name dmp file.

    Returns:
        relies (dict): Dictionary with {taxid: parent_taxid}.

    e.g.:
    >>> from collections import OrderedDict
    >>> filename = '/Work/code/BioTaxIDMapper/tmp/ncbi_taxonomy_test2.dmp'
    >>> nodes = read_node_dumps(filename)
    >>> test_case = {'2': '131567', '6': '335928', '7': '6', '9':'32199'}
    >>> shared_items = set(nodes.items()) & set(test_case.items())
    >>> len(shared_items)
    4

    """

    relies = {}

    with open(file_path, 'r') as in_file:
        for node in in_file:
            node = node.split('\t|\t')
            taxid = node[0]
            parent_taxid = node[1]

            # Do not take highest hierarchy nodes
            if taxid == parent_taxid:
                continue

            if taxid not in relies:
                relies[taxid] = parent_taxid
            else:
                raise DoubleRelies(taxid=taxid, parent_taxid=parent_taxid)

    return relies

def read_protein_taxid_links(file_path):


if __name__ == "__main__":
    import doctest
    doctest.testmod()
