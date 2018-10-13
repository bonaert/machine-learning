from constants import *


class NoSolutionError(Exception):
    pass

class LogicError(Exception):
    pass

def getPrediction(hypothesis, example):
    prediction = Label.YES
    for hypothesisValue, exampleValue in zip(hypothesis, example):
        if hypothesisValue == Special.ANY:
            continue
        elif hypothesisValue == Special.NONE or hypothesisValue != exampleValue:
            prediction = Label.NO
            break

    return prediction

def hypothesIsCoherentWithExample(hypothesis, example):
    assert len(hypothesis) == len(example) - 1
    label = example[-1]
    return getPrediction(hypothesis, example) == label

def getNumFields(data):
    return len(data[0]) - 1

def mostRestrictiveHypothesis(data):
    numFields = getNumFields(data)
    hypothesis = [Special.NONE] * numFields

    for example in data:
        label = example[-1]

        if label == Label.YES:
            for index in range(len(example) - 1):
                exampleValue, hypothesisValue = example[index], hypothesis[index]
                if hypothesisValue == Special.NONE:
                    hypothesis[index] = exampleValue
                elif hypothesisValue != Special.ANY and hypothesisValue != exampleValue:
                    hypothesis[index] = Special.ANY
        elif label == Label.NO and not hypothesIsCoherentWithExample(hypothesis, example):
            raise NoSolutionError("When looking at %s with hypothesis %s" % (example, hypothesis))
            
    return hypothesis



def makeGeneralization(hyp, example):
    """
    Given a hypothesis that is not coherent with the given (positive) example, returns
    the smallest generalization of the hypothesis that is coherent with the (positive) example.

    Examples:
    [Temp.WARM, Wind.STRONG], [Temp.COLD, Wind.STRONG]) -> [[Special.ANY, Wind.STRONG]]
    [Temp.WARM, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) -> [[Special.ANY, Special.ANY]]
    [Special.NONE, Special.NONE], [Temp.COLD, Wind.STRONG]) -> [[Temp.COLD, Wind.STRONG]]
    [Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) -> [[Special.ANY, Special.ANY]]
    [Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) -> [[Special.ANY, Wind.NORMAL]]
    [Temp.COLD, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) -> [[Temp.COLD, Wind.NORMAL]]
    """
    newHyp = []
    for i in range(len(hyp)):
        hypValue, exampleValue = hyp[i], example[i]
        
        if hypValue == Special.ANY:
            newHyp.append(Special.ANY)
        elif hypValue == Special.NONE:
            newHyp.append(exampleValue)
        elif hypValue == exampleValue:
            newHyp.append(exampleValue)
        else:
            newHyp.append(Special.ANY)
    
    return newHyp
    
def getOtherValuesInEnum(value):
    """
    Given a value V of an Enum X, returns all the other values in the Enum except V.

    Example:
    X = Enum([Cold, Hot, Normal])
    V = Hot
    returns [Cold, Normal]
    """
    enumClass = list(value.__class__)
    return [x for x in enumClass if x != value]


def makeSpecializations(hyp, incoherentExample):
    """
    Given a hypothesis H that is not coherent with a negative example, returns the (one or more)
    smallest specialisations of H that are coherent with the negative example.

    Examples:
    [Special.ANY, Special.ANY], [Temp.COLD, Wind.NORMAL]) -> [
        [Special.ANY, Wind.STRONG],
        [Temp.WARM, Special.ANY]
    ]

    [Temp.WARM, Special.ANY], [Temp.WARM, Wind.NORMAL] -> [
        [Temp.WARM, Wind.STRONG]
    ]

    [Temp.WARM, Special.ANY, Water.COOL], [Temp.WARM, Wind.NORMAL, Water.COOL] -> [
        [Temp.WARM, Wind.STRONG, Water.COOL]
    ]

    [Special.ANY, Special.ANY, Water.COOL], [Temp.WARM, Wind.NORMAL, Water.COOL] -> [
        [Special.ANY, Wind.STRONG, Water.COOL],
        [Temp.COLD, Special.ANY, Water.COOL]
    ]
    """
    newHypotheses = []
    if Special.NONE in hyp:
        raise LogicError("Cannot specialize the null hypothesis: %s" % hyp)

    # For each Special.ANY attribute in the hypothesis corresponding 
    # to an attribute X of value V (for example, X = Wind and V = Strong) in the negative example,
    # we can put replace it by any value of X except V (V = Weak, V = Normal)
    # We need the schema here!

    for i in range(len(hyp)):  
        hypValue, exampleValue = hyp[i], incoherentExample[i]
        if hypValue == Special.ANY:
            for otherValue in getOtherValuesInEnum(exampleValue):
                newHypothesis = hyp[:]
                newHypothesis[i] = otherValue
                newHypotheses.append(newHypothesis)
        elif hypValue != exampleValue: # We know hypValue is neither Special.NONE nor Special.ANY
            raise LogicError("No need to generalize, the hypothesis %s is already incoherent with the example %s" % (hyp, example))
            
    
    return newHypotheses



def isNullHypothesis(hyp):
    return any([x == Special.NONE for x in hyp])

