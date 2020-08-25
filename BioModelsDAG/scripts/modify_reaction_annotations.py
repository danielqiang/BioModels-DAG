from BioModelsDAG import yield_model_paths, classify, extract_annotation_identifiers
from bs4 import BeautifulSoup
import libsbml


def yield_complex_assembly_reactions():
    for fpath in yield_model_paths():
        model = libsbml.readSBMLFromFile(fpath).getModel()
        if model is None:
            continue

        for reaction in model.getListOfReactions():
            if classify(reaction, model) == 'complex assembly':
                print(fpath, reaction.getId(), sep=' | ')
                yield reaction, get_reactant_species_ids(reaction, model)


def get_reactant_species_ids(reaction: libsbml.Reaction, model: libsbml.Model):
    product = reaction.getListOfProducts()[0]
    product_species = model.getSpecies(product.toXMLNode().getAttrValue('species'))
    product_identifiers = set(extract_annotation_identifiers(product_species.getAnnotationString()))
    return product_identifiers


def new_rdf_annotation(metaid):
    """
    Creates and returns a standard RDF/XML annotation tag.

    The annotation tag is as follows:

        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:bqmodel="http://biomodels.net/model-qualifiers/"
                 xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
            <rdf:Description rdf:about="<'metaid' argument value>">
            </rdf:Description>
        </rdf:RDF>

    :param metaid: MetaID for SBML object containing this annotation.
    :rtype: bs4.Tag
    """
    return BeautifulSoup(
        f"""
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:bqmodel="http://biomodels.net/model-qualifiers/"
                 xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
            <rdf:Description rdf:about="{metaid}">
            </rdf:Description>
        </rdf:RDF>
        """,
        features='xml'
    ).find("rdf:RDF")


def new_version_tag():
    """
    Creates and returns the following XML tag:
        <bqbiol:isVersionOf>
            <rdf:Bag>
            </rdf:Bag>
        </bqbiol:isVersionOf>

    :rtype: bs4.Tag
    """
    # BeautifulSoup's xml parser requires valid namespace definitions.
    return BeautifulSoup(
        """
        <ns xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
                xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
            <bqbiol:isVersionOf>
                <rdf:Bag> 
                </rdf:Bag>
            </bqbiol:isVersionOf>
        </ns>
        """,
        features='xml'
    ).find("bqbiol:isVersionOf")


def annotate_reaction(reaction, species_ids):
    soup = BeautifulSoup(reaction.getAnnotationString(), features='xml')

    if not soup.contents:
        soup.append(soup.new_tag("annotation"))
    if not soup.find("rdf:Description"):
        soup.find("annotation").append(
            new_rdf_annotation(reaction.toXMLNode().getAttrValue('metaid'))
        )
    if not soup.find("bqbiol:isVersionOf"):
        soup.find("rdf:Description").append(new_version_tag())
    # Define the ReactDescript namespace
    soup.find("rdf:RDF")['xmlns:ReactDescript'] = "http://biomodels.net/reaction-description"

    soup.find("rdf:Bag").append(
        soup.new_tag(
            "rdf:li",
            attrs={"rdf:resource": "http://identifiers.org/GO:0065003"}
        )
    )
    for identifier in species_ids:
        soup.find("rdf:Bag").append(
            soup.new_tag(
                "ReactDescript:complexPart",
                attrs={"ReactDescript:resource": identifier}
            )
        )
    print("<!--==========ANNOTATION OUTPUT=========-->")
    print(soup.find("annotation").prettify())

    reaction.setAnnotation(soup.find('annotation').prettify())


def main():
    for reaction, species_ids in yield_complex_assembly_reactions():
        soup = BeautifulSoup(reaction.getAnnotationString(), features='xml')
        if soup.contents and not soup.find("rdf:Description"):
            print("<!--=========ORIGINAL ANNOTATION========-->")
            print(reaction.getAnnotationString())

            annotate_reaction(reaction, species_ids)

            print("<!--========LIBSBML NEW ANNOTATION======-->")
            print(reaction.getAnnotationString())


if __name__ == '__main__':
    main()
