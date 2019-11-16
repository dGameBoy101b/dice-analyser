from modifier import Modifier
from dice_pool import Dice
from roll_part_base import RollPart

class PartSum():
    PART_SEP = ' '
    RES_SEP = '='
    GROUP_START = '('
    GROUP_END = ')'
    
    def __init__(self, parts: list):
        if not isinstance(parts, list):
            raise TypeError('\'parts\' must be a list, not a ' +str(type(parts)))
        for part in parts:
            if not issubclass(type(part), RollPart):
                raise TypeError('every element in \'parts\' must be a subclass of RollPart, not ' + str(type(part)))
        self.parts = parts
        return

    def __repr__(self) -> str:
        '''Convert this roll part list to a machine exacutable string.

    This should create an exact copy of this roll part list when executed.'''
        return 'PartSum(' + repr(self.parts) + ')'

    def __str__(self):
        string = ''
        for part in self.parts:
            string += str(part)
        return string

    def __eq__(self, other) -> bool:
        '''Determin whether this roll part list is equal to another.'''
        if not isinstance(other, PartSum):
            raise TypeError('PartSum objects must be compared to other Partsum objects.')
        return self.parts == other.parts

    def sumParts(self, parts_given) -> float:
        '''Return the sum of all items in given list.'''
        parts = parts_given.copy()
        for i in range(len(parts)):
            parts[i] = sum(parts[i])
        return sum(parts)
    
    def min(self) -> ([[int]],int):
        '''Return all minimum components and their sum.'''
        minimum = self.parts.copy()
        for i in range(len(minimum)):
            minimum[i] = minimum[i].min()
        return (minimum, self.sumParts(minimum))

    def max(self) -> ([[int]],int):
        '''Return all maximum components and their sum.'''
        maximum = self.parts.copy()
        for i in range(len(maximum)):
            maximum[i] = maximum[i].max()
        return (maximum, self.sumParts(maximum))

    def avg(self) -> ([[float]],float):
        '''Return all average components and their sum.'''
        average = self.parts.copy()
        for i in range(len(average)):
            average[i] = average[i].avg()
        return (average, self.sumParts(average))

    def rand(self) -> ([[int]],int):
        '''Return all random components and their sum.'''
        random = self.parts.copy()
        for i in range(len(random)):
            random[i] = random[i].rand()
        return (random, self.sumParts(random))

    def string(self, parts: [[float]]) -> str:
        '''Return the string formula of the given parts.'''
        sum_parts = parts[0]
        string = str(sum_parts)
        string = string.replace(', ', PartSum.PART_SEP + RollPart.POS + PartSum.PART_SEP)
        string = string[1 : -1]
        string = string.replace('[', PartSum.GROUP_START)
        string = string.replace(']', PartSum.GROUP_END)
        i = 0
        while i < len(string):
            start = string[i :].find(PartSum.GROUP_START) + i
            if start == -1:
                break
            end = string[start :].index(PartSum.GROUP_END) + start
            if string[start : end + 1].count(RollPart.POS) < 1:
                string = string[: start] + string[start + 1: end] + string[end + 1:]
            i = end + 1
        string += PartSum.PART_SEP + PartSum.RES_SEP + PartSum.PART_SEP + str(parts[1])
        return string

    def min_str(self) -> str:
        return self.string(self.min())

    def max_str(self) -> str:
        return self.string(self.max())

    def avg_str(self) -> str:
        return self.string(self.avg())

    def rand_str(self) -> str:
        return self.string(self.rand())

assert PartSum([Dice(2,6),Modifier(2)]) == PartSum([Dice(2,6),Modifier(2)])
assert PartSum([Dice(2,6),Modifier(2)]).min() == ([[1,1],[2]],4)
assert PartSum([Dice(2,6),Modifier(2)]).max() == ([[6,6],[2]],14)
assert PartSum([Dice(2,6),Modifier(2)]).avg() == ([[3.5,3.5],[2]],9.0)
assert PartSum([Dice(2,6),Modifier(2)]).min_str() == '(1 + 1) + 2 = 4'
assert PartSum([Dice(2,6),Modifier(2)]).max_str() == '(6 + 6) + 2 = 14'
assert PartSum([Dice(2,6),Modifier(2)]).avg_str() == '(3.5 + 3.5) + 2 = 9.0'
