from ..bases import BaseParser
import re
import json
import libsbml


class BTOParser(BaseParser):
    def parser(self, sbml_file, **kwargs):
        from BioModelsETL.utils import extract_model_data

        with open("bto_lookup.json") as f:
            bto_lookup = json.load(f)

        pattern = re.compile("BTO:\d{7}")
        model_data = extract_model_data(sbml_file)
        model_data["color"] = "green"

        model = libsbml.readSBMLFromFile(sbml_file.name).getModel()
        for element in model.getListOfAllElements():
            for bto_id in pattern.findall(element.getAnnotationString()):
                if bto_id in bto_lookup:
                    yield model_data, "", {"name": bto_lookup[bto_id], "id": bto_id, "color": "red"}
                else:
                    print(f"BTO ID NOT FOUND: {bto_id}")
                    yield model_data, "", {"name": bto_id, "color": "red"}
