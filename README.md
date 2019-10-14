
_**This project is under active development as part of semantic data research with
[UW BIME](http://bime.uw.edu/).**_

# BioModels-ETL

<sub>_In collaboration with [Dr. John Gennari](http://bime.uw.edu/faculty/john-gennari/)._</sub>

Biomodels-ETL is an ETL pipeline for generating and visualizing semantic data networks 
from SBML [BioModels](https://www.ebi.ac.uk/biomodels/). An example network is displayed below
(via Cytoscape):

![](https://imgur.com/oOglAcV.gif)
<sub><sup>
Small subset of relational data network between derived BioModels.
PubMed models are displayed in red, EBI models are displayed in green.
</sup></sub>

The pipeline:
- Integrates and extracts semantic data from multiple RDF/XML SBML BioModel providers
- Processes and loads RDF triples and visualization data into a NetworkX DAG
- Converts the DAG to a Cytoscape-compatible file format (e.g. GraphML) for use by 
[UW BIME](http://bime.uw.edu/) researchers and [EMBL-EBI](https://www.ebi.ac.uk/) staff.

## Dependencies

[NetworkX](https://networkx.github.io/), [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
