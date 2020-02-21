import json
import os
from PreProcessing.preprocess import filtering
from Extracting.text_extractor import get_l_of_l
from Matching.levsim import levenshtein

s = ['Exemplaire', 'PC', 'Référence', 'Fuseau horaire utilisé pour l\'ensemble de l\'ordre',
     'ARTICULATION', 'Situation',
     'Forces ennemies',
     'ENI actuel',
     'Possibilités de l\'ENI',
     'ENI futur',
     'Forces amies',
     'Renforcements et prélèvements',
     'Evaluation de la situation par le commandement',
     'Population',
     'MISSION',
     'EXECUTION',
     'Idée de manoeuvre',
     ]


def print_words_between(my_list, word1, word2, last=False):
    string = ""
    k, j, i1, i2 = 0, 0, 1000000, 1000000
    for node in my_list:
        j = j + 1
        if levenshtein(filtering(word1), filtering(node)) < 0.3:
            i1 = min(i1, j)
        if levenshtein(filtering(word2), filtering(node)) < 0.3:
            i2 = min(i2, j)

    for node in my_list:
        k = k + 1
        if last:
            i2 = 1000000000000
        if i1 < k < i2:
            string += node
    return string


def create_dict(which_list, list_stopwords):
    dict_stopwords = dict.fromkeys(list_stopwords, 0)
    length = len(list_stopwords)
    i = 0
    while i < length - 1:
        dict_stopwords[list_stopwords[i]] = print_words_between(which_list, list_stopwords[i], list_stopwords[i + 1])
        i = i + 1
    dict_stopwords[list_stopwords[length - 1]] = print_words_between(which_list, list_stopwords[length - 2],
                                                                     list_stopwords[length - 1], True)

    return dict_stopwords


def to_json(dic, file_name="metadata.json"):
    js = json.dumps(dic, indent=1)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + "/" + str(file_name), 'w')

    # write to json file
    fp.write(js)

    # close the connection
    fp.close()


def struct_dict(parsed_text, alt_annexes=False, annex_path=None):
    if alt_annexes:
        structure_json = json.load(open(annex_path))
        annex_titles = list(structure_json.keys())
    else:
        annex_path = os.getcwd() + '/Extracting/data/structure.json'
        structure_json = json.load(open(annex_path))
        annex_titles = list(structure_json.keys())
    try:
        dict_of_dicts = dict.fromkeys(annex_titles, 0)
        for i in range(len(parsed_text) - 1):
            dict_of_dicts[annex_titles[i]] = create_dict(parsed_text[i], s)
    except Exception as e:
        print(e)

    return dict_of_dicts


def opord_to_json(path, save=False):
    parsed_text = get_l_of_l(path)
    opord_dic = struct_dict(parsed_text)

    if save:
        to_json(opord_dic, file_name='parsed_opord.json')

    return opord_dic