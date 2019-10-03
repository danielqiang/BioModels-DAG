# Note: All code in this file is prototypical and therefore may be messy and
# informally documented at best. Methods and procedures will be refactored and formally
# documented before they are removed from prototype.py and added to the project.


import xml.etree.cElementTree as ET
import os
import csv
from collections import defaultdict
from pprint import pprint

from tools.xmltools import *
from tools.timeit import timeit
from tools.dict_to_csv import dict_to_csv


@timeit
def examine_multicompartment_models(path):
    counter = defaultdict(int)
    compartment_filemap = defaultdict(list)

    for filename in os.listdir("curated"):
        filepath = os.path.join(os.path.dirname(__file__), "curated", filename)
        # filepath = os.path.join(os.path.dirname(__file__), "curated", "BIOMD0000000490.xml")

        tree = ET.parse(filepath)

        compartments = etree_find(tree.getroot(), "listOfCompartments", ignore_namespaces=True)

        if compartments and len(list(compartments)) > 1:
            # if compartments:
            print(os.path.basename(filepath))

            for compartment in list(compartments):
                if 'name' in compartment.attrib:
                    compartment_name = compartment.attrib['name'].lower()
                    # print(compartment.attrib['name'])
                    counter[compartment_name] += 1
                    compartment_filemap[compartment_name].append(filename)
                elif 'id' in compartment.attrib:
                    compartment_id = compartment.attrib['id'].lower()
                    # print(compartment.attrib['id'])
                    counter[compartment_id] += 1
                    compartment_filemap[compartment_id].append(filename)
                else:
                    print("{} DOES NOT HAVE AN ASSOCIATED NAME OR ID.".format(compartment))
                # if 'id' in compartment.attrib and 'name' in compartment.attrib \
                #         and compartment.attrib['name'] != compartment.attrib['id']:
                #     print(filepath)
                #     print("{}'s NAME AND ID ATTRIBUTES DO NOT MATCH. NAME: {}. ID: {}".format(
                #         compartment, compartment.attrib['name'], compartment.attrib['id'])
                #     )
    print()
    sorted_iterator = sorted(compartment_filemap.items(), key=lambda entry: -len(entry[-1]))

    for k, v in sorted_iterator:
        print(k)
        print()
        for filename in v:
            print('\t' + filename)
        print()
    # sort compartment names by occurrence from greatest to least
    dict_to_csv(path, counter, ['Compartment Name', 'Occurrences'], sort_key=lambda entry: -entry[1])


def count_multicompartment_models():
    with open("MultiCompartmentModels.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        for filename in os.listdir("curated"):
            filepath = os.path.join(os.path.dirname(__file__), "curated", filename)

            root = ET.parse(filepath).getroot()

            compartments = etree_find(root, "listOfCompartments", ignore_namespaces=True)

            if compartments and len(list(compartments)) > 1:
                print(os.path.basename(filepath), len(list(compartments)))
                writer.writerow([os.path.basename(filepath), len(list(compartments))])


def count_derived_models():
    derived_models_count = 0
    for filename in os.listdir("curated"):
        filepath = os.path.join(os.path.dirname(__file__), "curated", filename)

        root = ET.parse(filepath).getroot()

        if etree_contains(root, "isDerivedFrom", ignore_namespaces=True):
            derived_models_count += 1
            print(filename)
    print(derived_models_count)


def main():
    path = r"C:\Users\danie\OneDrive\Professional\Biomedical Informatics Research Position" \
           r"\Project Files\compartments.csv"
    examine_multicompartment_models(path)
    # count_derived_models()


if __name__ == '__main__':
    main()
