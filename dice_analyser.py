import sys, random

class RollPart():
    pos = '+'
    neg = '-'

class Dice(RollPart):
    sep = 'd'
    fudge = 'f'
    def __init__(self, quant: int, size: int, neg: bool = False):
        if not isinstance(quant, int):
            raise TypeError
        if not isinstance(size, int):
            raise TypeError
        if not isinstance(neg, bool):
            raise TypeError
        if size < 2:
            raise ValueError
        if quant < 1:
            raise ValueError
        self.neg = neg
        self.quant = quant
        self.size = size
        rand = 0
        count = 0
        while count < quant:
            rand += random.randint(1, size)
            count += 1
        if neg:
            self.min = -1 * quant * size
            self.max = -1 * quant
            self.avg = -1 * (size + 1) / 2 * quant
            self.rand = -1 * rand
        else:
            self.min = quant
            self.max = quant * size
            self.avg = (size + 1) / 2 * quant
            self.rand = rand
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
            raise TypeError
        return self.quant == other.quant and self.size == other.size and self.neg == other.neg
    def __ne__(self, other) -> bool:
        return not self == other
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
            raise TypeError
        self.const = const
        self.min = const
        self.max = const
        self.avg = const
        self.rand = const
        return
    def __repr__(self) -> str:
        return 'Modifier('+str(self.const)+')'
    def __str__(self) -> str:
        if self.const < 0:
            return str(self.const)
        else:
            return '+'+str(self.const)
    def __eq__(self, other) -> bool:
        if not isinstance(other, Modifier):
            raise TypeError
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

EXIT = 'close'
WELCOME = 'Welcome to the Mader Dice Analyser.\n'
HELP = 'Separate modifiers and dice with \''+RollPart.pos+'\' or \''+RollPart.neg+'\' and use \''+Dice.sep+'\' to indicate dice.\nThe left hand side of a dice is the quantity and the right hand side is the size.\nThe right hand side of a dice can be \''+Dice.fudge+'\' to roll a number of fudge/fate dice that roll either a 1, 0, or -1 each.\nFinally, input \''+EXIT+'\' to close this program.\n'
PROMPT = 'Input your dice roll formula (or \''+EXIT+'\' to exit): '
GOODBYE = 'Thanks for using the Mader Dice Analyser.'

def minimum(sum_list: list) -> int:
    minimum = 0
    for part in sum_list:
        if not isinstance(part, (Dice, Modifier)):
            raise TypeError
        minimum += part.min
    return minimum
assert minimum([Dice(1,6)]) == 1
assert minimum([Dice(1,6),Modifier(2)]) == 3
assert minimum([Dice(2,6)]) == 2

def maximum(sum_list: list) -> list:
    maximum = 0
    for part in sum_list:
        if not isinstance(part, (Dice, Modifier)):
            raise TypeError
        maximum += part.max
    return maximum
assert maximum([Dice(1,6)]) == 6
assert maximum([Dice(1,6),Modifier(2)]) == 8
assert maximum([Dice(2,6)]) == 12

def average(sum_list: list) -> float:
    average = 0.0
    for part in sum_list:
        if not isinstance(part, (Dice, Modifier)):
            raise TypeError
        average += part.avg
    return average
assert average([Dice(1,6)]) == 3.5
assert average([Dice(1,6),Modifier(2)]) == 5.5
assert average([Dice(2,6)]) == 7.0

def rand(sum_list: list) -> int:
    rand = 0
    for part in sum_list:
        if not isinstance(part, (Dice, Modifier)):
            raise TypeError
        rand += part.rand
    return rand
assert rand([Dice(1,6)]) >= 1 and rand([Dice(1,6)]) <= 6
assert rand([Dice(1,6),Modifier(2)]) >= 3 and rand([Dice(1,6),Modifier(2)]) <= 8
assert rand([Dice(2,6)]) >= 2 and rand([Dice(2,6)]) <= 12

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
    return part_list
assert identify('1d6')== [Dice(1,6)]
assert identify('1 d 6') == [Dice(1,6)]
assert identify('1d6+2') == [Dice(1,6),Modifier(2)]
assert identify(' 1 d 6 + 2 ') == [Dice(1,6),Modifier(2)]
assert identify('2d6') == [Dice(2,6)]
assert identify('2d6-4') == [Dice(2,6),Modifier(-4)]
assert identify('6-1d4') == [Modifier(6),Dice(1,4,True)]
assert identify('-2d4') == [Dice(2,4,True)]
assert identify('-1df') == [Dice(1,3),Modifier(-2)]
assert identify('3df') == [Dice(3,3),Modifier(-6)]

def main():
    print(WELCOME)
    print(HELP)
    while True:
        in_str = input(PROMPT)
        if in_str == EXIT:
            print(GOODBYE)
            raise SystemExit
        try:
            parts = identify(in_str)
            print('min: '+str(minimum(parts)))
            print('max: '+str(maximum(parts)))
            print('average: '+str(average(parts)))
            print('roll: '+str(rand(parts)))
            print()
        except:
            print(str(sys.exc_info()[0].__name__)+': '+str(sys.exc_info()[1]))
            print()
    raise

main()
