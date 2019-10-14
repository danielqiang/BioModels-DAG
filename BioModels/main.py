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
    all_compartments = {'vesicle', 'glycosome', 'Golgi apparatus', 'endoplasmic reticulum',
                        'sarcoplasmic reticulum', 'hepatocyte homeostasis', 'cytoplasm',
                        'early phagosome', 'smooth endoplasmic reticulum', 'endosome lumen',
                        'extracellular region', 'autophagosome', 'nucleus', 'mitochondrial matrix',
                        'obsolete intracellular part', 'cell', 'extraorganismal space',
                        'extracellular membrane-bounded organelle', 'endosome membrane', 'membrane',
                        'lysosome', 'endosome', 'proteasome complex', 'intracellular',
                        'cytoplasmic side of plasma membrane', 'endoplasmic reticulum membrane',
                        'DNA binding', 'cell surface', 'mitochondrion', 'spindle pole body',
                        'plasma membrane', 'chloroplast stroma', 'Golgi membrane',
                        'mitochondrial intermembrane space', 'extracellular space',
                        'nuclear membrane', 'mitochondrial inner membrane', 'cytosol'}

    # data = GraphDataBuilder(filepaths,
    #                         parser=parse_mcmp_model,
    #                         preprocessed_data=all_compartments).to_generator()
    # graph = build_graph(data)
    # networkx.write_graphml(graph, "data/multicompartment_models.graphml")
    print(all_compartments)


if __name__ == '__main__':
    main()
