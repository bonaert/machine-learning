from findS import Special, Label, hypothesisRespectsExample, mostRestrictiveHypothesis, fetchAllHypothesis, makeGeneralizations, makeSpecializations, getOtherValuesInEnum
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

assert getOtherValuesInEnum(Forecast.SAME) == [Forecast.CHANGE]
assert getOtherValuesInEnum(Forecast.CHANGE) == [Forecast.SAME]
assert getOtherValuesInEnum(Sky.CLOUDY) == [Sky.SUNNY, Sky.RAINY]

data = [
    [Sky.SUNNY, Temp.WARM, Humid.NORMAL, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.RAINY, Temp.COLD, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.CHANGE, Label.NO],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.COOL, Forecast.CHANGE, Label.YES],
]

RESTRICTIVE_HYPOTHESIS = [
    Sky.SUNNY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY
]

GENERAL_HYPOTHESIS = [
    [Sky.SUNNY, Special.ANY, Special.ANY, Special.ANY, Special.ANY, Special.ANY],
    [Special.ANY, Temp.WARM, Special.ANY, Special.ANY, Special.ANY, Special.ANY],
]

INTERMEDIATE_HYPOTHESIS = [
   [Sky.SUNNY, Special.ANY, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY],
    [Sky.SUNNY, Temp.WARM, Special.ANY, Special.ANY, Special.ANY, Special.ANY],
    [Special.ANY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY],
]

ALL_HYPOTHESES = [RESTRICTIVE_HYPOTHESIS] + GENERAL_HYPOTHESIS + INTERMEDIATE_HYPOTHESIS

restr = mostRestrictiveHypothesis(data)
assert restr == RESTRICTIVE_HYPOTHESIS
        
for example in data:
    assert hypothesisRespectsExample(RESTRICTIVE_HYPOTHESIS, example)

assert makeGeneralizations([Temp.WARM, Wind.STRONG], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Wind.STRONG]
assert makeGeneralizations([Temp.WARM, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Special.ANY]
assert makeGeneralizations([Special.NONE, Special.NONE], [Temp.COLD, Wind.STRONG]) == [Temp.COLD, Wind.STRONG]
assert makeGeneralizations([Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Special.ANY]
assert makeGeneralizations([Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) == [Special.ANY, Wind.NORMAL]
assert makeGeneralizations([Temp.COLD, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) == [Temp.COLD, Wind.NORMAL]


# TODO: improve testing because the returned list might be in any order
# I had to put the expected result in the right order for this to pass, and I shouldn't have to
assert makeSpecializations([Special.ANY, Special.ANY], [Temp.COLD, Wind.NORMAL]) == [
    [Temp.WARM, Special.ANY],
    [Special.ANY, Wind.STRONG]
]

assert makeSpecializations([Temp.WARM, Special.ANY], [Temp.WARM, Wind.NORMAL]) == [
    [Temp.WARM, Wind.STRONG]
]

assert makeSpecializations([Temp.WARM, Special.ANY, Water.COOL], [Temp.WARM, Wind.NORMAL, Water.COOL]) == [
    [Temp.WARM, Wind.STRONG, Water.COOL]
]

assert makeSpecializations([Special.ANY, Special.ANY, Water.COOL], [Temp.WARM, Wind.NORMAL, Water.COOL]) == [
    [Temp.COLD, Special.ANY, Water.COOL],
    [Special.ANY, Wind.STRONG, Water.COOL]
]





#assert mostGeneralHypothesis(data) == GENERAL_HYPOTHESIS
#assert fetchAllHypothesis(data) == ALL_HYPOTHESES
#assert makePrediction(hypotheses, newSituation) == PLAUSIBLE_PREDICTION