import os
from roll_part_list import PartSum
from dice_pool import Dice
from modifier import Modifier

class FormulaDatabase:
    DEFAULT_PATH = 'formulas'
    FILE_EXT = 'txt'
    
    def __init__(self, path :str =DEFAULT_PATH):
        if not isinstance(path,str):
            raise TypeError('\'path\' must be a string representing a directory, not a '+str(type(path)))
        if os.path.extsep in path:
            raise ValueError('\'path\' must not contain '+repr(os.extsep))
        os.makedirs(path,exist_ok=True)
        self.path = path

    def __repr__(self) ->str:
        if self.path == FormulaDatabase.DEFAULT_PATH:
            path = ''
        else:
            path = repr(self.path)
        return 'FormulaDatabase('+path+')'

    def __len__(self) ->int:
        return len(os.listdir(self.path))

    def __eq__(self, other) ->bool:
        if not isinstance(other, FormulaDatabase):
            raise TypeError('FormulaDatabases can only be compared to other FormulaDatabases, not a '+str(type(other)))
        return self.path == other.path

    def __ne__(self, other) ->bool:
        return not self == other

    def __getitem__(self, key :str) ->PartSum:
        if not isinstance(key, str):
            raise TypeError('\'key\' must be a string, not a '+str(type(key)))
        try:
            return self.load(key)
        except FileNotFoundError:
            raise KeyError('formula named '+repr(key)+' not found')

    def __setitem__(self, key :str, value :PartSum):
        if not isinstance(key, str):
            raise TypeError('\'key\' must be a string, not a '+str(type(key)))
        if not isinstance(value, PartSum):
            raise TypeError('\'value\' must be a PartSum, not a '+str(type(value)))
        self.save(key, value, True)

    def __delitem__(self, key :str):
        if not isinstance(key, str):
            raise TypeError('\'key\' must be a string, not a '+str(type(key)))
        try:
            self.remove(key)
        except FileNotFoundError:
            raise KeyError('formula named '+repr(key)+' not found')

    def __iter__(self):
        contents = os.listdir(self.path)
        keys = []
        for file in contents:
            if os.path.extsep + FormulaDatabase.FILE_EXT in file and os.path.pathsep not in file and os.path.altsep not in file:
                keys.append(os.path.splitext(file)[0])
        return iter(keys)

    def save(self, name :str, formula :PartSum, overwrite_ok :bool =True):
        '''Save a given formula to the database.'''
        if not isinstance(name, str):
            raise TypeError('\'name\' must be a string name of the saved formula, not a '+str(type(name)))
        if not isinstance(formula, PartSum):
            raise TypeError('\'formula\' must be a PartSum instance, not a '+str(type(formula)))
        if not isinstance(overwrite_ok, bool):
            raise TypeError('\'overwrite_ok\' must be a boolean, not a '+str(type(overwrite_ok)))
        if os.path.extsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.extsep))
        if os.path.pathsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.pathsep))
        if os.path.altsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.altsep))
        file = name + os.path.extsep + FormulaDatabase.FILE_EXT
        path = os.path.join(self.path, file)
        if file in os.listdir(self.path):
            if overwrite_ok:
                writer = open(path, 'wt')
            else:
                raise FileExistsError('An entry for the name '+repr(name)+' already exists')
        else:
            writer = open(path, 'xt')
        writer.write(repr(formula))
        writer.close()

    def load(self, name :str) ->PartSum:
        '''Attempt to load a formula from the database given the formula name.'''
        if not isinstance(name,str):
            raise TypeError('\'name\' must be a string name of the requested formula, not a '+str(type(name)))
        if os.path.extsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.path.extsep))
        if os.path.pathsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.path.pathsep))
        if os.path.altsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.path.altsep))
        file = name + os.path.extsep + FormulaDatabase.FILE_EXT
        path = os.path.join(self.path, file)
        if not file in os.listdir(self.path):
            raise FileNotFoundError('Could not find the requested formula in '+repr(self.path))
        reader = open(path, 'rt')
        result = eval(reader.read(), {'PartSum':PartSum, 'Dice':Dice, 'Modifier':Modifier})
        reader.close()
        if not isinstance(result, PartSum):
            raise Exception(repr(path)+' did not return a formula')
        return result

    def remove(self, name :str):
        '''Attempt to remove a formula from the database given the formula name.'''
        if not isinstance(name, str):
            raise TypeError('\'name\' must be a string name of the requested formula, not a '+str(type(name)))
        if os.path.extsep in name:
            raise ValueError('\'name\' must not contain '+repr(os.path.extsep))
        if os.path.pathsep in name:
            raise TypeError('\'name\' must not contain '+repr(os.path.pathsep))
        if os.path.altsep in name:
            raise TypeError('\'name\' must not contain '+repr(os.path.altsep))
        file = name + os.path.extsep + FormulaDatabase.FILE_EXT
        path = os.path.join(self.path, file)
        if not file in os.listdir(self.path):
            raise FileNotFoundError('Could not find the requiested formula in '+repr(self.path))
        os.remove(path)

if __name__ == '__main__':
    assert repr(FormulaDatabase(FormulaDatabase.DEFAULT_PATH)) == 'FormulaDatabase()'
    assert repr(FormulaDatabase('dice functions')) == 'FormulaDatabase(\'dice functions\')'
    assert len(FormulaDatabase('dice functions')) == 0
    FormulaDatabase('dice functions').save('test',PartSum([Dice(1,6)]))
    assert 'test'+os.path.extsep+FormulaDatabase.FILE_EXT in os.listdir('dice functions')
    assert 'test' in FormulaDatabase('dice functions')
    assert FormulaDatabase('dice functions').load('test') == PartSum([Dice(1,6)])
    assert FormulaDatabase('dice functions')['test'] == PartSum([Dice(1,6)])
    assert len(FormulaDatabase('dice functions')) == 1
    assert 'test' in FormulaDatabase('dice functions')
    FormulaDatabase('dice functions')['double test'] = PartSum([Dice(2,6)])
    assert len(FormulaDatabase('dice functions')) == 2
    FormulaDatabase('dice functions').save('test',PartSum([Dice(1,20)]))
    assert FormulaDatabase('dice functions')['test'] == PartSum([Dice(1,20)])
    FormulaDatabase('dice functions').remove('double test')
    assert 'double test' not in FormulaDatabase('dice functions')
    del FormulaDatabase('dice functions')['test']
    assert 'test' not in FormulaDatabase('dice functions')
    assert FormulaDatabase() == FormulaDatabase(FormulaDatabase.DEFAULT_PATH)
    assert FormulaDatabase() != FormulaDatabase('dice functions')
    #clean up
    os.rmdir('dice functions')
    os.rmdir(FormulaDatabase.DEFAULT_PATH)
