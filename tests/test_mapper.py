"""Unit tests for Mapper wrapper."""

import unittest
import os
import sys

# Assures that even if package is not installed, or codebase
# is in isolated environment, developer can run tests.
sys.path.insert(0, os.path.abspath('..'))

# Import module we gonna test
from mapper import version_to_accession, read_protein_acc


class TestMapper(unittest.TestCase):
    """Test class for Mapper testing."""
    def test_version_to_accession(self):
        """Test version_to_accession method"""

        self.assertEqual(version_to_accession('P06912.2'),
                         'P06912')
        self.assertEqual(version_to_accession('P22935.23'),
                         'P22935')

    def test_read_protein_acc(self):
        """Tests read_protein method"""

        # Test definition lines in FASTA-like format
        deflines = [
            '>gi|401774261|emb|CCJ07127.1| Conserved hypothetical protein \
            [Methylocystis sp. SC2]',
            '>WP_011112927.1 hypothetical protein [Nitrosomonas europaea]',
            '>sp|Q8I6R7|ACN2_ACAGO Acanthoscurrin-2 (Fragment) \
            OS=Acanthoscurria gomesiana GN=acantho2 PE=1 SV=1',
            '>UniRef50_Q9K794 Putative AgrB-like protein n=2 Tax=Bacillus \
            TaxID=1386 RepID=AGRB_BACHD',
        ]

        # Result we are testing
        result = [read_protein_acc(defline[1:]) for defline in deflines]

        # What we expect
        expected = ['CCJ07127', 'WP_011112927', 'Q8I6R7', 'UniRef50_Q9K794']

        # Assert whether we get what we want
        self.assertListEqual(list1=result, list2=expected)


if __name__ == '__main__':
    unittest.main()
