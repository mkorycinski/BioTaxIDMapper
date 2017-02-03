"""Unit tests for NCBI taxonomies parser"""

import unittest
import os
import sys

# Assures that even if package is not installed, or codebase
# is in isolated environment, developer can run tests.
sys.path.insert(0, os.path.abspath('..'))

# Import module we gonna test
import ncbi_taxonomies as tax

class TestNCBITaxonomies(unittest.TestCase):
    """Class for testing ncbi_taxonomies module"""

    @classmethod
    def setUpClass(cls):
        cls.current_location = os.path.abspath('.')
        print(cls.current_location)

    def test_read_names_dump(self):
        """Tests ncbi_taxonomies.read_name_dump method"""

        # Read names from the test file
        names = tax.read_names_dump(
            '%s/test_files/test_names.dmp' % cls.current_location)

        # What we expect
        expected = {'2': 'Bacteria'}

        # Assert if it works
        self.assertDictEqual(d1=names, d2=expected)

    def test_read_nodes_dump(self):
        """Tests ncbi_taxonomies.read_nodes_dump"""

        # Read nodes from the test file
        nodes = tax.read_nodes_dump('./test_files/test_nodes.dmp')

        # What we expect
        expected = {'2': '131567', '6': '335928', '7': '6', '9':'32199'}

        # Assert if works
        self.assertDictEqual(d1=nodes, d2=expected)

    def test_read_protein_taxid_links(self):
        """Tests ncbi_taxonomies.read_protein_taxid_links"""

        # Read links from the test file
        links = tax.read_protein_taxid_links('./test_files/test_links.txt')

        # What we expect
        expected = {'P29373': '9606',
                    'P22935': '10090',
                    'P18902': '9913',
                    'P02753': '9606',
                    'P27485': '9823',
                    'P06912': '9986',
                    'P04916': '10116',
                    'P06172': '8355',
                    'P12689': '559292',
                    'P24097': '417296'}

        # Assert if it works
        self.assertDictEqual(d1=links, d2=expected)

if __name__ == '__main__':
    unittest.main()
