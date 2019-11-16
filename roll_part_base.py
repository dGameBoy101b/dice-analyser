class RollPart():
    POS = '+'
    NEG = '-'

    def rand(self) -> [int]:
        '''Calculate a random roll of this dice part.'''
        raise NotImplemented('Every derivative of this class should overrride this method.')

    def min(self) -> [int]:
        '''Calculate the minimum roll of this roll part.'''
        raise NotImplemented('Every derivative of this class should overrride this method.')

    def max(self) -> [int]:
        '''Calculate the maximum roll of this roll part.'''
        raise NotImplemented('Every derivative of this class should overrride this method.')

    def avg(self) -> [float]:
        '''Calculate the average roll of this roll part.'''
        raise NotImplemented('Every derivative of this class should overrride this method.')
