"""Handling connection with a local Taxonomy Database."""

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"


class Node(object):
    """Describes Node object that is stored in the database as a document.
    Each node points to a parent node, unless tax_id = 0.

    """
    
    def __init__(self, taxid, scientific_name, upper_hierarchy, node_type):
        self.taxid = taxid
        self.scientific_name = scientific_name
        self.upper_hierarchy = upper_hierarchy
        self.node_type = node_type


class TaxDb(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies.

    """

    self.database_path = "/dbs/TaxID.mongodb"


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

    def add_record(self, protein_acc, tax_id):
        """Method updates database with a new entry.

        Params:
            protein_acc (str): Protein accession Identifier
            tax_id (str): Taxonomy Identifier

        Returns:
            Nothing

        """

        pass

    def add_new_lineage(self, tax_id):
        """Method adds new lineage to a database.

        Params:
            lineage (str): Lineage to write to a database.

        Returns:
            Nothing

        """

        pass
