from data import *
from decisionTree import DecisionTree, getEntropyFromCounts
from math import log2
import unittest

class Outlook(Enum):
    Sunny = 0
    Overcast = 1
    Rain = 2

class Temperature(Enum):
    Hot = 0
    Cool = 1
    Mild = 2

class Humidity(Enum):
    High = 0
    Normal = 1

class Wind(Enum):
    Weak = 0
    Strong = 1

outlook = [Outlook.Sunny, Outlook.Sunny, Outlook.Overcast, Outlook.Rain, Outlook.Rain, Outlook.Rain, Outlook.Overcast, Outlook.Sunny, Outlook.Sunny, Outlook.Rain, Outlook.Sunny, Outlook.Overcast, Outlook.Overcast, Outlook.Rain]
temperature = [Temperature.Hot, Temperature.Hot, Temperature.Hot, Temperature.Mild, Temperature.Cool, Temperature.Cool, Temperature.Cool, Temperature.Mild, Temperature.Cool, Temperature.Mild, Temperature.Mild, Temperature.Mild, Temperature.Hot, Temperature.Mild]
humidity = [Humidity.High, Humidity.High, Humidity.High, Humidity.High, Humidity.Normal, Humidity.Normal, Humidity.Normal, Humidity.High, Humidity.Normal, Humidity.Normal, Humidity.Normal, Humidity.High, Humidity.Normal, Humidity.High]
wind = [Wind.Weak, Wind.Strong, Wind.Weak, Wind.Weak, Wind.Weak, Wind.Strong, Wind.Strong, Wind.Weak, Wind.Weak, Wind.Weak, Wind.Strong, Wind.Strong, Wind.Weak, Wind.Strong] 
playTennis = [Label.NO, Label.NO, Label.YES, Label.YES, Label.YES, Label.NO, Label.YES, Label.NO, Label.YES, Label.YES, Label.YES, Label.YES, Label.YES, Label.NO] 

complexData = list(zip(outlook, temperature, humidity, wind, playTennis))




class DecisionTreeTest(unittest.TestCase):
    def testSimpleCase(self):
        tree = DecisionTree()
        tree.fit(simpleData)
        
        for datum in simpleData:
            self.assertEqual(datum[-1], tree.predict(datum))

        tree.print()

    def testComplexCase(self):
        tree = DecisionTree()
        tree.fit(complexData)
        
        for datum in complexData:
            self.assertEqual(datum[-1], tree.predict(datum))

        # Overcast = YES
        self.assertEqual(Label.YES, tree.predict([Outlook.Overcast, Temperature.Hot, Humidity.High, Wind.Weak]))
        self.assertEqual(Label.YES, tree.predict([Outlook.Overcast, Temperature.Cool, Humidity.Normal, Wind.Strong]))
        
        # Sunny + Normal = YES
        self.assertEqual(Label.YES, tree.predict([Outlook.Sunny, Temperature.Cool, Humidity.Normal, Wind.Strong]))
        self.assertEqual(Label.YES, tree.predict([Outlook.Sunny, Temperature.Hot, Humidity.Normal, Wind.Weak]))

        # Sunny + High = NO
        self.assertEqual(Label.NO, tree.predict([Outlook.Sunny, Temperature.Cool, Humidity.High, Wind.Strong]))
        self.assertEqual(Label.NO, tree.predict([Outlook.Sunny, Temperature.Hot, Humidity.High, Wind.Weak]))

        # Rain + Weak = Yes
        self.assertEqual(Label.YES, tree.predict([Outlook.Rain, Temperature.Cool, Humidity.Normal, Wind.Weak]))
        self.assertEqual(Label.YES, tree.predict([Outlook.Rain, Temperature.Hot, Humidity.High, Wind.Weak]))

        # Rain + Strong = No
        self.assertEqual(Label.NO, tree.predict([Outlook.Rain, Temperature.Cool, Humidity.Normal, Wind.Strong]))
        self.assertEqual(Label.NO, tree.predict([Outlook.Rain, Temperature.Hot, Humidity.High, Wind.Strong]))




        tree.print()

    def testEntropy(self):
        self.assertEqual(0, getEntropyFromCounts([10, 0]))
        self.assertEqual(0, getEntropyFromCounts([0, 7, 0]))
        self.assertEqual(1, getEntropyFromCounts([20, 20]))
        self.assertAlmostEqual(-log2(1/3), getEntropyFromCounts([20, 20, 20]))
        self.assertAlmostEqual(-log2(1/4), getEntropyFromCounts([20, 20, 20, 20]))


