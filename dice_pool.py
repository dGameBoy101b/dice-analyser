from roll_part_base import RollPart
from random import choice

class Dice(RollPart):
    SEP = 'd'
    FUDGE = 'f'
    FUDGE_RANGE = [1,0,-1]
    RANGE_START = '{'
    RANGE_END = '}'
    RANGE_SEP = ','
    RANGE_BASE = 1
    DROP_HIGH = 'v'
    DROP_LOW = '^'
    
    def __init__(self, quant: int, faces: ([int],range,int), drop: int =0):
        if not isinstance(quant, int):
            raise TypeError('\'quant\' must be an integer, not a ' + str(type(quant)))
        if isinstance(faces, int):
            if faces > Dice.RANGE_BASE:
                faces = range(Dice.RANGE_BASE, faces + 1)
            elif faces < Dice.RANGE_BASE * -1:
                faces = range(faces, Dice.RANGE_BASE * -1 + 1)
            else:
                raise ValueError('integer \'faces\' must be greater in magnitude than ' + str(Dice.RANGE_BASE) + ', not ' + str(faces))
        if isinstance(faces, range):
            faces = list(faces)
        if not isinstance(faces, list):
            raise TypeError('\'faces\' must be a list of integers, not a ' + str(type(faces)))
        if len(faces) < 2:
            raise ValueError('\'faces\' must be longer than 1, not ' + str(len(faces)))
        for face in faces:
            if not isinstance(face, int):
                raise TypeError('\'faces\' must contain only integers, not a ' + str(type(face)))
        if quant < 1:
            raise ValueError('\'quant\' must be greater than 0, not ' + str(quant))
        if not isinstance(drop,int):
            raise TypeError('\'drop\' must be an integer, not a '+str(type(drop)))
        if drop < -1:
            raise ValueError('\'drop\' must be -1 or greater, not '+str(drop))
        if drop > 1:
            raise ValueError('\'drop\' must be 1 or lesser, not '+str(drop))
        if quant - abs(drop) < 1:
            raise ValueError('Must have at least 1 dice left after dropping, not '+str(quant - abs(drop)))
        self.quant = quant
        self.faces = faces
        self.drop = drop
        self.minimum = None
        self.maximum = None
        self.average = None
        return
    
    def __repr__(self) -> str:
        '''Convert this dice pool into a machine executable string.

    Executing this string should create a copy of this dice pool.'''
        return 'Dice('+str(self.quant)+', '+repr(self.faces)+', '+str(self.drop)+')'

    def __str__(self) -> str:
        '''Convert this dice pool into a human readable string.

    This string should be able to be interpreted as an exact copy of this dice pool.'''
        #dropping
        if self.drop == 0:
            drop_str = ''
        elif self.drop == 1:
            drop_str = Dice.DROP_HIGH
        elif self.drop == -1:
            drop_str = Dice.DROP_LOW
        else:
            raise Exception('Unexpected \'self.drop\' value '+str(self.drop))
        #left hand side
        string = str(self.quant) + drop_str + Dice.SEP
        #right hand side
        if self.faces == list(range(Dice.RANGE_BASE, Dice.RANGE_BASE + len(self.faces))):
            string = Dice.POS + string + str(len(self.faces) - 1 + Dice.RANGE_BASE)
        elif self.faces == list(range((Dice.RANGE_BASE + len(self.faces) - 1) * -1, Dice.RANGE_BASE * -1 + 1)):
            string = Dice.NEG + string + str(len(self.faces) - 1 + Dice.RANGE_BASE)
        elif self.faces == Dice.FUDGE_RANGE:
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
        return self.quant == other.quant and self.faces == other.faces and self.drop == other.drop

    def __ne__(self, other) -> bool:
        '''Determine whether this dice pool is not equal to another dice pool.'''
        return not self == other

    def rand(self) -> [int]:
        '''Calculate a random roll of this dice pool.'''
        random = [0] * self.quant
        for i in range(self.quant):
            random[i] = choice(self.faces)
        if self.drop == 1:
            random.remove(max(random))
        elif self.drop == -1:
            random.remove(min(random))
        return random

    def min(self) -> [int]:
        '''Calculate the minimum roll of this dice pool.'''
        if self.minimum == None:
            self.minimum = [min(self.faces)] * (self.quant - abs(self.drop))
        return self.minimum

    def max(self) -> [int]:
        '''Calculate the mmaximum roll of this dice pool.'''
        if self.maximum == None:
            self.maximum = [max(self.faces)] * (self.quant - abs(self.drop))
        return self.maximum

    def avg(self) -> [float]:
        '''Calculate the average roll of this dice pool.'''
        if self.average == None:
            if self.drop == 0:
                self.average = [float(sum(self.faces)) / len(self.faces)] * self.quant
            else:
                space = self.genPermutes()
                total = 0
                for perm in space:
                    total += sum(perm)
                overal_avg = total / len(space)
                self.average = [overal_avg / (self.quant - abs(self.drop))] * (self.quant - abs(self.drop))
        return self.average

    def genPermutes(self) -> [[int]]:
        '''Generate the entire sample space of permutations for this dice pool.'''
        #variable setup
        count = self.quant - 1
        space = []
        for face in self.faces:
            space.append([face])
        #permutation generation
        while count > 0:
            new_space = []
            for sample in space:
                for face in self.faces:
                    new_space.append(sample + [face])
            space = new_space
            count -= 1
        #account dropping
        drop = self.drop
        while drop != 0:
            for perm in space:
                if drop > 0:
                    targ = max(perm)
                elif drop < 0:
                    targ = min(perm)
                perm.remove(targ)
            drop -= int(drop / abs(drop))
        return space

