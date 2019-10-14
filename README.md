
_**This project is under active development as part of semantic data research with
[UW BIME](http://bime.uw.edu/).**_

# BioModels-ETL

<sub>_In collaboration with [Dr. John Gennari](http://bime.uw.edu/faculty/john-gennari/)._</sub>

Biomodels-ETL is an ETL pipeline for generating and visualizing semantic data networks 
from SBML [BioModels](https://www.ebi.ac.uk/biomodels/). An example network is displayed below
(visualized with Cytoscape):

![](https://imgur.com/oOglAcV.gif)
<sub><sup>
Visual subset of relational data network between derived BioModels.
PubMed models are displayed in red, curated EBI models are displayed in green.
</sup></sub>

The pipeline:
- Integrates and extracts semantic data from multiple RDF/XML SBML BioModel providers
- Queries [GOlr](https://github.com/geneontology/amigo/tree/master/golr) REST API to
grab gene ontology JSON data
- Processes and loads RDF triples and visualization data into a NetworkX DAG
- Converts the DAG to a Cytoscape-compatible file format (e.g. GraphML) for use by 
[UW BIME](http://bime.uw.edu/) researchers and [EMBL-EBI](https://www.ebi.ac.uk/) staff.

## Dependencies

[NetworkX](https://networkx.github.io/), [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
