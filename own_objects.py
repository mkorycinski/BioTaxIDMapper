"""Contains project-specific objects"""

class Node(object):
    """Describes Node object that is stored in the database as a document.
    Each node points to a parent node, unless tax_id = 0.

    """

    def __init__(self, taxid, scientific_name, upper_hierarchy, node_type=None):
        self.taxid = taxid
        self.scientific_name = scientific_name
        self.upper_hierarchy = upper_hierarchy
        self.node_type = node_type

    def post_format(self):
        """Formats object into post format required by MongoDB.
        
        Params:
            None
            
        Returns:
            Dictionary representation of an object
            
        e,g,:
        >>> node = Node(taxid='224325',
        ...             scientific_name='Archaeoglobus fulgidus DSM 4304',
        ...             upper_hierarchy='2234')
        >>> nd = node.post_format()
        >>> nd['TaxID']
        '224325'
        
        >>> nd['Parent']
        '2234'
        
        >>> nd['SciName']
        'Archaeoglobus fulgidus DSM 4304'
            
        """
        return {'TaxID': self.taxid,
                'Parent': self.upper_hierarchy,
                'SciName': self.scientific_name}
    
class ProteinLink(object):
    """Describes Protein link object that is stored in database's links
    collection."""
    
    def __init__(self, protein_id, taxid):
        self.protein_id = protein_id
        self.taxid = taxid
        
    def post_format(self):
        """Formats object into post format required by MongoDB.

        Params:
            None

        Returns:
            Dictionary representation of an object.

        e,g,:
        >>> p_link = ProteinLink(protein_id='WP123.1', taxid='224325')
        >>> nd = node.post_format()
        >>> nd['TaxID']
        '224325'

        >>> nd['ProteinID']
        'WP123.1'

        """
        
        return {'ProteinID':self.protein_id,
                'TaxID': self.taxid}

if __name__ == "__main__":
    import doctest
    doctest.testmod()