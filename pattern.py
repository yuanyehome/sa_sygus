import copy
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

    def hasFunc(self, l):
        if self.funcDef[0] in l:
            return True, l
        for ele in l:
            if type(ele) == list:
                b, retl = self.hasFunc(ele)
                if b:
                    return True, retl
        return False

    def replaceCons(self, l, argMap):
        for i in range(len(l)):
            if type(l[i]) == list:
                self.replaceCons(l[i], argMap)
            elif argMap.has_key(l[i]):
                l[i] = argMap[l[i]]

    def preProcessCons(self):
        for cons in self.allCons:
            b, retl = self.hasFunc(cons)
            argMap = {}
            for i in range(1, len(retl)):
                argMap[retl[i]] = self.funcArgs[i - 1]
            self.replaceCons(cons, argMap)


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
