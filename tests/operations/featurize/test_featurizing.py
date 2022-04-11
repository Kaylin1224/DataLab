import unittest

from datalabs import load_dataset
from datalabs.operations.data import TextData
from datalabs.operations.featurize import general


class MyTestCase(unittest.TestCase):
    def test_Data_featurize(self):
        print("\n---- test_Data_featurize ---")

        a = [
            "I love this movie.",
            "apple is looking at buying U.K. startup for $1 billion.",
        ]
        A = TextData(a)

        B = A.apply(general.get_gender_bias)
        for b in B:
            print(b)

        B = A.apply(general.get_lexical_richness)
        for b in B:
            print(b)

        B = A.apply(general.get_basic_words)
        for b in B:
            print(b)


if __name__ == "__main__":
    unittest.main()
