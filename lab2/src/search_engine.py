import re
import json

from common_elements import get_common_elements


def create_inverted_index(base_path, files):
    index = {}
    titles = {}

    for filename in files:

        file_data = {}

        with open(base_path + filename) as user_file:
            file_data = json.load(user_file)

        titles[filename] = file_data['title']

        sanitized_text = re.sub("\?|\.|\,|\n|-", ' ', file_data['text'])
        words = sanitized_text.split(' ')
        words = filter(len, words)

        for word in words:
            if len(word) > 0:
                if word not in index:
                    index[word] = []

                if filename not in index[word]:
                    index[word].append(filename)

    return (index, titles)


def search_inverted_index(index, keyword):
    result = index[keyword] if keyword in index else []
    return result


def search(index, input):
    result = []
    query_keywords = input.split(' ')

    for keyword in query_keywords:
        if keyword not in index:
            print("keyword %s was not found" % keyword)
            continue

        filenames = index[keyword]
        if len(result) == 0:
            result = filenames
            continue

        result = get_common_elements(result, filenames)
    return result


def format_search_result(filenames, titles):
    result = [["Title", "Filename"]]
    for filename in filenames:
        result.append([titles[filename],  filename])
    return result


def main():
    base_path = 'C:/Users/vlad/Desktop/study/iss/lab2/seeds/'
    files = ["data_1.json", "data_2.json", "data_3.json"]

    index, titles = create_inverted_index(base_path, files)

    while True:
        user_input = input("Enter keywords separated by space:\n")
        if len(user_input) < 1:
            break

        found_files = search(index, user_input)

        if len(found_files) > 0:
            result = format_search_result(found_files, titles)

            print()
            
            for line in result:
                print(*line)

            print()

        else:
            print("Files not found")


main()
