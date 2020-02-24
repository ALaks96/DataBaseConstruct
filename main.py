import os
from Structuring.structure import annex_walker
from Formatting.formatter import meta_to_df

path = os.getcwd() + "/Data"
struct_path = os.getcwd() + "/CANEVAS_STRUCT.json"
structured_opord = annex_walker(path, struct_path, save=True)
viz_df = meta_to_df(structured_opord, save=True)