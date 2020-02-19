import os
from Structuring.structure import opord_to_json

path = os.getcwd() + '/Extracting/data/Correction OPORD 20(AZ)DB.docx'
opord_to_json(path, save=True)