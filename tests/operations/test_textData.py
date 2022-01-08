import unittest
import datasets
from data import Data, TextData


"""
from datasets.operations.edit.core import add_typos_checklist
from datasets import load_dataset
dataset = load_dataset("ag_news")
dataset["test"].apply(add_typos_checklist)



from datasets.operations.featurize.text_classification import get_length
from datasets import load_dataset
dataset = load_dataset("ag_news")
res = dataset["test"].apply(get_length)


"""

class MyTestCase(unittest.TestCase):

    def test_Data(self):
        a = ['I love this movie', 'do you love this movie']
        A = Data(a)
        print(A.data)


        self.assertEqual(A.name, "Data")
        self.assertEqual(A.data, a)


    def test_TextData(self):
        a = ['I love this movie', 'do you love this movie']
        A = TextData(a)
        print(A.data)


        self.assertEqual(A.name, "textData")
        self.assertEqual(A.data, [{"text":text} for text in a])
if __name__ == '__main__':
    unittest.main()
