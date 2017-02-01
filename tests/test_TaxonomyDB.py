"""TaxonomyDB module unit tests.

Tests for TaxDb class methods, some of which operate on a database.
For test purposes we create an instance of TaxDb class connecting to
test version of a database. Test database contains same kind of records,
but prepared directly in the mongo shell with pseudo-data."""

import unittest
import pymongo

from ..TaxonomyDB import TaxDb
from ..OwnObjects import Node, ProteinLink

def set_up_test_db(db_name):
    """Sets up temporary database for test purposes."""
    
    client = pymongo.MongoClient()
    db = client[db_name]
    
    for i in range(10, -1, -1):
        if i == 0:
            parent = unicode(0)
        else:
            parent = unicode(i - 1)
        
        db.nodes.insert_one({'TaxID': unicode(i),
                             'SciName': u'Species_lvl_%d' % i,
                             'Parent': parent
                             })
        
        db.links.insert_one({'ProteinID': u'P%d' % i,
                             'TaxID': unicode(i)})

# Create an instance of a class we gonna test
TaxDb.NAME = 'TaxIDMapper_test'
database = TaxDb()

# Connect to the same database with pymongo interface
# to avoid using more than one method from TaxDb class
# in a single test.
client = pymongo.MongoClient()
db_pymongo = client[TaxDb.NAME]

# Set up database with test data
set_up_test_db(TaxDb.NAME)

    
class TestTaxDb(unittest.TestCase):
    """Tests for TaxDb class"""
    
    def test_add_record(self):
        """Testing TaxDb.add_record method"""

        node_entry = Node(taxid='11',
                          scientific_name='Test_node_11_parent_22',
                          upper_hierarchy='10')

        database.add_record(node_entry)

        # read results with pymongo
        result = db_pymongo.nodes.find_one({'TaxID':'11'})

        # remove unique ID given by MongoDB client
        result.pop('_id')
        
        # what we expect to receive
        expected = {'TaxID':'11',
                    'SciName':'Test_node_11_parent_22',
                    'Parent':'10'}

        # db.delete_one({'TaxID':'11'})
        
        # assert if dictionaries are the same
        self.assertDictEqual(d1=result, d2=expected)
        
    def test_add_protein_link(self):
        """Tests TaxDb.add_protein_link method"""
        
        protein_link = ProteinLink(protein_id='P11',
                                   taxid='11')
        
        # method we test
        database.add_protein_link(protein_link)
        
        # read results with pymongo
        result = db_pymongo.links.find_one({'ProteinID': 'P11'})
        
        # remove unique ID given by MongoDB client
        result.pop('_id')
        
        # what we expect
        expected = {'ProteinID': 'P11',
                  'TaxID': '11'}
        
        self.assertDictEqual(d1=result, d2=expected)
        
    def test_get_node(self):
        """Tests TaxDb.get_node method"""
        
        record = database.get_node('10')
        record = record.post_format()
        
        expected = {'TaxID': u'10',
                  'SciName': u'Species_lvl_10',
                  'Parent': u'9'}
        
        self.assertDictEqual(d1=record, d2=expected)
        
    def test_search_scientific_name(self):
        """Tests TaxDb.search_scientific_name method"""
        
        # Method we want to test
        record = database.search_scientific_name('Species_lvl_10')
        record = record.post_format()
        
        # Result we expect
        expected = {'TaxID': u'10',
                  'SciName': u'Species_lvl_10',
                  'Parent': u'9'}
        
        # Assert if we get what we want
        self.assertDictEqual(d1=record, d2=expected)
        
    def test_protein_taxid(self):
        """Tests TaxDb.protein_taxid method"""
        
        # Method we want to test
        record = database.protein_taxid('P10')
        
        # What we expect
        # expect = {'ProteinID': 'P10',
        #           'TaxID': '10'}
        expected = u'10'
        
        # Assert if we get what we want
        self.assertEqual(first=record, second=expected)
        
    def test_get_lineage_from_db(self):
        """Tests TaxDb.get_lineage_from_db method"""
        
        # Method we want to test
        record = database.get_lineage_from_db('10')
        
        # What we expect
        expected = [u'Species_lvl_%d' % i for i in range(0, 11)]
        
        # Assert if we get what we want
        self.assertListEqual(list1=record, list2=expected)

if __name__ == '__main__':
    unittest.main()
    client.drop_database(TaxDb.NAME)
