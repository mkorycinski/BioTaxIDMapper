# BioTaxIDMapper
BioTaxIDMapper is a simple tool for mapping taxonomy information onto files containing FASTA-like headers. It keeps local database containing links between protein accessions and taxonomy identifiers, as well as whole taxonomic lineages. Scripts provided together with the tool allows to constantly update local database using NCBI taxonomy dumps and link file containing taxid mapping onto protein IDs / accessions.

**Requirements**

Beside standard libraries BioTaxIDMapper requires **pymongo** ver. 3.4.0 or higher. It can be installed with [pip](https://pypi.python.org/pypi/pip):
```
pip install pymongo
```


## Creating a local database
In order to run software you need to install [MongoDB](https://www.mongodb.com/) database. Database configuration is specified in the file **db.cfg**. File contains 3 parameters and comment lines:
```
# This is comment line that is omitted by parser.
HOSTNAME=localhost
PORT=27017
NAME=TaxIDMapper
```
You don't need to create specific databases and collections, it will be done autmatically when first records will be added. However keep in mind that if you alredy have a database with name as specified in the configuration file, records will be added to already existing one. In such case it might be a smart move to change name in the config file.

**Data I/O Speedup**

In order to increase the speed with which records are added and / or retrieved, as well as to ommit having duplicated documents, I highly recommend creating unique Indexes for fields **'TaxID'** in the **'nodes'** collection, and **'ProteinID'** in the **'links'** collection. It can be achieved in MongoDB shell by executing:
```
> use TaxIDMapper
> db.nodes.createIndex( { TaxID: 1 }, { unique: true } )
> db.links.createIndex( { ProteinID: 1 }, { unique: true } )
```

More information about handling MongoDB can be found in official docs - [LINK](https://docs.mongodb.com/).

## Keeping database up to date
In order to update local database you can use provided script. Remember to set correct database in the config file. To run script simply type:
```
python updatelocaldb.py [PATH_TO_NCBI_DIR]
```
Where **[PATH_TO_NCBI_DIR]** is a path where all required dump files are stored:
  - *names.dmp,* containing scientific names for Taxonomy IDs
  - *nodes.dmp,* containing nodes information
  - *protein_taxonomy.lnk,* containing links between protein IDs / accessions and taxonomy IDs

If your database is empty all records will be added at the first run. Keep in mind that if you didn't create indexes in the database collections you will encounter duplicate records. To avoid this either create Indexes (described above, speeds up interaction with the database) or update database only with new nodes and protein accession - taxid links (e.g. by diff between old and new files.)

## Mapping lineages onto files
To map Lineages you can either use **Mapper** script or use module interactively. To learn how to use mapper script simply run it with **-h** parameter:
```
./mapper.py -h
```

To use Mapper as a module in your python console simply:
```
#Import module class
>>> from BioTaxIDMapper.taxonomydb import TaxDb

# Create and instance
>>> t = TaxDb()
```

You my now use following methods depending on your needs:
  - t.add_record()
  - t.add_protein_link()
  - t.get_node()
  - t.search_scientific_name()
  - t.protein_taxid()
  - t.get_lineage_from_db()
  
Docstrings will explain you how to use each of the methods. It is important to now, that in order to get protein accession to tax id link, we use accession, not version (e.g. WP_12323, not WP_12323.1). Module **mapper** has a function that returns proper accession:
```
>>> from BioTaxIDMapper.mapper import version_to_accession
>>> version_to_accession('WP_12323.34')
'WP_12323'
```
## Contact
If you have any questions or suggestions regarding this tool or README file itself, feel free to contact me:
  - **E-mail:** mat . korycinski [at] gmail.com
  - **Twitter:** @mkorycinski
  
## Acknowledgments
  - Vikram Alva
  - Andrew Stephens
  - David Rau
  - Lukas Zimmermann
