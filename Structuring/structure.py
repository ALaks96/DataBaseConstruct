from __future__ import print_function
import os
import json
from Matching.segmenter import recursive_items
from Matching.segmenter import get_annexes
from Matching.parser import make_dic
from Extracting.metadata_extractor import get_meta
from Extracting.text_extractor import get_text
from Formatting.formatter import get_arbo
from Formatting.formatter import to_json

def restructure(struct, parsed):
    for key, value in struct.items():
        if type(value) is dict:

            restructure(value, parsed)
        else:
            print(key)
            print(list(parsed.keys()))
            if key in parsed.keys():
                struct[key] = parsed[key]
    return struct


def annex_walker(path, struct_path="CANEVAS_STRUCT.json", save=True):
    # Define your structure in a json and input it as a parameter
    final_struct = json.load(open(struct_path))
    list_of_titles = recursive_items(final_struct)

    # Initiate mega dic containing everything
    megadic = {}
    index = 1

    # Get all OPORD in dir in any format (msoffice or pdf)
    arbo = get_arbo(path)

    for opord in arbo:
        # Initiate same key dic to be completed every time
        try:
            dic_of_files = {}

            # Get metadata of opord and assign it
            meta = get_meta(opord)
            dic_of_files['Title'] = meta['Title']
            dic_of_files['Author(s)'] = meta['Author(s)']
            dic_of_files['Last Modified By'] = meta['Last Modified By']
            dic_of_files['Created Date'] = meta['Created Date']
            dic_of_files['Modified Date'] = meta['Modified Date']
            dic_of_files['Location'] = opord

            # Extract text from opo 
            flat_text = get_text(opord)

            # Seperate annexes
            list_of_lists, annex_titles = get_annexes(flat_text)

            # Create flat dictionnary of opord
            flat_dic = make_dic(list_of_lists, annex_titles, list_of_titles)

            # Then restructure it from your definiton, respecting hierarchy and assign it to a field of our sub dic
            dic_of_annexes = {}
            for annex in flat_dic.keys():
                final_struct = json.load(open(struct_path))
                dic_of_annexes[str(annex)] = restructure(final_struct, flat_dic[str(annex)])
            dic_of_files["Content"] = dic_of_annexes

            # And assign all of this to our megadic, indexed by incremental numbers!
            megadic[str(index)] = dic_of_files
            index += 1
        except Exception as e:
            print("ERROR::", e, ':', os.path.basename(opord))

    if save:
        to_json(megadic, "scan.json")

    return megadic