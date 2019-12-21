cmp_symbols = ['<', '<=', '>=', '>']


class PreConstrain:
    allCons = []
    funcDef = []
    funcArgs = []
    decVars = []

    def __init__(self):
        pass

    def processFunc(self, expr):
        self.funcDef.append(expr[1])
        for arg in expr[2]:
            self.funcDef.append(arg[0])
            self.funcArgs.append(arg[0])

    def preProcessCons(self):
        pass


class ConstrainPattern:
    cmp_cons = []
    eq_cons = []
    imply_cons = []
    logic_cons = []

    def __init__(self):
        pass

    def getPattern(self, constrains):
        pass

    def buildGuess(self):
        pass
