#! /usr/bin/env python
"""Wrapper for the BioTaxIDMapper package."""

from os import sys
import argparse

from taxonomydb import TaxDb

usage = """Biological Taxonomies ID Mapper.
This simple tool allows to map NCBI taxonomy database information onto files
containing FASTA-like definition lines. Taxonomic lineage is appended to the
defline between '#|' and '|#' delimiters. Each node is separated with '<->'.

e.g.:
    > (...) #|cellular organisms <-> Bacteria |#
    
To run simply type:
./mapper.py -i [IN_FILE] -o [OUT_FILE]
"""

def parse_arguments(argv):
    """Parses user arguments."""

    parser = argparse.ArgumentParser(description=usage,
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i',
                        '--input-file',
                        help='Input file with FASTA-like deflines',
                        type=str,
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        help='Output file with taxonomies marked. ' +
                             'If not specified results will be written to' +
                             '\'annotated.txt\'',
                        type=str,
                        required=False,
                        default='annotated.txt')

    args = parser.parse_args(argv)

    return args


def version_to_accession(protein_ver):
    """Extracts accession from a version.

    Params:
        protein_ver (str): Protein version ID

    Returns:
        protein_acc (str): Protein accession ID
    """
    if '.' in protein_ver:
        return protein_ver[:protein_ver.rfind('.')]
    else:
        return protein_ver

def read_protein_acc(defline):
    """Retrieves protein accession from a definition line.

    Params:
        defline (str): Definition line in FASTA-like format

    Returns:
        protein_acc (str): Protein accession ID
    """

    if defline.startswith('gi|'):
        protein_version = defline.split('|')[3]
        return version_to_accession(protein_version)

    elif ( defline.startswith('sp|') or
           defline.startswith('tr|') ):
        return defline.split('|')[1]

    else:
        protein_version = defline.split()[0]
        return version_to_accession(protein_version)

def map_taxonomies(in_file, out_file):
    """Maps taxonomies onto deflines from input file.
    Params:
        in_file (str): Input filename
        out_file (str): Output filename

    Returns:
        Writes output file, as specified in input parameters, with taxonomy
        markings.
    """

    # Connect to the database
    database = TaxDb()

    # Open input and output files for reading / writing
    with open(args.input_file, 'r') as in_file, \
        open(args.output_file, 'w') as out_file:

        # Iterate in line per line fashion
        for line in in_file:
            # If it is not defline - write to putput as it is
            if not line.startswith('>'):
                out_file.write(line)
                continue
            
            # Retrieve data from the database
            protein_acc = read_protein_acc(line[1:])
            taxid = database.protein_taxid(protein_acc)
            lineage = database.get_lineage_from_db(taxid)

            # Create lineage string in a human-readable way
            lineage = "<->".join(lineage)

            # Create new definition line containing lineage
            new_defline = '%s #| %s |#\n' % (line.strip(),
                                             lineage)
            # Write to output
            out_file.write(new_defline)

    # Just in case - disconnect from the database
    database.disconnect()

if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    map_taxonomies(args.input_file, args.output_file)