from BioModels import *
from BioModels.tools import timeit


@timeit
def main():
    import networkx
    import os

    filepaths = (os.path.join('curated', model) for model in os.listdir("curated"))

    # data = GraphDataBuilder(filepaths, parser=parse_derived_model).to_generator()
    # graph = build_graph(data)
    # networkx.write_graphml(graph, "data/derived_models.graphml")

    # Extracted using get_all_go_compartments("curated")
    all_compartments = {'mitochondrion', 'extraorganismal space', 'endoplasmic reticulum',
                        'obsolete intracellular part', 'sarcoplasmic reticulum', 'endosome lumen', 'endosome membrane',
                        'extracellular membrane-bounded organelle', 'cell', 'autophagosome', 'early phagosome',
                        'proteasome complex', 'spindle pole body', 'smooth endoplasmic reticulum', 'plasma membrane',
                        'DNA binding', 'glycosome', 'mitochondrial matrix', 'extracellular region',
                        'mitochondrial inner membrane', 'cytoplasmic side of plasma membrane', 'cytosol',
                        'mitochondrial intermembrane space', 'Golgi membrane', 'nucleus', 'lysosome', 'endosome',
                        'endoplasmic reticulum membrane', 'hepatocyte homeostasis', 'Golgi apparatus',
                        'extracellular space', 'membrane', 'cell surface', 'nuclear membrane', 'vesicle',
                        'chloroplast stroma', 'intracellular', 'cytoplasm'}

    data = GraphDataBuilder(filepaths,
                            parser=parse_mcmp_model,
                            preprocessed_data=all_compartments).to_generator()
    graph = build_graph(data)
    networkx.write_graphml(graph, "data/multicompartment_models.graphml")


if __name__ == '__main__':
    main()
