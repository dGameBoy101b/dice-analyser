from roll_part_base import RollPart
from random import randint

class Dice(RollPart):
    sep = 'd'
    fudge = 'f'
    def __init__(self, quant: int, size: int, neg: bool = False):
        if not isinstance(quant, int):
            raise TypeError('\'quant\' must be an integer, not a ' + str(type(quant)))
        if not isinstance(size, int):
            raise TypeError('\'size\' must be and integer, not a ' + str(type(size)))
        if not isinstance(neg, bool):
            raise TypeError('\'neg\' must be a boolean, not a ' + str(type(neg)))
        if size < 2:
            raise ValueError('\'size\' must be greater than 1, not ' + str(size))
        if quant < 1:
            raise ValueError('\'quant\' must be greater than 0, not ' + str(quant))
        self.neg = neg
        self.quant = quant
        self.size = size
        return
    
    def __repr__(self) -> str:
        '''Convert this dice pool into a machine executable string.

    Executing this string should create a copy of this dice pool.'''
        return 'Dice('+str(self.quant)+','+str(self.size)+','+str(self.neg)+')'

    def __str__(self) -> str:
        '''Convert this dice pool into a human readable string.

    This string should be able to be interpreted as an exact copy of this dice pool.'''
        string = str(self.quant)+'d'+str(self.size)
        if self.neg:
            return Dice.neg+string
        else:
            return Dice.pos+string

    def __eq__(self, other) -> bool:
        '''Determine if this dice pool is equal to another dice pool.'''
        if not isinstance(other, Dice):
            raise TypeError('Dice can only be compared to other Dice, not ' + str(type(other)))
        return self.quant == other.quant and self.size == other.size and self.neg == other.neg

    def __ne__(self, other) -> bool:
        '''Determine whether this dice pool is not equal to another dice pool.'''
        return not self == other

    def rand(self) -> int:
        '''Calculate a random roll of this dice pool.'''
        total = 0
        for i in range(self.quant):
            total += randint(1, self.size)
        if self.neg:
            total *= -1
        return total

    def min(self) -> int:
        '''Calculate the minimum roll of this dice pool.'''
        minimum = self.quant
        if self.neg:
            minimum *= -1 * self.size
        return minimum

    def max(self) -> int:
        '''Calculate the mmaximum roll of this dice pool.'''
        maximum = self.quant
        if self.neg:
            maximum *= -1
        else:
            maximum *= self.size
        return  maximum

    def avg(self) -> float:
        '''Calculate the average roll of this dice pool.'''
        average = (self.size + 1) / 2 * self.quant
        if self.neg:
            average *= -1 
        return average

assert Dice(1,2) == Dice(1,2, False)
assert Dice(2,3) != Dice(3,2)
assert Dice(1,2).quant == 1
assert Dice(1,2).size == 2
assert Dice(1,2).min() == 1
assert Dice(1,2).max() == 2
assert Dice(1,2).avg() == 1.5
assert repr(Dice(1,2)) == 'Dice(1,2,False)'
assert str(Dice(1,2)) == '+1d2'
assert Dice(2,2).rand() >= Dice(2,2).min() and Dice(2,2).rand() <= Dice(2,2).max()

assert Dice(1,2,True).min() == -2
assert Dice(1,2,True).max() == -1
assert Dice(1,2,True).avg() == -1.5
assert repr(Dice(1,2,True)) == 'Dice(1,2,True)'
assert str(Dice(1,2,True)) == '-1d2'
assert Dice(1,2,True).rand() >= Dice(1,2,True).min() and Dice(1,2,True).rand() <= Dice(1,2,True).max()
