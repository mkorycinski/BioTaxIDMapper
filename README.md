# BioTaxIDMapper
BioTaxIDMapper is a simple tool for mapping taxonomy information onto files containing FASTA-like headers. It keeps local database containing links between protein accessions and taxonomy identifiers, as well as whole taxonomic lineages. Scripts provided together with the tool allows to constantly update local database using NCBI taxonomy dumps and link file containing taxid mapping onto protein IDs / accessions.


## Creating a local database
TO BE FILLED WHEN FUNCTIONALITY IS FULLY IMPLEMENTED


## Keeping database up to date
In order to update local database you can use provided script. Remember to set correct database in use, either by specifying TaxDB class attributes **TaxDB.HOSTNAME** and **TaxDB.PORT**. To run script simply type:
```
python UpdateLocalDB.py [PATH_TO_NCBI_DIR]
```
Where **[PATH_TO_NCBI_DIR]** is a path where all required dump files are stored:
  - *names.dmp,* containing scientific names for Taxonomy IDs
  - *nodes.dmp,* containing nodes information
  - *protein_taxonomy.lnk,* containing links between protein IDs / accessions and taxonomy IDs


## Mapping lineages onto a files
TO BE FILLED WHEN FUNCTIONALITY IS FULLY IMPLEMENTED
