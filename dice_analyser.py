from roll_part_base import RollPart
from modifier import Modifier
from dice_pool import Dice
from roll_part_list import PartSum
import sys

class UserInterface():
    EXIT = 'close'
    LOST = 'help'
    WELCOME = 'Welcome to the Mader Dice Analyser.\n'
    HELP = ('Separate modifiers and dice with \''+RollPart.POS+'\' or \''+RollPart.NEG+'\' and use \''+Dice.SEP+'\' to indicate dice.'
            +'\nThe left hand side of a dice is the quantity and the right hand side is the size.'
            +'\nThe right hand side of a dice can be \''+Dice.FUDGE+'\' to roll a number of fudge/fate dice that roll either a 1, 0, or -1 each.'
            +'\nThe right hand side of a dice can also be a custom dice range by enclosing a set of numbers with \''+Dice.RANGE_START+'\' and \''+Dice.RANGE_END
            +'\', with each number separated by \''+Dice.RANGE_SEP+'\'.'
            +'\nThe left hand side may optionally have a \''+Dice.DROP_HIGH+'\' just before the dice separator to indicate that the highest result of that dice pool'
            +' should be dropped during calculations and rolling.'
            +'\nSimilarly, the left hand side may instead have a \''+Dice.DROP_LOW+'\' just before the dice separator to indicate that the lowest result of that dice'
            +' pool should be dropped during calculations and rolling.'
            +'\nFinally, input \''+EXIT+'\' to close this program or \''+LOST+'\' to display this help section.\n')
    PROMPT = 'Input your dice roll formula (or \''+EXIT+'\' to exit or \''+LOST+'\' to show help): '
    GOODBYE = 'Thanks for using the Mader Dice Analyser.'

    def separate(str0: str, sep: str) -> [str]:
        strings = str0.split(sep)
        i = 1
        while i < len(strings):
            strings[i] = sep + strings[i]
            i += 1
        if strings[0] == '':
            strings.pop(0)
        return strings

    def splitParts(str0: str) -> [str]:
        #remove spaces
        str1 = str0.replace(' ','')
        #separate by plus
        str2 = UserInterface.separate(str1, RollPart.POS)
        #separate by minus
        str3 = []
        for part in str2:
            piece = UserInterface.separate(part, RollPart.NEG)
            for item in piece:
                str3.append(item)
        #group ranges
        str4 = []
        start = 0
        while start < len(str3):
            if str3[start].count(Dice.RANGE_START) < 1:
                str4.append(str3[start])
                start += 1
            else:
                end = start
                while end < len(str3):
                    if str3[end].count(Dice.RANGE_END) < 1:
                        end += 1
                    else:
                        part = ''
                        for i in range(start, end + 1):
                            part += str3[i]
                        str4.append(part)
                        start = end + 1
                        break
        #group dice
        str5 = []
        prefix = 0
        while prefix < len(str4):
            if prefix < len(str4) - 1 and str4[prefix].count(Dice.SEP) > 0 and len(str4[prefix].partition(Dice.SEP)[2]) < 1:
                str5.append(str4[prefix] + str4[prefix + 1])
                prefix += 2
            else:
                str5.append(str4[prefix])
                prefix += 1
        return str5

    def identify(str0: str) -> PartSum:
        #split input
        parts = UserInterface.splitParts(str0)
        part_list = []
        #validate input
        for part in parts:
            if part.count(Dice.SEP) > 1:
                raise ValueError('Must be at most 1 dice separator in a roll part!')
            if part.count(Dice.RANGE_START) > 1:
                raise ValueError('Must be at most 1 dice range starter in a roll part!')
            if part.count(Dice.RANGE_END) > 1:
                raise ValueError('Must be at most 1 dice range ender in a roll part!')
            if part.count(Dice.RANGE_START) != part.count(Dice.RANGE_END):
                raise ValueError('Must be the same number of dice range starters and enders in a roll part!')
            if part.find(Dice.RANGE_START) > part.find(Dice.RANGE_END):
                raise ValueError('A dice range starter must come before a dice range ender in a roll part!')
            if part.count(Dice.DROP_HIGH) > 1:
                raise ValueError('Must be at most 1 drop high flag in a roll part!')
            if part.count(Dice.DROP_LOW) > 1:
                raise ValueError('Must be at most 1 drop low flag in a roll part!')
            if part.find(Dice.DROP_HIGH) != -1 and part.find(Dice.DROP_LOW) != -1:
                raise ValueError('Cannot have both a drop high and a drop low flag in a roll part!')
            if part.find(Dice.DROP_HIGH) != -1 and part.find(Dice.DROP_HIGH) + len(Dice.DROP_HIGH) != part.find(Dice.SEP):
                raise ValueError('A drop high flag must come immediately before a dice separator in a roll part!')
            if part.find(Dice.DROP_LOW) != -1 and part.find(Dice.DROP_LOW) + len(Dice.DROP_LOW) != part.find(Dice.SEP):
                raise ValueError('A drop low flag must com immediately before a dice separator in a roll part!')
            #interpret input
            if part.count(Dice.SEP) == 1:
                lhs = part.partition(Dice.SEP)[0]
                rhs = part.partition(Dice.SEP)[2]
                if lhs.find(Dice.DROP_HIGH) != -1:
                    drop = 1
                    lhs = lhs[: -len(Dice.DROP_LOW)]
                elif lhs.find(Dice.DROP_LOW) != -1:
                    drop = -1
                    lhs = lhs[: -len(Dice.DROP_LOW)]
                else:
                    drop = 0
                if rhs == Dice.FUDGE:
                    faces = Dice.FUDGE_RANGE
                    if lhs[0] == RollPart.NEG:
                        lhs = lhs[1 :]
                elif rhs[0] == Dice.RANGE_START and rhs[-1] == Dice.RANGE_END:
                    faces = rhs.strip(Dice.RANGE_START + Dice.RANGE_END).split(Dice.RANGE_SEP)
                    for i in range(len(faces)):
                        faces[i] = int(faces[i])
                else:
                    faces = int(rhs)
                if int(lhs) < 0:
                    if isinstance(faces, list):
                        faces.reverse()
                        for i in range(len(faces)):
                            faces[i] *= -1
                    elif isinstance(faces, int):
                        faces *= -1
                    else:
                        raise TypeError('Unexpected \'faces\' type '+repr(type(faces)))
                dice = Dice(abs(int(lhs)), faces, drop)
                part_list.append(Dice(abs(int(lhs)), faces, drop))
            else:
                part_list.append(Modifier(int(part)))
        return PartSum(part_list)

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
                parts = UserInterface.identify(in_str)
                print('minimum: ' + parts.min_str())
                print('maximum: ' + parts.max_str())
                print('average: ' + parts.avg_str())
                print('roll: ' + parts.rand_str())
                print()
            except:
