from data import *
from decisionTree import DecisionTree
import unittest

class DecisionTreeTest(unittest.TestCase):
    def testSimpleCase(self):
        tree = DecisionTree()
        tree.fit(simpleData)
        
        for datum in simpleData:
            self.assertEqual(datum[-1], tree.predict(datum))

# TODO: add much better tests