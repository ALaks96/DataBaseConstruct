import os
import json
import pandas as pd
from datetime import datetime


def get_arbo(path, ext=['ppt','pptx','docx','pdf','xlsx']):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(path)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(path, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_arbo(fullPath)
        else:
            if entry.endswith(tuple(ext)):
                allFiles.append(fullPath)
            else:
                continue

    return allFiles


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x


def to_json(dic, file_name="metadata.json"):
    js = json.dumps(dic, indent=1, cls=DateTimeEncoder)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + "/" + str(file_name), 'w')

    # write to json file
    fp.write(js)

    # close the connection
    fp.close()


def dic_for_viz(final_dic):
    collection = {}
    index = 1
    for doc, meta in final_dic.items():
        metadata = {}
        for key, value in final_dic[doc].items():
            if key != "Content":
                metadata[key] = value
        collection[index] = metadata
        index += 1

    return collection


def meta_to_df(final_dic, save=False):
    df = pd.DataFrame(dic_for_viz(final_dic))
    df = df.T
    if save:
        df.to_csv("Output/metadata.csv")

    return df