def isMoreGeneral(hyp1, hyp2):
    assert len(hyp1) == len(hyp2)
    
    oneAttributeIsMoreGeneral = False
    for (val1, val2) in zip(hyp1, hyp2):
        if val1 == Special.NONE and val2 == Special.NONE: # (None, None)
            return False
        elif val1 == val2: # (a, a) or (Any, Any)
            continue
        elif val2 == Special.NONE: # (a/Any, None)
            oneAttributeIsMoreGeneral = True
        elif val1 == Special.NONE: # (None, a/Any)
            return False
        elif val1 == Special.ANY:  # (Any, a)
            oneAttributeIsMoreGeneral = True
        else: # (a, Any)
            return False
            
    return oneAttributeIsMoreGeneral

def isMoreSpecific(hyp1, hyp2):

    assert len(hyp1) == len(hyp2)

    oneAttributeIsMoreSpecific = False
    for (val1, val2) in zip(hyp1, hyp2):
        if val2 == Special.NONE: # (X, None) 
            return False # Impossible to more specific than the null hypothesis
        elif val1 == val2: # (a, a) or (Any, Any)
            continue
        elif val1 == Special.NONE: # (None, a/Any)
            oneAttributeIsMoreSpecific = True
        elif val1 == Special.ANY:  # (Any, a)
            return False
        elif val2 == Special.ANY: # (a, Any)
            oneAttributeIsMoreSpecific = True
        else: # (a, b)
            return False
    
    return oneAttributeIsMoreSpecific

def existsMoreGeneralHypothesis(hyp, collection):
    return any((isMoreGeneral(x, hyp) for x in collection))

def existsMoreSpecificHypothesis(hyp, collection):
    return any((isMoreSpecific(x, hyp) for x in collection))



def removeTooGeneralHypothesis(collection):
    """
    Remove from S any hypothesis that is more general than another hypothesis in S
    """
    result = []
    for i in range(len(collection)):
        isGood = True

        for j in range(len(collection)):
            if i == j:
                pass
            
            if isMoreGeneral(collection[i], collection[j]):
                isGood = False
                break
        
        if isGood:
            result.append(collection[i])
    
    return result
            


def removeTooSpecificHypothesis(collection):
    """
    Remove from S any hypothesis that is more general than another hypothesis in S
    """
    result = []
    for i in range(len(collection)):
        isGood = True

        for j in range(len(collection)):
            if i == j:
                pass
            
            if isMoreSpecific(collection[i], collection[j]):
                isGood = False
                break
        
        if isGood:
            result.append(collection[i])
    
    return result


def findSAndG(data):
    numFields = getNumFields(data)
    S = [[Special.NONE] * numFields]
    G = [[Special.ANY] * numFields]
    for example in data:
        label = example[-1]

        if label == Label.YES:
            G = [hyp for hyp in G if hypothesIsCoherentWithExample(hyp, example)]

            newS = []
            for hyp in S:
                if hypothesIsCoherentWithExample(hyp, example):
                    newS.append(hyp)
                    continue
                
                
                generalization = makeGeneralization(hyp, example)
                if existsMoreGeneralHypothesis(generalization, G):
                    newS.append(generalization)
                

            # Remove from S any hypothesis that is more general than another hypothesis in S
            S = removeTooGeneralHypothesis(newS)


        else: # Label.NO
            
            S = [hyp for hyp in S if hypothesIsCoherentWithExample(hyp, example)]

            newG = []
            for hyp in G:
                if hypothesIsCoherentWithExample(hyp, example):
                    newG.append(hyp)
                    continue
                

                newG += [x for x in makeSpecializations(hyp, example) if existsMoreSpecificHypothesis(x, S)]

            G = removeTooSpecificHypothesis(newG)
    
    return S, G

def specializeNearS(hyp, S):
    """
    Given a hypothesis and a lower bound hypothesis S, we give all specializations of hyp 
    towards S that can be made by changing a single element of the hypothesis
    Note:  We suppoose that S isn't the null hypothesis, e.g. there are no Special.NONE in S
    """

    new = []
    for i in range(len(hyp)):
        hypValue, sValue = hyp[i], S[i]
        
        # Can specialize: (Any, a)
        # Can't specialize: (Any, Any), (a, a)
        if hypValue != sValue:
            copy = hyp[:]
            copy[i] = sValue
            new.append(copy)
    
    return new
            


def createAllHypotheses(S, G):
    """
    Returns [S] + G + all hypothesis H such that S is more general than H and
    there's a hypothesis in G that's more general than H
    """
    S = S[0] # TODO: fix this, currently S is treated like a collection, when it's in really a single hypothesis
    solutions = set([tuple(S)])
    toExplore = set(map(tuple, G))
    while toExplore:
        hyp = list(toExplore.pop())

        solutions.add(tuple(hyp))

        for specialization in specializeNearS(hyp, S):
            if tuple(specialization) not in solutions:
                toExplore.add(tuple(specialization))
     
    return [list(x) for x in solutions]


def fetchAllHypothesis(data):
    S, G = findSAndG(data)
    return createAllHypotheses(S, G)


class FindSClassifier:
    def fit(self, data):
        self.hypotheses = fetchAllHypothesis(data)
    
    def predict(self, example):
        positive, negative = 0, 0
        for hypothesis in self.hypotheses:
            if getPrediction(hypothesis, example) == Label.YES:
                positive += 1
            else:
                negative += 1
    
        return positive >= negative