##                if __debug__:
##                    raise
                print(str(sys.exc_info()[0].__name__)+': '+str(sys.exc_info()[1]))
                print()
        raise SystemExit('Abnormal exit!')

assert UserInterface.separate('a b c', ' ') == ['a',' b',' c']
assert UserInterface.separate(' a b c ', ' ') == [' a',' b',' c',' ']
assert UserInterface.separate(',',',') == [',']
assert UserInterface.separate('$$$','$') == ['$','$','$']
assert UserInterface.separate('->a->b->c->','->') == ['->a','->b','->c','->']

assert UserInterface.identify('1d6')== PartSum([Dice(1,6)])
assert UserInterface.identify('1 d 6') == PartSum([Dice(1,6)])
assert UserInterface.identify('1d6+2') == PartSum([Dice(1,6),Modifier(2)])
assert UserInterface.identify(' 1 d 6 + 2 ') == PartSum([Dice(1,6),Modifier(2)])
assert UserInterface.identify('2d6') == PartSum([Dice(2,6)])
assert UserInterface.identify('2d6-4') == PartSum([Dice(2,6),Modifier(-4)])
assert UserInterface.identify('6-1d4') == PartSum([Modifier(6),Dice(1,-4)])
assert UserInterface.identify('-2d4') == PartSum([Dice(2,-4)])
assert UserInterface.identify('-1df') == PartSum([Dice(1,Dice.FUDGE_RANGE)])
assert UserInterface.identify('3df') == PartSum([Dice(3,Dice.FUDGE_RANGE)])
assert UserInterface.identify('2vd6') == PartSum([Dice(2,6,1)])
assert UserInterface.identify('2^d6') == PartSum([Dice(2,6,-1)])

if __name__ == '__main__':
    UserInterface().main()
