#!/usr/bin/env python

"""TaxIDMapper provides wrapper for maintaining TaxID database containing
links between protein accession codes and taxonomy identifiers and lineages.
"""

from Bio import Entrez
from os import sys

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"


# Required by Entrez
Entrez.email = "mkorycinski@protonmail.ch"


class TaxIdDb(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies.

    """
    def __init__(self):
        self.database = "/dbs/TaxID.mongodb"


    def get_lineage_from_db(self, tax_id):
        """Method retrieves phylogenetic lineage from database based on
        accession.

        Params:
            tax_id (str): NCBI taxonomy identifier.

        Returns:
            lineage (str): Lineage of an organism represented by tax identifier.

        e.g.:
        >>> TaxIdDb.get_lineage_from_db('224325')
        ['cellular organisms', \
'Archaea', \
'Euryarchaeota', \
'Archaeoglobi', \
'Archaeoglobales', \
'Archaeoglobaceae', \
'Archaeoglobus', \
'Archaeoglobus fulgidus', \
'Archaeoglobus fulgidus DSM 4304']

        >>> TaxIdDb.get_lineage_from_db('2')
        ['cellular organisms', 'Bacteria']

        >> TaxIdDb.get_lineage_from_db('2759')
        ['cellular organisms', 'Eukaryota']

        """
        #connecting to db
        #retrieve db entry
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

    @classmethod
    def retrieve_lineage(self, tax_id):
        """TaxIdDbTaxIdDb.retrieve_lineage retrievs full lineage for query
        Taxonomy identifier.

        Params:
            tax_id (str): NCBI Taxonomy identifier.

        Returns:
            lineage (list): Full lineage for given tax_id.

        e.g.:
        >>> TaxIdDb.retrieve_lineage('224325')
        ['cellular organisms', \
'Archaea', \
'Euryarchaeota', \
'Archaeoglobi', \
'Archaeoglobales', \
'Archaeoglobaceae', \
'Archaeoglobus', \
'Archaeoglobus fulgidus', \
'Archaeoglobus fulgidus DSM 4304']

        >>> TaxIdDb.retrieve_lineage('2')
        ['cellular organisms', 'Bacteria']

        >> TaxIdDb.retrieve_lineage('2759')
        ['cellular organisms', 'Eukaryota']

        """

        handle = Entrez.efetch(db='taxonomy',
                               id=tax_id,
                               retmode='xml')

        result = Entrez.read(handle)

        lineage = result[0]['Lineage'].split('; ')
        lineage.append(result[0]['ScientificName'])

        return lineage


def get_accession_from_defline(dline):
    """Method retrieves accession code from definition line of a FASTA file.

    Params:
        dline (str): Description line from FASTA file.

    Returns:
        accession (str): Protein accession ID.

    e.g.:
    >>> dline = ">WP12312.1 STAC domain-containing [Escherichia coli]"
    >>> get_accession_from_defline(dline)
    'WP12312.1'

    >>> dline = ">gi|123123|WP12312.1| STAC domain-containing [Escherichia coli]"
    >>> get_accession_from_defline(dline)
    'WP12312.1'

    """
    # If file is FASTA from NCBI / old styel
    if "|" in dline:
        accession = dline.split("|")[2]

    # Otherwise take as accession first word from definition line following
    # the ">" sign of FASTA
    else:
        accession = dline.split()[0][1:]

    return accession

def map_taxonomy(in_file, out_file):
    """Method for mapping phylogenetic lineage onto file containing
    sequences in FASTA format (e.g. FASTA or CLANS).

    Params:
        None

    Returns:
        Nothing

    """

    taxdb = TaxIdDb()
    # Open input file for reading and output file for saving
    with open(in_file, 'r') as ifile, \
            open(out_file, 'w') as ofile:
        for line in ifile:
            if line.startswith(">"):
                accession = get_accession_from_defline(line)
                lineage = taxdb.get_lineage_from_db(accession)
                ofile.write(">%s {%s}\n" % (line.strip(), lineage))
            else:
                ofile.write(line)

if __name__ == "__main__":
    from os import sys

    # Allow testing...
    if sys.argv[1] == "-v":
        import doctest
        doctest.testmod()

    # If no verbose mode is specified module will be run as a script
    # without tests.
    else:
        in_file = sys.argv[1]
        dot_ind = in_file.rfind(".")
        out_file = "%s_taxonomy%s" % (in_file[:dot_ind], in_file[dot_ind:])

        map_taxonomy(in_file=in_file, out_file=out_file)
