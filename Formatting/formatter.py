import os
import json
import pandas as pd
from datetime import datetime

def get_arbo(location, ext=['ppt','pptx','docx','pdf','xlsx']):
    # Initialize list of directories
    paths = []

    for file in os.listdir(location):
        if file.endswith(tuple(ext)):
            path = str(location) + "/" + str(file)
            paths.append(path)

    return paths


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


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