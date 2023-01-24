import unittest

import forward_index
import inverted_index


class ForwardIndexTest(unittest.TestCase):
    def test_forward_index_with_one_word(self):
        text = 'ship'
        result = forward_index.create_forward_index(text)
        self.assertEqual(result, ['ship'])

    def test_forward_index_multiple_words(self):
        text = 'The alien mothership is in orbit here'
        result = forward_index.create_forward_index(text)
        self.assertEqual(['alien', 'here', 'in', 'is',
                         'mothership', 'orbit', 'the'], result)

    def test_forward_index_empty(self):
        text = ''
        result = forward_index.create_forward_index(text)
        self.assertEqual(result, [])


class InvertedIndexTest(unittest.TestCase):
    def test_inverted_index_with_one_word(self):
        text = 'Seagull'
        index = {
            'jonathan': ['text1']
        }
        result = inverted_index.create_inverted_index(text, index, 'text2')
        self.assertEqual(result, {
            'seagull': ['text2'],
            'jonathan': ['text1']
        })

    def test_inverted_index_with_multiple_words(self):
        text = 'Jonathan was a seagull'
        index = {
            'seagull': ['text1']
        }
        result = inverted_index.create_inverted_index(text, index, 'text2')
        self.assertDictEqual(result, {
            'jonathan': ['text2'],
            'was': ['text2'],
            'a': ['text2'],
            'seagull': ['text1', 'text2']
        })

    def test_inverted_index_empty(self):
        text = ''
        result = {
            'livingston': ['text1']
        }
        inverted_index.create_inverted_index(text, result, 'text2')
        self.assertEqual(result, {
            'livingston': ['text1']
        })


class SearchForwardTest(unittest.TestCase):
    def test_search_forward_present_in_one(self):
        index = {
            'data_1': ['i', 'was', 'having', 'the', 'most', 'wonderful', 'dream'],
            'data_2': ['wow', 'you', 'got', 'that', 'off', 'the', 'internet']
        }
        result = forward_index.search_forward_index(index, 'internet')
        self.assertEqual(result, ['data_2'])

    def test_search_forward_present_in_many(self):
        index = {
            'data_1': ['a', 'superpowers', 'drug', 'you', 'can', 'just', 'rub', 'onto', 'your', 'skin'],
            'data_2': ['fry', 'you', 'can\'t', 'just', 'sit', 'here', 'in', 'the', 'dark', 'listening', 'to', 'classical', 'music']
        }
        result = forward_index.search_forward_index(index, 'just')
        self.assertEqual(result, ['data_1', 'data_2'])

    def test_search_forward_in_none(self):
        index = {
            'data_1': ['calculon', 'is', 'gonna', 'kill', 'us', 'and', 'it\'s', 'all', 'everybody', 'else\'s', 'fault'],
            'data_2': ['also' 'he' 'got' 'a' 'race' 'car'],
        }
        result = forward_index.search_forward_index(index, 'skin')
        self.assertEqual(result, [])


class SearchInvertedTest(unittest.TestCase):
    def test_search_inverted_present_in_one(self):
        index = {
            'bender': ['data_1'],
            'fry': ['data_2', 'data_2'],
        }
        result = inverted_index.search_inverted_index(index, 'bender')
        self.assertEqual(result, ['data_1'])

    def test_search_inverted_present_in_many(self):
        index = {
            'bender': ['data_1', 'data_2'],
            'fry': ['data_3', 'data_4'],
        }
        result = inverted_index.search_inverted_index(index, 'fry')
        self.assertEqual(result, ['data_3', 'data_4'])

    def test_search_inverted_in_none(self):
        index = {
            'bender': ['data_1', 'data_3'],
            'fry': ['data_1', 'data_2'],
        }
        result = inverted_index.search_inverted_index(index, 'gandhi')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
