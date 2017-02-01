"""Handling connection with a local Taxonomy Database."""

import doctest
import pymongo
from pymongo.errors import AutoReconnect

from OwnExceptions import NoProteinLink, NoRecord
from OwnObjects import Node


# MongoDB connection test for methods requiring database access
def autoreconnect_retry(func, retries=3):
    """Decorating checking connection to the database."""
    def db_op_wrapper(*args, **kwargs):
        """Decorator wrapper"""
        tries = 0

        while tries < retries:
            try:
                return func(*args, **kwargs)

            except AutoReconnect:
                tries += 1

        raise Exception(
            "Couldn't connect to the database, even after %d retries" % retries)
    return db_op_wrapper

class TaxDb(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies.

    """

    # Database connection parameters.
    HOSTNAME = 'localhost'
    PORT = 27017
    NAME = 'TaxIDMapper'

    def __init__(self):
        """Connects to the database"""

        self.db_client = pymongo.MongoClient(self.HOSTNAME, self.PORT)

        database = self.db_client[self.NAME]
        self.db_nodes = database.nodes
        self.db_links = database.links

    def disconnect(self):
        """Closes connection to the database"""

        self.db_client.close()

    @autoreconnect_retry
    def add_record(self, node):
        """Method updates database with a new entry.

        Params:
            node (Node): TaxDB node object

        Returns:
            result (ObjectId): Unique ID of a newly added record.

        """

        try:
            self.db_nodes.insert_one(node.post_format())
        except pymongo.errors.DuplicateKeyError:
            print('%s already exists. Record not inserted.' % node.taxid)

    @autoreconnect_retry
    def add_protein_link(self, protein_link):
        """Method updates database with a new protein link.
        Params:
            protein_link (ProteinLink): ProteinLink object

        Returns:
            result (ObjectID): Unique ID of a newly added link
        """

        try:
            self.db_links.insert_one(protein_link.post_format())
        except pymongo.errors.DuplicateKeyError:
            print('%s already exists, link not inserted.'
                  % protein_link.protein_id)

    # @autoreconnect_retry
    # def record_exists(self, node):
    #     """Method checks whether record already exists in the database"""
    #
    #     record = self.db_nodes.find_one(node.post_format())
    #
    #     return bool(record)
    #
    # @autoreconnect_retry
    # def link_exists(self, protein_link):
    #     """Method checks whether record already exists in the database"""
    #
    #     record = self.db_links.find_one(protein_link.post_format())
    #
    #     return bool(record)

    @autoreconnect_retry
    def get_node(self, taxid):
        """Returns node record from database.

        Params:
            taxid (str): Taxonomy ID

        Returns:
            record (Node): Node record
        """

        result = self.db_nodes.find_one({'TaxID': taxid})

        if not result:
            raise NoRecord(taxid)

        record = Node(taxid=result['TaxID'],
                      scientific_name=result['SciName'],
                      upper_hierarchy=result['Parent'])

        return record

    @autoreconnect_retry
    def search_scientific_name(self, sci_name):
        """Search Database with scientific name

        Params:
            sci_name (str): Scientific name of an organism or phylum to search

        Returns:
            record (Node): Node record from the database

        """

        result = self.db_nodes.find_one({'SciName': sci_name})

        if not result:
            raise NoRecord(sci_name)

        record = Node(taxid=result['TaxID'],
                      scientific_name=result['SciName'],
                      upper_hierarchy=result['Parent'])

        return record

    @autoreconnect_retry
    def protein_taxid(self, protein_id):
        """Translates protein id to taxonomy id"""

        record = self.db_links.find_one({'ProteinID':protein_id})

        if not record:
            raise NoProteinLink(protein_acc=protein_id)

        return record['TaxID']

    def get_lineage_from_db(self, taxid, lineage=None):
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

        # If it is the first call
        if not lineage:
            lineage = []

        curr_taxid = self.get_node(taxid=taxid)

        # Check whether it is not the highest hierarchy possible
        if curr_taxid.taxid != curr_taxid.upper_hierarchy:
            # if there is higher hierarchy, append and travel up the tree
            lineage.append(curr_taxid.scientific_name)
            try:
                return TaxDb.get_lineage_from_db(self, curr_taxid.upper_hierarchy, lineage)
            except NoRecord:
                pass

        lineage.append(curr_taxid.scientific_name)
        lineage.reverse()
        return lineage

if __name__ == "__main__":
    doctest.testmod()
