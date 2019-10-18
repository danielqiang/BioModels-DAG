
_**This project is under active development as part of semantic data research with
[UW BIME](http://bime.uw.edu/).**_

# BioModels-ETL

<sub>_In collaboration with [Dr. John Gennari](http://bime.uw.edu/faculty/john-gennari/)._</sub>

Biomodels-ETL is an ETL pipeline for generating and visualizing semantic data networks 
from SBML [BioModels](https://www.ebi.ac.uk/biomodels/). An example network is displayed below
(visualized with Cytoscape):

![](https://imgur.com/oOglAcV.gif)
<sub><sup>
Relational data network representing parent-child relationships between BioModels.
PubMed models are displayed in red, curated EBI models are displayed in green.
</sup></sub>

The pipeline:
- Extracts and parses semantic RDF/XML data from multiple SBML BioModel providers
- Queries [GOlr](https://github.com/geneontology/amigo/tree/master/golr) REST API to acquire
 and integrate gene ontology JSON data with RDF/XML annotations
- Processes and loads RDF triples and visualization data into a NetworkX DAG
- Converts the DAG to a Cytoscape-compatible file format (e.g. GraphML) for use by 
[UW BIME](http://bime.uw.edu/) researchers and [EMBL-EBI](https://www.ebi.ac.uk/) staff.

Completed example networks are available [here](BioModels-ETL/data).

## Dependencies

[NetworkX](https://networkx.github.io/), [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
