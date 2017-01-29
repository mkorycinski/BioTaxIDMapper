"""Module containing non-standard exceptions"""

class NoConnection(Exception):
    """Exception that is raised by each method that requires connection
    to the database

    e.g.:
    >>> raise NoConnection
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.NoConnection[0]>", line 1, in <module>
        raise NoConnection
    NoConnection: 'No connection to the database! Exiting.'

    """
    
    def __str__(self):
        return repr("No connection to the database! Exiting.")
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()