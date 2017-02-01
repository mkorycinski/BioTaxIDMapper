"""TaxonomyDB module unit tests.

Tests for TaxDb class methods, some of which operate on a database.
For test purposes we create an instance of TaxDb class connecting to
test version of a database. Test database contains same kind of records,
but prepared directly in the mongo shell with pseudo-data."""

import unittest
import pymongo

from BioTaxIDMapper.TaxonomyDB import TaxDb
from BioTaxIDMapper.OwnObjects import Node, ProteinLink

TaxDb.NAME = 'TaxIDMapper_test'
database = TaxDb()


class TestTaxDb(unittest.TestCase):
    """Tests for TaxDb class"""

    def test_add_record(self):
        """Testing TaxDb.add_record method"""

        node_entry = Node(taxid='11',
                          scientific_name='Test_node_11_parent_22',
                          upper_hierarchy='22')

        database.add_record(node_entry.post_format())

        db = pymongo.MongoClient['TaxIDMapper_test'].nodes

        result = db.find_one({'TaxID':'11'})
        expected = {'TaxID':'11',
                    'SciName':'Test_node_11_parent_22',
                    'Parent':'22'}

        # db.delete_one({'TaxID':'11'})

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
