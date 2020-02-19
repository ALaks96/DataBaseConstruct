import unidecode

special_characters = ["@", "/", "#", ".", ",", "!", "?", "(", ")", "-", "_", "’", "'", "\"", ":", "=", "+", "&",
                          "`", "*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "'", '.', '‘', ';']
transformation_sc_dict = {initial: " " for initial in special_characters}


def filtering(s):
    s = unidecode.unidecode(s.lower().translate(str.maketrans(transformation_sc_dict)).strip())
    return s