if __name__ == '__main__':
    assert Dice(1,2) == Dice(1,2)
    assert Dice(2,3) != Dice(3,2)
    assert Dice(1,2).quant == 1
    assert Dice(1,2).min() == [1]
    assert Dice(1,2).max() == [2]
    assert Dice(1,2).avg() == [1.5]
    assert repr(Dice(1,2)) == 'Dice(1, [1, 2], 0)'
    assert str(Dice(1,2)) == '+1d2'

    assert Dice(2,-2).min() == [-2]*2
    assert Dice(2,-2).max() == [-1]*2
    assert Dice(2,-2).avg() == [-1.5]*2
    assert repr(Dice(1,-2)) == 'Dice(1, [-2, -1], 0)'
    assert str(Dice(1,-2)) == '-1d2'

    assert Dice(2,Dice.FUDGE_RANGE).min() == [-1]*2
    assert Dice(2,Dice.FUDGE_RANGE).max() == [1]*2
    assert Dice(2,Dice.FUDGE_RANGE).avg() == [0]*2
    assert repr(Dice(2,Dice.FUDGE_RANGE)) == 'Dice(2, [1, 0, -1], 0)'
    assert str(Dice(2,Dice.FUDGE_RANGE)) == '+2df'

    assert Dice(3,[1,2,4,8]).min() == [1]*3
    assert Dice(3,[1,2,4,8]).max() == [8]*3
    assert Dice(3,[1,2,4,8]).avg() == [3.75]*3
    assert repr(Dice(3,[1,2,4,8])) == 'Dice(3, [1, 2, 4, 8], 0)'
    assert str(Dice(3,[1,2,4,8])) == '+3d{1,2,4,8}'

    assert Dice(1,6).genPermutes().sort() == [[1],[2],[3],[4],[5],[6]].sort()
    assert Dice(2,3).genPermutes().sort() == [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]].sort()
    assert Dice(3,2).genPermutes().sort() == [[1,1,1],[1,1,2],[1,2,1],[1,2,2],[2,1,1],[2,1,2],[2,2,1],[2,2,2]].sort()
    assert Dice(2,3,1).genPermutes().sort() == [[1]*5,[2]*3,[3]].sort()
    assert Dice(2,3,-1).genPermutes().sort() == [[1],[2]*3,[3]*5].sort()

    assert Dice(2,6,1).min() == [1]
    assert Dice(2,6,1).max() == [6]
    assert Dice(2,6,1).avg() == [91/36]
    assert len(Dice(2,6,1).rand()) == 1
    assert repr(Dice(2,6,1)) == 'Dice(2, [1, 2, 3, 4, 5, 6], 1)'
    assert str(Dice(2,6,1)) == '+2vd6'

    assert Dice(2,6,-1).min() == [1]
    assert Dice(2,6,-1).max() == [6]
    assert Dice(2,6,-1).avg() == [161/36]
    assert len(Dice(2,6,-1).rand()) == 1
    assert repr(Dice(2,6,-1)) == 'Dice(2, [1, 2, 3, 4, 5, 6], -1)'
    assert str(Dice(2,6,-1)) == '+2^d6'
