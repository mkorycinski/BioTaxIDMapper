"""Unit tests for Mapper wrapper."""

import unittest
from BioTaxIDMapper.Mapper import version_to_accession, read_protein_acc


class TestMapper(unittest.TestCase):
    """Test class for Mapper testing."""
    def test_version_to_accession(self):
        """Test version_to_accession method"""

        self.assertEqual(version_to_accession('P06912.2'),
                         'P06912')
        self.assertEqual(version_to_accession('P22935.23'),
                         'P22935')

    def test_read_protein_acc(self):
        deflines = [
            '>gi|401774261|emb|CCJ07127.1| Conserved hypothetical protein [Methylocystis sp. SC2]',
            '>WP_011112927.1 hypothetical protein [Nitrosomonas europaea]',
            '>sp|Q8I6R7|ACN2_ACAGO Acanthoscurrin-2 (Fragment) OS=Acanthoscurria gomesiana GN=acantho2 PE=1 SV=1',
            '>UniRef50_Q9K794 Putative AgrB-like protein n=2 Tax=Bacillus TaxID=1386 RepID=AGRB_BACHD',
        ]

        result = [read_protein_acc(defline[1:]) for defline in deflines]
        expected = ['CCJ07127', 'WP_011112927', 'Q8I6R7', 'UniRef50_Q9K794']

        self.assertEqual(result, expected)

    def map_taxonomies(self):
        fasta_test = '''>gi|401774261|emb|CCJ07127.1| Conserved hypothetical protein [Methylocystis sp. SC2]
        ATGATGATTAGTAGATGATGATGATGATGATAGTAGTAT
        >WP_011112927.1 hypothetical protein [Nitrosomonas europaea]
        ATGATGATTAGTAGATGATGATGATGATGATAGTAGTAT
        >sp|Q8I6R7|ACN2_ACAGO Acanthoscurrin-2 (Fragment) OS=Acanthoscurria gomesiana GN=acantho2 PE=1 SV=1
        ATGATGATTAGTAGATGATGATGATGATGATAGTAGTAT
        >UniRef50_Q9K794 Putative AgrB-like protein n=2 Tax=Bacillus TaxID=1386 RepID=AGRB_BACHD
        ATGATGATTAGTAGATGATGATGATGATGATAGTAGTAT'''

if __name__ == '__main__':
    unittest.main()