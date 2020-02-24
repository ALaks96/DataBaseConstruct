import os
from Structuring.structure import annex_walker

path = os.getcwd() + "/Extracting/data"
struct_path = os.getcwd() + "/CANEVAS_STRUCT.json"
annex_walker(path, struct_path, save=True)