from enum import Enum
from constants import *

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

simpleData = [
    [Sky.SUNNY, Temp.WARM, Humid.NORMAL, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.SAME, Label.YES],
    [Sky.RAINY, Temp.COLD, Humid.HIGH, Wind.STRONG, Water.WARM, Forecast.CHANGE, Label.NO],
    [Sky.SUNNY, Temp.WARM, Humid.HIGH, Wind.STRONG, Water.COOL, Forecast.CHANGE, Label.YES],
]
