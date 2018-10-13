from findS import *
from unittest import TestCase
from data import *

assert getOtherValuesInEnum(Forecast.SAME) == [Forecast.CHANGE]
assert getOtherValuesInEnum(Forecast.CHANGE) == [Forecast.SAME]
assert getOtherValuesInEnum(Sky.CLOUDY) == [Sky.SUNNY, Sky.RAINY]


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

restr = mostRestrictiveHypothesis(simpleData)
assert restr == RESTRICTIVE_HYPOTHESIS
        
for example in simpleData:
    assert hypothesIsCoherentWithExample(RESTRICTIVE_HYPOTHESIS, example)

assert makeGeneralization([Temp.WARM, Wind.STRONG], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Wind.STRONG]
assert makeGeneralization([Temp.WARM, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Special.ANY]
assert makeGeneralization([Special.NONE, Special.NONE], [Temp.COLD, Wind.STRONG]) == [Temp.COLD, Wind.STRONG]
assert makeGeneralization([Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.STRONG]) == [Special.ANY, Special.ANY]
assert makeGeneralization([Special.ANY, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) == [Special.ANY, Wind.NORMAL]
assert makeGeneralization([Temp.COLD, Wind.NORMAL], [Temp.COLD, Wind.NORMAL]) == [Temp.COLD, Wind.NORMAL]


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


assert isNullHypothesis([Special.NONE])
assert not isNullHypothesis([Special.ANY])
assert not isNullHypothesis([Temp.WARM])
assert not isNullHypothesis([Temp.WARM, Wind.NORMAL, Special.ANY])
assert isNullHypothesis([Temp.WARM, Special.NONE, Wind.NORMAL, Special.ANY])


#
# Is More General
#

assert isMoreGeneral([Special.ANY], [Temp.WARM])
assert isMoreGeneral([Special.ANY], [Special.NONE])
assert isMoreGeneral([Temp.WARM], [Special.NONE])


assert not isMoreGeneral([Special.ANY], [Special.ANY])

assert not isMoreGeneral([Temp.WARM], [Temp.WARM])
assert not isMoreGeneral([Temp.COLD], [Temp.WARM])

assert not isMoreGeneral([Special.NONE], [Special.NONE])
assert not isMoreGeneral([Special.NONE], [Temp.COLD])
assert not isMoreGeneral([Special.NONE], [Special.ANY])

assert isMoreGeneral([Temp.WARM, Special.ANY], [Temp.WARM, Wind.NORMAL])

assert not isMoreGeneral([Temp.WARM, Wind.NORMAL], [Temp.WARM, Wind.NORMAL])
assert not isMoreGeneral([Special.NONE, Special.ANY], [Temp.WARM, Wind.NORMAL])



#
# Is More Specific
#

assert isMoreSpecific([Temp.WARM], [Special.ANY])
assert isMoreSpecific([Special.NONE], [Special.ANY])
assert isMoreSpecific([Special.NONE], [Temp.WARM])


assert not isMoreSpecific([Special.ANY], [Special.ANY])

assert not isMoreSpecific([Temp.WARM], [Temp.WARM])
assert not isMoreSpecific([Temp.WARM], [Temp.COLD])

assert not isMoreSpecific([Special.NONE], [Special.NONE])
assert not isMoreSpecific([Temp.COLD], [Special.NONE])
assert not isMoreSpecific([Special.ANY], [Special.NONE])

assert isMoreSpecific([Temp.WARM, Wind.NORMAL], [Temp.WARM, Special.ANY])

assert not isMoreSpecific([Temp.WARM, Wind.NORMAL], [Temp.WARM, Wind.NORMAL])
assert not isMoreSpecific([Temp.WARM, Wind.NORMAL], [Special.NONE, Special.ANY])


S, G = findSAndG(simpleData)
assert S == [[Sky.SUNNY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY]]
assert G == [[Sky.SUNNY, Special.ANY, Special.ANY, Special.ANY, Special.ANY, Special.ANY], [Special.ANY, Temp.WARM, Special.ANY, Special.ANY, Special.ANY, Special.ANY]]

sol = fetchAllHypothesis(simpleData)

#for x in sol:
#    print(x)

# The result is a permutation of
#  [
#    [Sky.SUNNY, Special.ANY, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY],
#    [Special.ANY, Temp.WARM, Special.ANY, Special.ANY, Special.ANY, Special.ANY],
#    [Sky.SUNNY, Temp.WARM, Special.ANY, Special.ANY, Special.ANY, Special.ANY],
#    [Sky.SUNNY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY],
#    [Special.ANY, Temp.WARM, Special.ANY, Wind.STRONG, Special.ANY, Special.ANY],
#    [Sky.SUNNY, Special.ANY, Special.ANY, Special.ANY, Special.ANY, Special.ANY]
#]



classifier = FindSClassifier()
classifier.fit(simpleData)
assert classifier.predict([
    Sky.CLOUDY, Temp.COLD, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME
]) == False

assert classifier.predict([
    Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME
]) == True

assert classifier.predict([
    Sky.RAINY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME
]) == False

assert classifier.predict([
    Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.NORMAL, Water.WARM, Forecast.SAME
]) == True