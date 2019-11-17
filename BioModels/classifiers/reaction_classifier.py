from BioModels import extract_annotation_identifiers
import libsbml

__all__ = [
    'is_complex_assembly',
    'is_transport',
    'classify'
]


def is_transport(reaction: libsbml.Reaction, model: libsbml.Model):
    """
    Returns true iff 'reaction' can be classified as a biological transport.

    Rules:
        - The reaction must have exactly one reactant and one product
        - The reactant and product must be annotated with the same non-empty set
          of identifiers (if they are annotated with the same identifiers,
          they are assumed to refer to the same biological object)
        - The reactant and product must reside in different compartments.

    :param reaction: libSBML Reaction object to classify as a transport.
    :param model: libsbml Model containing the 'reaction' object.
    :rtype: bool
    """
    if len(reaction.getListOfReactants()) != 1 or len(reaction.getListOfProducts()) != 1:
        return False

    reactant, product = reaction.getListOfReactants()[0], reaction.getListOfProducts()[0]
    reactant_species = model.getSpecies(reactant.toXMLNode().getAttrValue('species'))
    product_species = model.getSpecies(product.toXMLNode().getAttrValue('species'))

    reactant_compartment = model.getCompartment(reactant_species.getCompartment())
    product_compartment = model.getCompartment(product_species.getCompartment())

    reactant_identifiers = set(extract_annotation_identifiers(reactant_species.getAnnotationString()))
    product_identifiers = set(extract_annotation_identifiers(product_species.getAnnotationString()))

    return (
            len(reactant_identifiers) > 0
            and reactant_identifiers.intersection(product_identifiers)
            and reactant_compartment != product_compartment
    )


def is_complex_assembly(reaction: libsbml.Reaction, model: libsbml.Model):
    """
    Returns true iff 'reaction' can be classified as a biomolecular complex assembly.

    Rules:
        - The reaction must have at least two reactants and exactly one product
        - The product must be annotated with the same non-empty set
          of identifiers as the full set of identifiers for all reactants.
          (This is assumed to mean that the product contains all and consists
          only of the specified reactants, so the reaction is a complex assembly.)

    :param reaction: libSBML Reaction object to classify as a transport.
    :param model: libsbml Model containing the 'reaction' object.
    :rtype: bool
    """
    if len(reaction.getListOfReactants()) < 2 or len(reaction.getListOfProducts()) != 1:
        return False

    reactant_identifiers = set()
    for reactant in reaction.getListOfReactants():
        reactant_species = model.getSpecies(reactant.toXMLNode().getAttrValue('species'))
        reactant_identifiers.update(extract_annotation_identifiers(reactant_species.getAnnotationString()))

    product = reaction.getListOfProducts()[0]
    product_species = model.getSpecies(product.toXMLNode().getAttrValue('species'))
    product_identifiers = set(extract_annotation_identifiers(product_species.getAnnotationString()))

    return len(reactant_identifiers) > 0 and reactant_identifiers == product_identifiers


def classify(reaction: libsbml.Reaction, model: libsbml.Model):
    """
    Classify a libsbml.Reaction object.
    Returns a string representing the classification result.

    Possible return values:
        - 'transport' (if 'reaction' is a biological transport)
        - 'complex assembly' (if 'reaction' is a biomolecular complex assembly)
        - 'biochemical reaction' (if 'reaction' is a biochemical reaction').

    :param reaction: libSBML Reaction object to classify as a transport.
    :param model: libsbml Model containing the 'reaction' object.
    :rtype: str
    """
    if is_transport(reaction, model):
        return 'transport'
    if is_complex_assembly(reaction, model):
        return 'complex assembly'
    # All reactions that are not transports or complex assemblies
    # are classified as biochemical reactions
    return 'biochemical reaction'
