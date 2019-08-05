import sys, random

class RollPart():
    pos = '+'
    neg = '-'

class Dice(RollPart):
    sep = 'd'
    fudge = 'f'
    low = '<'
    high = '>'
    def __init__(self, quant: int, size: int, neg: bool = False, drop_high: int = 0, drop_low: int = 0):
        if not isinstance(quant, int):
            raise TypeError('\'quant\' must be an integer, not a ' + str(type(quant)))
        if not isinstance(size, int):
            raise TypeError('\'size\' must be and integer, not a ' + str(type(size)))
        if not isinstance(neg, bool):
            raise TypeError('\'neg\' must be a boolean, not a ' + str(type(neg)))
        if not isinstance(drop_high, int):
            raise TypeError('\'drop_high\' must be an integer, not a ' + str(type(drop_high)))
        if not isinstance(drop_low, int):
            raise TypeError('\'drop_low\' must be an integer, not a ' + str(type(drop_low)))
        if size < 2:
            raise ValueError('\'size\' must be greater than 1, not ' + str(size))
        if quant < 1:
            raise ValueError('\'quant\' must be greater than 0, not ' + str(quant))
        if drop_high < 0:
            raise ValueError('\'drop_high\' must be greater than -1, not ' + str(drop_high))
        if drop_low < 0:
            raise ValueError('\'drop_low\' must be greater than -1, not ' + str(drop_low))
        if drop_high + drop_low >= quant:
            raise ValueError('the quantity of dice after dropping must be greater than 0, not ' + str(quant - drop_high - drop_low))
        self.neg = neg
        self.quant = quant
        self.size = size
        self.drop_high = drop_high
        self.drop_low = drop_low
        if neg:
            self.min = -1 * quant * size
            self.max = -1 * quant
            self.avg = -1 * (size + 1) / 2 * quant
        else:
            self.min = quant
            self.max = quant * size
            self.avg = (size + 1) / 2 * quant
        self.roll()
        return
    def __repr__(self) -> str:
        return 'Dice('+str(self.quant)+','+str(self.size)+','+str(self.neg)+')'
    def __str__(self) -> str:
        string = str(self.quant)+'d'+str(self.size)
        if self.neg:
            return Dice.neg+string
        else:
            return Dice.pos+string
    def __eq__(self, other) -> bool:
        if not isinstance(other, Dice):
            raise TypeError('Dice can only be compared to other Dice, not ' + str(type(other)))
        return self.quant == other.quant and self.size == other.size and self.neg == other.neg
    def __ne__(self, other) -> bool:
        return not self == other
    def roll(self) -> int:
        rand_list = []
        count = 0
        while count < self.quant:
            rand_list.append(random.randint(1, self.size))
            count += 1
        rand_list.sort()
        if self.drop_high > 0:
            rand_list=rand_list[self.drop_low:-self.drop_high]
        else:
            rand_list=rand_list[self.drop_low:]
        rand = 0
        i = 0
        while i < len(rand_list):
            rand += rand_list[i]
            i += 1
        if self.neg:
            self.rand = -1 * rand
        else:
            self.rand = rand
        return self.rand
assert Dice(1,2) == Dice(1,2, False)
assert Dice(2,3) != Dice(3,2)
assert Dice(1,2).quant == 1
assert Dice(1,2).size == 2
assert Dice(1,2).min == 1
assert Dice(1,2).max == 2
assert Dice(1,2).avg == 1.5
assert repr(Dice(1,2)) == 'Dice(1,2,False)'
assert str(Dice(1,2)) == '+1d2'
assert Dice(2,2).rand >= Dice(2,2).min and Dice(2,2).rand <= Dice(2,2).max
assert Dice(1,2,True).min == -2
assert Dice(1,2,True).max == -1
assert Dice(1,2,True).avg == -1.5
assert Dice(1,2,True).rand >= -2 and Dice(1,2,True).rand <= -1
assert repr(Dice(1,2,True)) == 'Dice(1,2,True)'
assert str(Dice(1,2,True)) == '-1d2'

class Modifier(RollPart):
    def __init__(self, const: int):
        if not isinstance(const, int):
            raise TypeError('\'const\' must be an integer, not a ' + str(type(const)))
        self.const = const
        self.min = const
        self.max = const
        self.avg = const
        self.rand = const
        return
    def __repr__(self) -> str:
        return 'Modifier(' + str(self.const) + ')'
    def __str__(self) -> str:
        if self.const < 0:
            return str(self.const)
        else:
            return '+' + str(self.const)
    def __eq__(self, other) -> bool:
        if not isinstance(other, Modifier):
            raise TypeError('Modifer must only be compater to other Modifer, not a ' + str(type(other)))
        return self.const == other.const
    def __ne__(self, other) -> bool:
        return not self == other
assert Modifier(1) == Modifier(1)
assert Modifier(1) != Modifier(2)
assert Modifier(1).const == 1
assert Modifier(1).min == 1
assert Modifier(1).max == 1
assert Modifier(1).avg == 1
assert repr(Modifier(1)) == 'Modifier(1)'
assert str(Modifier(1)) == '+1'
assert Modifier(1).rand == 1
assert str(Modifier(-1)) == '-1'

