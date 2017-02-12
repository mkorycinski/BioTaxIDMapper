"""NCBI Taxonomies read NCBI's taxonomy dumps"""

from own_exceptions import DoubleRelies
from own_objects import ProteinLink

def read_names_dump(file_path):
    """Reads names from a dump file.

    Params:
        file_path (str): Path to a name dmp file.

    Returns:
        names (dict): Dictionary with {taxid: name} pairs.
    """

    names = {}

    with open(file_path, 'r') as in_file:
        for node in in_file:
            node = node.split('\t|\t')
            taxid = node[0]
            name = node[1]
            status = node[3].split('\t|')[0].strip()

            if taxid not in names and status == 'scientific name':
                names[taxid] = name

    return names

def read_nodes_dump(file_path):
    """Reads node from a dump file.

    Params:
        file_path (str): Path to a name dmp file.

    Returns:
        relies (dict): Dictionary with {taxid: parent_taxid}.

    # e.g.:
    # >>> filename = '/Work/code/BioTaxIDMapper/tmp/test_nodes.dmp'
    # >>> nodes = read_node_dumps(filename)
    # >>> test_case = {'2': '131567', '6': '335928', '7': '6', '9':'32199'}
    # >>> shared_items = set(nodes.items()) & set(test_case.items())
    # >>> test_case['2']
    # '131567'

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

def protein_taxid_links(file_path):
    """Reads protein - taxid links from NCBI link DB.

    Generator goes through protein links one by one

    Params:
        file_path (str): Path to a name dmp file.

    Returns:
        links (dict): Dictionary with {protein_id: taxid}

    e.g.:
    >>> links = read_protein_taxid_links(test_links.txtinks['P06912']
    '9986'

    >>> links['P18902']
    '9913'

    """

    with open(file_path, 'r') as in_file:
        for link in in_file:
            if link.startswith('accession'):
                continue

            link = link.split()
            protein_acc = link[0]
            taxid = link[2]

            yield ProteinLink(protein_id=protein_acc,
                              taxid=taxid)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
