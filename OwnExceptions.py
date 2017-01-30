"""Module containing non-standard exceptions"""

class NoConnection(Exception):
    """Exception that is raised if a method requires database connection, but
    connection is not established.
    """
    
    def __str__(self):
        return repr("No connection to the database! Exiting.")
    
    
class NoProteinLink(Exception):
    """Exception raised when link between protein accession and taxid does
    not exist.
    """
    def __init__(self, protein_acc):
        self.protein_acc = protein_acc
        
    def __str__(self):
        return repr("No link for %s found." % self.protein_acc)
    
    
class NoRecord(Exception):
    """Exception raised when record cannot be found in the database."""
    
    def __init__(self, identifier):
        self.identifier = identifier
        
    def __str__(self):
        return repr('%s record doesn\'t exist in the database.'
                     % self.identifier)
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()