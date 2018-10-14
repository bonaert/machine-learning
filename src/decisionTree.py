from math import log2
from typing import List, Union
from collections import defaultdict
from constants import * 


def getEntropyFromCounts(counts):
    # Remove 0 counts
    counts = [count for count in counts if count > 0]
    assert len(counts) > 0
    
    if len(counts) == 1: # Only one possible outcome
        return 0

    total = sum(counts)
    entropy = 0
    for count in counts:
        p = count / total
        entropy -= p * log2(p)
    
    return entropy


class Node:
    pass

class LeafNode(Node):
    def __init__(self, parent, value, label):
        self.label = label
        self.parent = parent
        self.value = value

    def isLeaf(self) -> bool:
        return True
    
    def print(self, tabs=0):
        enumName = self.value.__class__.__name__  # Sky
        enumValue = str(self.value).split('.')[1] # Sky.Sunny -> Sunny
        labelValue = str(self.label).split('.')[1]
        print("%sColumn %d: %s = %s -> Label = %s" % ('| ' * tabs, self.parent.columnIndex, enumName, enumValue, labelValue))

class DecisionNode(Node):
    def __init__(self, parent, value, data):
        self.data = data
        self.parent = parent
        self.value = value # TODO: find better name
        self.children = {}        
        self.columnIndex = None
    
    def getNumColumns(self):
        return len(self.data[0]) - 1

    def getUsedColumns(self):
        """
        Returns all the columns that were used to categorise data, from the root to the 
        current node.
        Example: Temperature (attribute 3) -> Wind (attribute 0) -> Humidity (attribute 1)
        Return: [3, 0, 1]
        """
        result = []
        node = self.parent
        while node:
            result.append(node.columnIndex)
            node = node.parent
            
        return result
    
    def getUnusedColumns(self):
        usedColumns = self.getUsedColumns()
        return [index for index in range(self.getNumColumns()) if index not in usedColumns]
        

    def isLeaf(self) -> bool:
        return False

    def goToAppropriateChild(self, example):
        value = example[self.columnIndex]
        return self.children[value]

    
    def getColumnStatistics(self, columnIndex):
        """
        Returns the statistic for the given column.
        
        Example where we get the statistic for Temperature:
        Returns:
        {
            Temp.COLD: {Label.Yes: 7, Label.No: 6},
            Temp.MEDIUM: {Label.Yes: 2, Label.No: 10},
            Temp.HOT: {Label.Yes: 10, Label.No: 3},
        }
        """
        counter = {}
        for datum in self.data:
            value, label = datum[columnIndex], datum[-1]
            if value not in counter:
                counter[value] = {Label.YES: 0, Label.NO: 0}

            counter[value][label] += 1

        return counter
    
    def getEntropy(self):
        counts = self.countColumnCount(self.columnIndex)
        total = len(self.data)
        probabilities = [count / total for count in counts]
        entropy = sum(p * math.log2(p) for p in probabilities)


    def getPossibleValuesOfColumn(self, columnIndex):
        return self.data[0][columnIndex].__class__.__members__

    def getAllDataWithValue(self, value):
        return [x for x in self.data if x[self.columnIndex] == value]


    def split(self, columnIndex):
        """
        Splits the decision node, creating a new subnode for each possible value of Column.
        
        Example: if column is Wind[None, Normal, Strong], then we create 3 sub-nodes, one
        for None, one for Normal, one for Strong. 
        Each newly-created subnode will receving the data concerning it: 
        - The None   sub-node will receive all the data that have Wind = None
        - The Normal sub-node will receive all the data that have Wind = Normal
        - The Strong sub-node will receive all the data that have Wind = Strong

        If all the data of a sub-node have the same label (Yes/No), we created a LeafNode 
        with that label. Otherwise, we created a new DecisionNode (that can be split later).

        Returns the newly-created sub-nodes.
        """
        assert len(self.children) == 0 and self.columnIndex is None, "Already split!"
        self.columnIndex = columnIndex

        for value in self.getPossibleValuesOfColumn(columnIndex).values():
            childData = self.getAllDataWithValue(value)
            labels = [x[-1] for x in childData]
            numLabels = len(set(labels))
            
            if numLabels == 0:
                continue
                #raise Exception("No instances for attribute %s %s!" % (value.__class__, value))
            elif numLabels == 1: # Only one label
                newNode = LeafNode(parent=self, value=value, label=childData[0][-1])
            else:
                newNode = DecisionNode(parent=self, value=value, data=childData)
            
            self.children[value] = newNode
        
        return self.children.values()

    def getLabelDistributions(self):
        """
        Returns a tuple with four elements:
            - the number of data with Label=Yes
            - the number of data with Label=No
            - the percent of data with Label=Yes
            - the percent of data with Label=No
        
        Example: (833, 167, 0.83, 0.17)
        """
        total = len(self.data)
        plus = len([x for x in self.data if x[-1] == Label.YES])
        minus = total - plus
        percentPlus, percentMinus = plus / total, minus / total
        return plus, minus, percentPlus, percentMinus
    
    def print(self, tabs=0):
        plus, minus, percentPlus, percentMinus = self.getLabelDistributions()

        if self.value is None:
            # [833+, 167-] 0.83+ 0.17-
            print("%s[%d+, %d-] %.2f+ %.2f-" % ('| ' * tabs, plus, minus, percentPlus, percentMinus))
        else:
            # Column 0: Sky = High [833+, 167-] 0.83+ 0.17-
            enumName = self.value.__class__.__name__  # Sky
            enumValue = str(self.value).split('.')[1] # Sky.Sunny -> Sunny
            print("%sColumn %d: %s = %s  [%d+, %d-] %.2f+ %.2f-" % 
                ('| ' * tabs, self.parent.columnIndex, enumName, enumValue, plus, minus, percentPlus, percentMinus)
            )
        
        for child in self.children.values():
            child.print(tabs + 1)

    

