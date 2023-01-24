import json
import re
import sys


def create_forward_index(text):
    forward_index = []

    sanitized_text = re.sub("\?|\.|\,|\n|-", ' ', text)
    words = sanitized_text.split(' ')
    words = filter(len, words)

    for word in words:
        transformed_word = word.lower()
        if transformed_word not in forward_index:
            forward_index.append(transformed_word)

    forward_index.sort()
    return forward_index


def search_forward_index(index, keyword):
    filenames = []
    for fname in index:
        if keyword in index[fname]:
            filenames.append(fname)
    return filenames


if __name__ == "__main__":
    input_filenames = ['data_1.txt', 'data_2.txt', 'data_3.txt']
    output_filename = 'output/forward_index.json'
    
    forward_index_results = {}

    for filename in input_filenames:
        f = open('input/' + filename, 'r')
        forward_index_results[filename] = create_forward_index(f.read())
        f.close()

    output = open(output_filename, 'w')
    output.write(json.dumps(forward_index_results, indent=4))
    output.close()

    try:
        index_file = open(output_filename, 'r')
    except:
        raise "Forward index was not found"

    index = json.loads(index_file.read())
    keywords = sys.argv[1:]
    for keyword in keywords:
        filenames = search_forward_index(index, keyword)
        result = ', '.join(filenames)
        print(f'{keyword}: {result}')
