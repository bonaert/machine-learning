from findS import Special, Label, hypothesisRespectsExample, mostRestrictiveHypothesis
from unittest import TestCase
from enum import Enum


class Sky(Enum):
    SUNNY = 0
    CLOUDY = 1
    RAINY = 2

class Temp(Enum):
    WARM = 0
    COLD = 1

class Humid(Enum):
    NORMAL = 0
    HIGH = 1

class Wind(Enum):
    STRONG = 0
    NORMAL = 1

class Water(Enum):
    WARM = 0
    COOL = 1

class Forecast(Enum):
    SAME = 0
    CHANGE = 1


data = [
    [Sky.SUNNY, Temp.WARM, Humid.NORMAL, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.RAINY, Temp.COLD, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.CHANGE, Label.NO],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.COOL, Forecast.CHANGE, Label.YES],
]

RESTRICTIVE_HYPOTHESIS = [
    Sky.SUNNY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY
]

restr = mostRestrictiveHypothesis(data)
assert restr == RESTRICTIVE_HYPOTHESIS
        
for example in data:
    assert hypothesisRespectsExample(RESTRICTIVE_HYPOTHESIS, example)

#assert mostGeneralHypothesis(data) == GENERAL_HYPOTHESIS
#assert fetchAllHypothesis(data) == ALL_HYPOTHESES
#assert makePrediction(hypotheses, newSituation) == PLAUSIBLE_PREDICTION