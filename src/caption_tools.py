from re import findall

def unique_words(words_as_list):
    result = []
    for word in words_as_list:
        if not word in result:
            result.append(word)
    return result


def optimize_caption(caption):
    words_as_list = findall(r"[A-Za-z0-9]+", caption)
    resulting_words = unique_words(words_as_list)
    return " ".join(resulting_words)