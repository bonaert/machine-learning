from enum import Enum

class Special(Enum):
    NONE = 0
    ANY = 1

class Label(Enum):
    NO = 0
    YES = 1


class NoSolutionError(Exception):
    pass

class LogicError(Exception):
    pass


def hypothesisRespectsExample(hypothesis, example):
    assert len(hypothesis) == len(example) - 1
    
    prediction = Label.YES
    for hypothesisValue, exampleValue in zip(hypothesis, example):
        if hypothesisValue == Special.ANY:
            continue
        elif hypothesisValue == Special.NONE or hypothesisValue != exampleValue:
            prediction = Label.NO
            break
    
    label = example[-1]
    return prediction == label

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
        elif label == Label.NO and not hypothesisRespectsExample(hypothesis, example):
            raise NoSolutionError("When looking at %s with hypothesis %s" % (example, hypothesis))
            
    return hypothesis



def makeGeneralizations(hyp, example):
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







    

def existsMoreGeneralHypothesis(hyp, collection):
    pass

def existsMoreSpecificHypothesis(hyp, collection):
    pass

def removeTooGeneralHypothesis(collection):
    pass

def removeTooSpecificHypothesis(collection):
    pass


def findSAndG(data):
    numFields = getNumFields(data)
    S = [[Special.NONE] * numFields]
    G = [[Special.ANY] * numFields]
    for example in data:
        label = example[-1]

        if label == Label.YES:
            G = [hyp for hyp in G if hypothesisRespectsExample(hyp, example)]

            newS = []
            for hyp in S:
                if hypothesisRespectsExample(hyp, example):
                    newS.append(hyp)
                    continue
                
                newS += [new for new in makeGeneralizations(hyp, example) if existMoreGeneralHypothesis(new, G)]

            S = removeTooGeneralHypothesis(newS)


        else: # Label.NO
            
            S = [hyp for hyp in S if hypothesisRespectsExample(hyp, example)]

            newG = []
            for hyp in G:
                if hypothesisRespectsExample(hyp, example):
                    newG.append(hyp)
                    continue
                
                newG += [new for new in makeSpecializations(hyp, example) if existMoreSpecificHypothesis(new, S)]

            G = removeTooSpecificHypothesis(newG)
    
    return S, G


def fetchAllHypothesis(data):
    S, G = findSAndG(data)
    return createAllHypotheses(S, G)