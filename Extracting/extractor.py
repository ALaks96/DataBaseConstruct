try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def annexe_splitter(s):
    new = s.split("ANNEXE")
    return new


def line_splitter(s):
    s = s.split("new")
    return s


def parser(path):
    s = ""
    zfile = zipfile.ZipFile(path)
    core_xml = XML(zfile.read('word/document.xml'))
    for paragraph in core_xml.getiterator(PARA):
        for node in paragraph.getiterator(TEXT):
            s += str("new" + node.text)
    return s


def get_l_of_l(path):
    splitted = [line_splitter(annexe) for annexe in annexe_splitter(parser(path))]
    return splitted