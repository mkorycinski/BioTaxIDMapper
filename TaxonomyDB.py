"""Handling connection with a local Taxonomy Database."""

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"

# External imports
import pymongo

# Internal imports
from OwnExceptions import NoConnection
from OwnObjects import Node

class TaxDb(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies.

    """

    # Database connection parameters.
    HOSTNAME = 'localhost'
    PORT = 27017
    NAME = 'TaxIDMapper'
    STATUS = False

    def connect(self):
        """Connects to the database"""

        self.db_client = pymongo.MongoClient(self.HOSTNAME, self.PORT)

        database = self.db_client[self.NAME]
        self.db_nodes = database.nodes
        self.db_links = database.links
        self.STATUS = True
        print('Connection to the database established')
    
    # def setup_new_db(self):
    #     """Setup new empty database with required collections."""
    #
    #     db_client = pymongo.MongoClient(self.HOSTNAME, self.PORT)
    #
    #     database = db_client[self.NAME]
        
    
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

        record = self.db_nodes.find_one(node.post_format())

        if record:
            return True
        else:
            return False

    def get_record_taxid(self, taxid):
        """Retrieves record from the database by taxid.

        Params:
            taxid (str): query Taxonomy ID

        Returns:
            node (Node): Node object

        """

        self.check_connection()

        record = self.db_nodes.find_one({'TaxID':taxid})
        node = Node(taxid=record['TaxID'],
                    scientific_name=record['SciName'],
                    upper_hierarchy=record['Parent'])

        return node

    def protein_taxid(self, protein_id):
        """Translates protein id to taxonomy id"""

        record = self.db_links.find_one({'ProteinID':protein_id})
        return record['TaxID']

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()