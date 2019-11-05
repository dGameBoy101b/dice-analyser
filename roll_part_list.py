from modifier import Modifier
from dice_pool import Dice
from roll_part_base import RollPart

class PartSum():
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
        raise NotImplemented('Use \'stat_str()\' instead')

    def __eq__(self, other) -> bool:
        '''Determin whether this roll part list is equal to another.'''
        if not isinstance(other, PartSum):
            raise TypeError
        return self.parts == other.parts

    def min(self) -> int:
        minimum = 0
        for part in self.parts:
            minimum += part.min()
        return minimum

    def max(self) -> int:
        maximum = 0
        for part in self.parts:
            maximum += part.max()
        return maximum

    def avg(self) -> float:
        avg = 0.0
        for part in self.parts:
            avg += part.avg()
        return avg

    def rand(self) -> int:
        rand = 0
        for part in self.parts:
            rand += part.rand()
        return rand

    def stat_str(self, stat: str) -> str:
        str0 = ''
        for part in self.parts:
            if stat == 'min':
                val = part.min()
            elif stat == 'max':
                val = part.max()
            elif stat == 'avg':
                val = part.avg()
            elif val == 'rand':
                val = part.rand()
            else:
                raise ValueError('\'stat\' must be one of \'min\', \'max\', \'avg\', or \'rand\', not '+repr(stat))
            if isinstance(part, Dice) and part.neg:
                str0 += RollPart.neg + str(val)
            elif isinstance(part, Dice):
                str0 += RollPart.pos + str(val)
            elif isinstance(part, Modifier) and val >= 0:
                str0 += RollPart.pos + str(val)
            else:
                str0 += str(val)
        if str0[0] == RollPart.pos:
            str0 = str0[1:]
        return str0
    
assert PartSum([Dice(1,6),Modifier(2)]) == PartSum([Dice(1,6),Modifier(2)])
assert PartSum([Dice(1,6),Modifier(2)]).min() == 3
assert PartSum([Dice(1,6),Modifier(2)]).max() == 8
assert PartSum([Dice(1,6),Modifier(2)]).avg() == 5.5
assert PartSum([Dice(1,6),Modifier(2)]).avg() >= PartSum([Dice(1,6),Modifier(2)]).min() and PartSum([Dice(1,6),Modifier(2)]).rand() <= PartSum([Dice(1,6),Modifier(2)]).max()
assert PartSum([Dice(1,6),Modifier(2)]).stat_str('min') == '1+2'
assert PartSum([Dice(1,6),Modifier(2)]).stat_str('max') == '6+2'
assert PartSum([Dice(1,6),Modifier(2)]).stat_str('avg') == '3.5+2'
