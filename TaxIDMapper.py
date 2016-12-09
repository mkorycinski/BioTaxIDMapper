# __author__ == "Mateusz Korycinski"


class MapTaxID(object):
    """Class containing methods to handle users requests for translating
    tax ids into phylogenies
    """
    def __init__(self, in_file):
        self.in_file = in_file
        dot_ind = in_file.rfind(".")
        self.out_file = "%s_taxonomy%s" % (in_file[:dot_ind], \
                                           in_file[dot_ind:])

    @staticmethod
    def get_accession_from_defline(dline):
        """Method retrieves accession code from definition line of a FASTA file
        """
        # If file is FASTA from NCBI / old styel
        if "|" in dline:
            return dline.split("|")[1]
        
        # Otherwise take as accession first word from definition line following
        # the ">" sign of FASTA
        else:
            return dline.split()[0][1:]

    def get_lineage_from_db(self, acc):
        """Method retrieves phylogenetic lineage from database based on
        accession.
        """
        #connecting to db
        #retrieve db entry
        pass

    def map(self):
        """Method for mapping phylogenetic lineage onto file containing
        sequences in FASTA format (e.g. FASTA or CLANS)
        """
        
        # Open input file for reading and output file for saving
        with open(self.in_file, 'r') as ifile, \
                open(self.out_file, 'w') as ofile:
            for line in ifile:
                if line.startswith(">"):
                    accession = self.get_accession_from_defline(line)
                    lineage = self.get_lineage_from_db(accession)
                    ofile.write(">%s {%s}\n" % (line.strip(), lineage))
                else:
                    ofile.write(line)




if __name__ == "__main__":
    print "Biological TaxID mapper"
