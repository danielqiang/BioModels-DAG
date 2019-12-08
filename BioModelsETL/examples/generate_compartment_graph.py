from BioModelsETL import *
from BioModelsETL.utils import timeit, yield_model_paths


@timeit
def main():
    import networkx

    filepaths = yield_model_paths()

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

    data = extract_data(filepaths,
                        parser=CompartmentParser(),
                        all_go_compartments=all_compartments,
                        skip_single_cmp_models=True)
    graph = build_graph(data)
    networkx.write_graphml(graph, "graphs/multicompartment_models.graphml")


if __name__ == '__main__':
    main()
