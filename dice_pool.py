from roll_part_base import RollPart
from random import randint

class Dice(RollPart):
    SEP = 'd'
    FUDGE = 'f'
    RANGE_START = '{'
    RANGE_END = '}'
    RANGE_SEP = ','
    RANGE_BASE = 1
    
    def __init__(self, quant: int, faces: [int]):
        if not isinstance(quant, int):
            raise TypeError('\'quant\' must be an integer, not a ' + str(type(quant)))
        if not isinstance(faces, list):
            raise TypeError('\'faces\' must be a list of integers, not a ' + str(type(faces)))
        if len(faces) < 2:
            raise ValueError('\'faces\' must be longer than 1, not ' + str(len(faces)))
        for face in faces:
            if not isinstance(face, int):
                raise TypeError('\'faces\' must contain only integers, not a ' + str(type(face)))
        if quant < 1:
            raise ValueError('\'quant\' must be greater than 0, not ' + str(quant))
        self.quant = quant
        self.faces = faces
        return
    
    def __repr__(self) -> str:
        '''Convert this dice pool into a machine executable string.

    Executing this string should create a copy of this dice pool.'''
        return 'Dice('+str(self.quant)+', '+repr(self.faces)+')'

    def __str__(self) -> str:
        '''Convert this dice pool into a human readable string.

    This string should be able to be interpreted as an exact copy of this dice pool.'''
        string = str(self.quant) + Dice.SEP
        if self.faces == list(range(Dice.RANGE_BASE, Dice.RANGE_BASE + len(self.faces))):
            string = Dice.POS + string + str(len(self.faces) - 1 + Dice.RANGE_BASE)
        elif self.faces == list(range((Dice.RANGE_BASE + len(self.faces) - 1) * -1, Dice.RANGE_BASE * -1 + 1)):
            string = Dice.NEG + string + str(len(self.faces) - 1 + Dice.RANGE_BASE)
        elif self.faces == [1,0,-1]:
            string = Dice.POS + string + Dice.FUDGE
        else:
            string = Dice.POS + string + Dice.RANGE_START
            for i in range(len(self.faces)):
                string += str(self.faces[i])
                if i < len(self.faces) - 1:
                    string += Dice.RANGE_SEP
            string += Dice.RANGE_END
        return string

    def __eq__(self, other) -> bool:
        '''Determine if this dice pool is equal to another dice pool.'''
        if not isinstance(other, Dice):
            raise TypeError('Dice can only be compared to other Dice, not ' + str(type(other)))
        return self.quant == other.quant and self.faces == other.faces

    def __ne__(self, other) -> bool:
        '''Determine whether this dice pool is not equal to another dice pool.'''
        return not self == other

    def rand(self) -> [int]:
        '''Calculate a random roll of this dice pool.'''
        random = [0] * self.quant
        for i in range(self.quant):
            random[i] = choose(self.faces)
        return random

    def min(self) -> [int]:
        '''Calculate the minimum roll of this dice pool.'''
        return [min(self.faces)] * self.quant

    def max(self) -> [int]:
        '''Calculate the mmaximum roll of this dice pool.'''
        return [max(self.faces)] * self.quant

    def avg(self) -> [float]:
        '''Calculate the average roll of this dice pool.'''
        return [float(sum(self.faces)) / len(self.faces)] * self.quant

assert Dice(1,list(range(1,2+1))) == Dice(1,list(range(1,2+1)))
assert Dice(2,list(range(1,3+1))) != Dice(3,list(range(1,2+1)))
assert Dice(1,list(range(1,2+1))).quant == 1
assert Dice(1,list(range(1,2+1))).min() == [1]
assert Dice(1,list(range(1,2+1))).max() == [2]
assert Dice(1,list(range(1,2+1))).avg() == [1.5]
assert repr(Dice(1,list(range(1,2+1)))) == 'Dice(1, [1, 2])'
assert str(Dice(1,list(range(1,2+1)))) == '+1d2'

assert Dice(2,list(range(-2,-1+1))).min() == [-2,-2]
assert Dice(2,list(range(-2,-1+1))).max() == [-1,-1]
assert Dice(2,list(range(-2,-1+1))).avg() == [-1.5,-1.5]
assert repr(Dice(1,list(range(-2,-1+1)))) == 'Dice(1, [-2, -1])'
assert str(Dice(1,list(range(-2,-1+1)))) == '-1d2'

assert Dice(2,[1,0,-1]).min() == [-1,-1]
assert Dice(2,[1,0,-1]).max() == [1,1]
assert Dice(2,[1,0,-1]).avg() == [0,0]
assert repr(Dice(2,[1,0,-1])) == 'Dice(2, [1, 0, -1])'
assert str(Dice(2,[1,0,-1])) == '+2df'

assert Dice(3,[1,2,4,8]).min() == [1,1,1]
assert Dice(3,[1,2,4,8]).max() == [8,8,8]
assert Dice(3,[1,2,4,8]).avg() == [3.75,3.75,3.75]
assert repr(Dice(3,[1,2,4,8])) == 'Dice(3, [1, 2, 4, 8])'
assert str(Dice(3,[1,2,4,8])) == '+3d{1,2,4,8}'
