from roll_part_base import RollPart
from modifier import Modifier
from dice_pool import Dice
from roll_part_list import PartSum
import sys

class UserInterface():    
    EXIT = 'close'
    LOST = 'help'
    WELCOME = 'Welcome to the Mader Dice Analyser.\n'
    HELP = ('Separate modifiers and dice with \''+RollPart.POS+'\' or \''+RollPart.NEG+'\' and use \''+Dice.sep+'\' to indicate dice.'
            +'\nThe left hand side of a dice is the quantity and the right hand side is the size.'
            +'\nThe right hand side of a dice can be \''+Dice.fudge+'\' to roll a number of fudge/fate dice that roll either a 1, 0, or -1 each.'
            +'\nFinally, input \''+EXIT+'\' to close this program or \''+LOST+'\' to display this help section.\n')
    PROMPT = 'Input your dice roll formula (or \''+EXIT+'\' to exit or \''+LOST+'\' to show help): '
    GOODBYE = 'Thanks for using the Mader Dice Analyser.'
    
    def separate(str0: str, sep: str) -> list:
        strings = str0.split(sep)
        i = 1
        while i < len(strings):
            strings[i] = sep + strings[i]
            i += 1
        if strings[0] == '':
            strings.pop(0)
        return strings
    
    def identify(str0: str) -> list:
        str0 = str0.replace(' ','')
        str1_parts = UserInterface.separate(str0, RollPart.POS)
        str2_parts = []
        for part in str1_parts:
            parts = UserInterface.separate(part, RollPart.NEG)
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
                if __debug__:
                    raise
                print(str(sys.exc_info()[0].__name__)+': '+str(sys.exc_info()[1]))
                print()
        raise

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
assert UserInterface.identify('6-1d4') == PartSum([Modifier(6),Dice(1,4,True)])
assert UserInterface.identify('-2d4') == PartSum([Dice(2,4,True)])
assert UserInterface.identify('-1df') == PartSum([Dice(1,3),Modifier(-2)])
assert UserInterface.identify('3df') == PartSum([Dice(3,3),Modifier(-6)])

if __name__ == '__main__':
    UserInterface().main()