class SumList():
    def __init__(self, parts: list):
        if not isinstance(parts, list):
            raise TypeError('\'parts\' must be a list, not a ' +str(type(parts)))
        for part in parts:
            if not issubclass(type(part), RollPart):
                raise TypeError('every element in \'parts\' must be a subclass of RollPart, not ' + str(type(part)))
        self.parts = parts
        return
    def __repr__(self) -> str:
        return 'SumList(' + repr(self.parts) + ')'
    def __str__(self):
        raise NotImplemented('Use \'stat_str()\' instead')
    def __eq__(self, other) -> bool:
        if not isinstance(other, SumList):
            raise TypeError
        return self.parts == other.parts
    def min(self) -> int:
        minimum = 0
        for part in self.parts:
            minimum += part.min
        return minimum
    def max(self) -> int:
        maximum = 0
        for part in self.parts:
            maximum += part.max
        return maximum
    def avg(self) -> float:
        avg = 0.0
        for part in self.parts:
            avg += part.avg
        return avg
    def rand(self) -> int:
        rand = 0
        for part in self.parts:
            rand += part.rand
        return rand
    def stat_str(self, stat: str) -> str:
        str0 = ''
        for part in self.parts:
            val = eval('part.' + stat, globals(), locals())
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
assert SumList([Dice(1,6),Modifier(2)]) == SumList([Dice(1,6),Modifier(2)])
assert SumList([Dice(1,6),Modifier(2)]).min() == 3
assert SumList([Dice(1,6),Modifier(2)]).max() == 8
assert SumList([Dice(1,6),Modifier(2)]).avg() == 5.5
assert SumList([Dice(1,6),Modifier(2)]).stat_str('min') == '1+2'
assert SumList([Dice(1,6),Modifier(2)]).stat_str('max') == '6+2'
assert SumList([Dice(1,6),Modifier(2)]).stat_str('avg') == '3.5+2'

def separate(str0: str, sep: str) -> list:
    strings = str0.split(sep)
    i = 1
    while i < len(strings):
        strings[i] = sep + strings[i]
        i += 1
    if strings[0] == '':
        strings.pop(0)
    return strings
assert separate('a b c', ' ') == ['a',' b',' c']
assert separate(' a b c ', ' ') == [' a',' b',' c',' ']
assert separate(',',',') == [',']
assert separate('$$$','$') == ['$','$','$']
assert separate('->a->b->c->','->') == ['->a','->b','->c','->']

def identify(str0: str) -> list:
    str0 = str0.replace(' ','')
    str1_parts = separate(str0, RollPart.pos)
    str2_parts = []
    for part in str1_parts:
        parts = separate(part, RollPart.neg)
        for item in parts:
            str2_parts.append(item)
    part_list = []
    for part in str2_parts:
        if part.count(Dice.sep) > 1:
            raise ValueError
        elif part.count(Dice.sep) == 1:
            lhs = part.partition(Dice.sep)[0]
            rhs = part.partition(Dice.sep)[2]
            if rhs == Dice.fudge:
                part_list.append(Dice(abs(int(lhs)), 3))
                part_list.append(Modifier(-2*abs(int(lhs))))
            elif int(lhs) < 0:
                part_list.append(Dice(int(lhs)*-1, int(rhs), True))
            else:
                part_list.append(Dice(int(lhs), int(rhs), False))
        else:
            part_list.append(Modifier(int(part)))
    return SumList(part_list)
assert identify('1d6')== SumList([Dice(1,6)])
assert identify('1 d 6') == SumList([Dice(1,6)])
assert identify('1d6+2') == SumList([Dice(1,6),Modifier(2)])
assert identify(' 1 d 6 + 2 ') == SumList([Dice(1,6),Modifier(2)])
assert identify('2d6') == SumList([Dice(2,6)])
assert identify('2d6-4') == SumList([Dice(2,6),Modifier(-4)])
assert identify('6-1d4') == SumList([Modifier(6),Dice(1,4,True)])
assert identify('-2d4') == SumList([Dice(2,4,True)])
assert identify('-1df') == SumList([Dice(1,3),Modifier(-2)])
assert identify('3df') == SumList([Dice(3,3),Modifier(-6)])

class UserInterface():    
    EXIT = 'close'
    LOST = 'help'
    WELCOME = 'Welcome to the Mader Dice Analyser.\n'
    HELP = 'Separate modifiers and dice with \''+RollPart.pos+'\' or \''+RollPart.neg+'\' and use \''+Dice.sep+'\' to indicate dice.\nThe left hand side of a dice is the quantity and the right hand side is the size.\nThe right hand side of a dice can be \''+Dice.fudge+'\' to roll a number of fudge/fate dice that roll either a 1, 0, or -1 each.\nFinally, input \''+EXIT+'\' to close this program or \''+LOST+'\' to display this help section.\n'
    PROMPT = 'Input your dice roll formula (or \''+EXIT+'\' to exit or \''+LOST+'\' to show help): '
    GOODBYE = 'Thanks for using the Mader Dice Analyser.'
    
    def main(self):
        print(self.WELCOME)
        print(self.HELP)
        while True:
            in_str = input(self.PROMPT)
            if in_str == self.EXIT:
                print(self.GOODBYE)
                raise SystemExit
            elif in_str == self.LOST:
                print(self.HELP)
                continue
            try:
                parts = identify(in_str)
                print('min: ' + parts.stat_str('min') + ' = ' + str(parts.min()))
                print('max: ' + parts.stat_str('max') + ' = ' + str(parts.max()))
                print('average: ' + parts.stat_str('avg') + ' = ' + str(parts.avg()))
                print('roll: ' + parts.stat_str('rand') + ' = ' + str(parts.rand()))
                print()
            except:
                print(str(sys.exc_info()[0].__name__)+': '+str(sys.exc_info()[1]))
                print()
        raise

if __name__ == '__main__':
    UserInterface().main()
