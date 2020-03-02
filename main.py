import os
import sys
from Structuring.structure import annex_walker
from Formatting.formatter import meta_to_df
try:
    struct_path = os.getcwd() + "/CANEVAS_STRUCT.json"
except FileNotFoundError:
    print("Rename your structure to 'CANEVAS_STRUCT.json' and put at the root of the repo")

try:
    if sys.argv[1] == 'test':
        path = os.getcwd() + "/temp"
    elif sys.argv[1] == 'df':
        path = os.getcwd() + "/Data"
        structured_opord = annex_walker(path, struct_path, save=True)
        viz_df = meta_to_df(structured_opord, save=True)
    else:
        path = os.getcwd() + "/Data"
except IndexError:
    path = os.getcwd() + "/Data"

structured_opord = annex_walker(path, struct_path, save=True)

try:
    if sys.argv[2] == 'df':
        viz_df = meta_to_df(structured_opord, save=True)
except IndexError:
    pass