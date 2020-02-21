from __future__ import print_function
import string
import unidecode
from ftfy import fix_encoding

special_characters = ["@", "/", "#", ".", ",", "!", "?", "(", ")", "-", "_", "’", "'", "\"", ":", "=", "+", "&",
                          "`", "*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "'", '.', '‘', ';']
transformation_sc_dict = {initial: " " for initial in special_characters}


def correct_ascii(text):
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))

    return text


def fix_text(text, decoding=False):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\u2013", "-")
    text = text.replace("\u03d5", "ϕ")
    text = text.rstrip("\n")
    text = text.rstrip("\t")
    if decoding:
        text = fix_encoding(text)
        text = unidecode.unidecode(text)
        text = correct_ascii(text)

    return text


def filtering(s):
    s = unidecode.unidecode(s.lower().translate(str.maketrans(transformation_sc_dict)).strip())
    return s