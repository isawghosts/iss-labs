import copy
import json
import re
import sys


def create_inverted_index(text, existing_index, filename):
    inv_index = copy.deepcopy(existing_index) if existing_index else {}

    sanitized_text = re.sub("\?|\.|\,|\n|-", ' ', text)
    words = sanitized_text.split(' ')
    words = filter(len, words)

    for word in words:
        transformed_word = word.lower()
        if len(word) > 0:
            if transformed_word not in inv_index:
                inv_index[transformed_word] = []

            if filename not in inv_index[transformed_word]:
                inv_index[transformed_word].append(filename)

    return inv_index


def search_inverted_index(index, keyword):
    result = index[keyword] if keyword in index else []
    return result


if __name__ == "__main__":
    input_filenames = ['data_1.txt', 'data_2.txt', 'data_3.txt']
    output_filename = '../inverted_index.json'

    inverted_index_results = {}
    for filename in input_filenames:
        f = open('../seeds/' + filename, 'r')
        inverted_index_results = create_inverted_index(
            f.read(), inverted_index_results, filename)
        f.close()

    output = open(output_filename, 'w')
    output.write(json.dumps(inverted_index_results, indent=4))
    output.close()

    try:
        index_file = open(output_filename, 'r')
    except:
        raise "Inverted index was not found"

    index = json.loads(index_file.read())
    keywords = sys.argv[1:]
    for keyword in keywords:
        filenames = search_inverted_index(index, keyword)
        result = ', '.join(filenames)
        print(f'{keyword}: {result}')
