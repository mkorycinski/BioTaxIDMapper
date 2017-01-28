#!/usr/bin/env python

"""TaxIDMapper provides wrapper for maintaining TaxID database containing
links between protein accession codes and taxonomy identifiers and lineages.

Input:
    FASTA      (str, stdin): FASTA format query sequences
    FASTA_file (str):        Path to a FASTA file with query sequences
    Org_list   (str, stdin): List of query organisms, one per line.
    Org_list   (str):        Path to a file with list of query organisms,
                             one per line.

Output:
    Lineage (list): Full lineage for a query organism
"""

__author__      = "Mateusz Korycinski"
__license__     = "GPL"
__version__     = "1.0"
__maintainer__  = "Mateusz Korycinski"
__email__       = "mkorycinski@protonmail.ch"
__status__      = "Testing"


# Global imports

# Local imports
from TaxonomyDB import TaxDb

def main():
    pass

    
if __name__ == "__main__":
    main()
