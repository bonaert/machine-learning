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

def mostRestrictiveHypothesis(data):
    numColumns = len(data[0]) - 1
    hypothesis = [Special.NONE] * numColumns

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
            raise NoSolutionError("When looking at %s in %s with hypothesis %s" % (exampleValue, example, hypothesis))
            
    return hypothesis



        

