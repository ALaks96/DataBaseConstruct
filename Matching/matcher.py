def annexe_splitter(s):
    new = s.split("ANNEXE")
    return new


def line_splitter(s):
    s = s.split("new")
    return s


def get_annex_titles(annexes):
    i = 0
    annex_titles = []
    for annex in annexes:
        title = annex[0].strip()
        if not title:
            if i < 1:
                i += 1
                title = "MAIN"
            else:
                title = annex[1].strip()
                if not title:
                    title = "OTHER"

        annex_titles.append(title)
    return annex_titles


def get_annexes(text):
    splitted = [line_splitter(annexe) for annexe in annexe_splitter(text)]
    titles = get_annex_titles(splitted)
    return splitted, titles