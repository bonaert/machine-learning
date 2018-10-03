from enum import Enum

class Special(Enum):
    NONE = 0
    ANY = 1

class Label(Enum):
    NO = 0
    YES = 1


class NoSolutionError(Exception):
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
    

def makeSpecializations(hyp, example):
    pass

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