class DecisionTree:
    def fit(self, data):
        """
        Builds the decision tree, by splitting each node until only leafs nodes 
        (with Yes/No) labels remain. We split each node so that it maximises information
        gain. The criterion used is entropy (e.g. as in information theory)
        """
        self.tree = DecisionNode(parent=None, value=None, data=data)
        toSplit = [self.tree]
        while toSplit:
            currentNode = toSplit.pop()
            column = self.findBestColumnToSplit(currentNode)
            children = currentNode.split(column)

            toSplit.extend([x for x in children if not x.isLeaf()])

    def findBestColumnToSplit(self, node: DecisionNode):
        """ 
        Decides which column should be used to split the node. The goal is to choose
        the column that maximizes the information gain. The information gain is 
        computed using the following formula:

        Gain(S, A) = Entropy(S) -     sum         [(count(Sv) / count(data)) * entropy(Sv)]
                                (v in column.values) 

        where Sv is the data that has columnValue=v.

        Finding the A that maximizes Gain(S, A) is equivalent to find the A that minimizes
               sum            [count(Sv) * entropy(Sv)]
        (v in column.values)         
        """
        unusedColumns = node.getUnusedColumns()

        bestScore, bestColumn = None, None
        for column in unusedColumns:
            statistics = node.getColumnStatistics(column)
            score = 0
            total = 0
            for value, counts in statistics.items():
                total = counts[Label.YES] + counts[Label.NO]
                entropy = getEntropyFromCounts(counts.values())
                score += total * entropy
            
            if bestScore is None or score < bestScore:
                bestScore, bestColumn = score, column
        
        return bestColumn
    
    def predict(self, example):
        """
        Predicts the label for the given example, by walking down the tree until we hit
        a leaf node (e.g. with a Yes/No label). Returns the label.
        """
        node = self.tree
        while not node.isLeaf():
            node = node.goToAppropriateChild(example)
        
        return node.label
    
    def print(self):
        self.tree.print()
    

# TODO: add visualisation