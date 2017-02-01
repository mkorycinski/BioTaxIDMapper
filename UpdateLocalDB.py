#!/usr/bin/env python

"""Script updating local taxonomy database.

Script allows to update local taxonomy database using new taxonomy dumps from
NCBI taxonomy database.

Requirements:
    Names file - path to NCBI taxonomy dmp file containing mapping of s
                 scientific names onto Taxonomy ID's. Default is 'names.dmp'.
    Nodes file - path to NCBI taxonomy dmp file containing node definitions with
                 tax id being mapped to a higher hierarchy node.
                 The default is 'nodes.dmp'.
    Links file - path to a file containing protein id - taxonomy id mapping.
                 The default is - 'protein_taxonomy.lnk'

"""

# External libraries imports
from os import sys

# Internal modules import
import NCBITaxonomies as ncbi
from TaxonomyDB import TaxDb
from OwnObjects import Node, ProteinLink

# Directory where all files from NCBI have been downloaded and extracted
ncbi_download = sys.argv[1]

def update_nodes():
    """Updates nodes collection of the database."""

    # Paths to all required files.
    print('Reading nodes...')
    names_file = '%s/names.dmp' % ncbi_download
    nodes_file = '%s/nodes.dmp' % ncbi_download

    print('Updating nodes collection in the database...')
    names = ncbi.read_name_dump(names_file)
    nodes = ncbi.read_node_dumps(nodes_file)


    # Initialize connection with a database
    database = TaxDb()

    # Go through NCBI taxonomy dump records, update if record
    # doesn't exist
    for taxid, parent_taxid in nodes.iteritems():

        # If given taxid record does not exist
        # in a local database, create Node object
        # and create document in a database
        new_node = Node(taxid=taxid,
                        scientific_name=names[taxid],
                        upper_hierarchy=parent_taxid,)

        database.add_record(node=new_node)

    # Always disconnect the database!
    database.disconnect()

    print('Done!')

def update_links():
    """Updates links collection of the database."""

    print('Reading links...')
    links_file = '%s/prot.accession2taxid' % ncbi_download
    links = ncbi.read_protein_taxid_links(links_file)

    print('Updating links collection...')
    database = TaxDb()

    # Go thorugh NCBI protein ACC - taxid mappings, update if record
    # doesn't exist
    for protein_acc, taxid in links.iteritems():
        new_link = ProteinLink(protein_id=protein_acc,
                               taxid=taxid)

        database.add_protein_link(new_link)

    # Always disconnect the database!
    database.disconnect()

    print('Done!')

if __name__ == "__main__":
    update_links()
    update_nodes()