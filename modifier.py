from roll_part_base import RollPart

class Modifier(RollPart):

    def __init__(self, const: int):
        if not isinstance(const, int):
            raise TypeError('\'const\' must be an integer, not a ' + str(type(const)))
        self.const = const
        return

    def __repr__(self) -> str:
        '''Convert this modifier to a machine executable string.

    This string should create an exact copy of this modifier when executed.'''
        return 'Modifier(' + str(self.const) + ')'

    def __str__(self) -> str:
        '''Convert this modifier to a human readable string.

    This string should be able to be interpreted as an exact copy of this modifier.'''
        if self.const < 0:
            return str(self.const)
        else:
            return '+' + str(self.const)

    def __eq__(self, other) -> bool:
        '''Determine whether this modifier is equal to another modifier.'''
        if not isinstance(other, Modifier):
            raise TypeError('Modifer must only be compater to other Modifer, not a ' + str(type(other)))
        return self.const == other.const

    def __ne__(self, other) -> bool:
        '''Determine whether this modifier is not equal to another modifier.'''
        return not self == other

    def min(self) -> [int]:
        '''Calculate the minimum roll of this modifier.'''
        return [self.const]

    def max(self) -> [int]:
        '''Calculate the maximum roll of this modifier.'''
        return [self.const]

    def avg(self) -> [float]:
        '''Calculate the average roll of this modifier.'''
        return [self.const]
    
    def rand(self) -> [int]:
        '''Calculate a random roll of this modifier.'''
        return [self.const]


assert Modifier(1).const == 1
assert Modifier(1) == Modifier(1)
assert Modifier(1) != Modifier(2)
assert Modifier(1).min() == [1]
assert Modifier(1).max() == [1]
assert Modifier(1).avg() == [1]
assert Modifier(1).rand() == [1]
assert repr(Modifier(1)) == 'Modifier(1)'
assert str(Modifier(1)) == '+1'
assert str(Modifier(-1)) == '-1'
