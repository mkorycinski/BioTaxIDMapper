"""Handling connection with a local Taxonomy Database."""

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"

import pymongo

class Node(object):
    """Describes Node object that is stored in the database as a document.
    Each node points to a parent node, unless tax_id = 0.

    """

    def __init__(self, taxid, scientific_name, upper_hierarchy, node_type=None):
        self.taxid = taxid
        self.scientific_name = scientific_name
        self.upper_hierarchy = upper_hierarchy
        self.node_type = node_type

    def post_format(self):
        return {'TaxID': self.taxid,
                'Parent': self.upper_hierarchy,
                'SciName': self.scientific_name}


class NoConnection(Exception):
    """Exception that is raised by each method that requires connection
    to the database
    """

    def __str__(self):
        return repr("No connection to the database! Exiting.")


class TaxDb(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies.

    """

    # Database connection parameters.
    HOSTNAME = 'localhost'
    PORT = '27017'
    STATUS = False

    def connect(self):
        """Connects to the database"""

        self.db_client = pymongo.MongoClient(self.HOSTNAME,
                                             self.PORT)

        database = self.db_client['TaxIDMapper']
        self.db_nodes = database.nodes
        self.db_names = database.names
        self.STATUS = True
        print('Connection to the database established')

    def disconnect(self):
        """Closes connection to the database"""

        self.db_client.close()

    def check_connection(self):
        """Checks whether connection to the database has been established.
        If not - raises No Connection exception.
        """

        if not self.STATUS:
            raise NoConnection


    def add_record(self, node):
        """Method updates database with a new entry.

        Params:
            node (Node): TaxDB node object

        Returns:
            result (ObjectId): Unique ID of a newly added record.

        """
        self.check_connection()

        record_id = self.db_nodes.insert_one(node.post_format())

        return record_id

    def record_exists(self, node):
        """Method checks whether the document already exists in the database"""

        self.check_connection()

        self.db_nodes.find_one(node.post_format())

    def organism_to_taxid(self, organism_name):
        """Method retrieves taxonomy ID for a query organism name.

        Params:
            organism_name (str): Binominal name of a query organism_name

        Returns:
            taxid (str): Taxonomy ID for a query organism

        e.g.:
        >>> TaxDb.organism_to_taxid('Archaeoglobus fulgidus DSM 4304')
        '224325'

        """

        pass

    def get_lineage_from_db(self, tax_id):
        """Method retrieves phylogenetic lineage from database based on
        accession.

        Params:
            tax_id (str): NCBI taxonomy identifier.

        Returns:
            lineage (str): Lineage of an organism represented by tax identifier.

        e.g.:
        >>> TaxDb.get_lineage_from_db('224325')
        ['cellular organisms', \
'Archaea', \
'Euryarchaeota', \
'Archaeoglobi', \
'Archaeoglobales', \
'Archaeoglobaceae', \
'Archaeoglobus', \
'Archaeoglobus fulgidus', \
'Archaeoglobus fulgidus DSM 4304']

        >>> TaxDb.get_lineage_from_db('2')
        ['cellular organisms', 'Bacteria']

        >> TaxIdDb.get_lineage_from_db('2759')
        ['cellular organisms', 'Eukaryota']

        """

        pass

