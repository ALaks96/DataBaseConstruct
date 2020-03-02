from PreProcessing.preprocess import filtering
from fuzzywuzzy import fuzz


def print_words_between(my_list, word1, word2, last=False, fuzzy=True, thresh=50):
    string = ""
    k, j, i1, i2 = 0, 0, 1000000, 1000000
    for node in my_list:
        j = j + 1
        if fuzzy:
            if fuzz.token_sort_ratio(filtering(word1), filtering(node)) > thresh:
                i1 = min(i1, j)
            if fuzz.token_sort_ratio(filtering(word2), filtering(node)) > thresh:
                i2 = min(i2, j)
        else:
            if filtering(word1) in filtering(node):
                i1 = min(i1, j)
            if filtering(word2) in filtering(node):
                i2 = min(i2, j)

    for node in my_list:
        k = k + 1
        if last:
            i2 = 1000000000000
        if i1 < k < i2:
            string += node
    return string


def create_dict(which_list, list_stopwords, fuzzy=True, thresh=50):
    dict_stopwords = dict.fromkeys(list_stopwords, 0)
    length = len(list_stopwords)
    i = 0
    while i < length - 1:
        try:
            elem = print_words_between(which_list, list_stopwords[i], list_stopwords[i + 1], False, fuzzy=fuzzy, thresh=thresh)
            if elem:
                dict_stopwords[list_stopwords[i]] = elem
            else:
                dict_stopwords[list_stopwords[i]] = "title not found"
            i = i + 1
        except Exception:
            dict_stopwords[list_stopwords[i]] = print_words_between(which_list, list_stopwords[i], list_stopwords[i + 1], False, fuzzy=fuzzy, thresh=thresh)

    try:
        last_elem = print_words_between(which_list, list_stopwords[length - 2],
                                        list_stopwords[length - 1], True, fuzzy=fuzzy, thresh=thresh)
        if last_elem:
            dict_stopwords[list_stopwords[length - 1]] = last_elem
        else:
            dict_stopwords[list_stopwords[length - 1]] = "title not found"
    except Exception:
        dict_stopwords[list_stopwords[length - 1]] = print_words_between(which_list, list_stopwords[length - 2],
                                        list_stopwords[length - 1], True, fuzzy=fuzzy, thresh=thresh)


    return dict_stopwords


def make_dic(parsed_text, annexes, list_of_titles, fuzzy=True, thresh=50):
    try:
        dict_of_dicts = dict.fromkeys(annexes, 0)
        for i in range(len(parsed_text)):
            dict_of_dicts[annexes[i]] = create_dict(parsed_text[i], list_of_titles, fuzzy=fuzzy, thresh=thresh)
    except Exception as e:
        print(e)

    return dict_of_dicts

def conformity_stat(flat_dic):
    list_title_empty = []
    list_content_empty = []
    list_total = []
    for title in list(flat_dic.keys()):
        list_title_empty.append(len(list(i for i in list(flat_dic[title].values()) if i == '')))
        list_content_empty.append(len(list(i for i in list(flat_dic[title].values()) if i == 'title not found')))
        list_total.append(len(list(flat_dic[title].values())))
    part_empty = (sum(list_content_empty)/2 + sum(list_title_empty))/sum(list_total)
    return 1-part_empty