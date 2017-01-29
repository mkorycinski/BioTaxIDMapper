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
from TaxonomyDB import TaxDb, Node

# Directory where all files from NCBI have been downloaded and extracted
ncbi_download = sys.argv[1]

# Paths to all required files.
names_file = '%s/names.dmp' % ncbi_download
nodes_file = '%s/nodes.dmp' % ncbi_download
links_file = '%s/protein_taxonomy.dmp' % ncbi_download

names = ncbi.read_name_dump(names_file)
nodes = ncbi.read_node_dumps(nodes_file)
links = ncbi.read_protein_taxid_links(links_file)

# Initialize connection with a database
database = TaxDb()
database.connect()

# Go through NCBI taxonomy dump records
for taxid, parent_taxid in nodes.iteritems():

    # If given taxid record does not exist
    # in a local database, create Node object
    # and create document in a database
    if not database.document_exists():
        new_node = Node(taxid=taxid,
                        scientific_name=names[taxid],
                        upper_hierarchy=parent_taxid,)

        database.add_record(node=new_node)

# Always disconnect the database!
database.disconnect()