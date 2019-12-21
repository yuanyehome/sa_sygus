import copy
cmp_symbol = ['<', '<=', '>=', '>']
logic_symbol = ['and', 'or', '=>', 'not']


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
            argMap = {}
            for i in range(1, len(l)):
                argMap[l[i]] = self.funcArgs[i - 1]
            return True, argMap
        for ele in l:
            if type(ele) == list:
                b, argMap = self.hasFunc(ele)
                if b:
                    return True, argMap
        return False, {}

    def replaceCons(self, l, argMap):
        for i in range(len(l)):
            if type(l[i]) == list:
                self.replaceCons(l[i], argMap)
            elif argMap.has_key(l[i]):
                l[i] = argMap[l[i]]

    def preProcessCons(self):
        for cons in self.allCons:
            b, argMap = self.hasFunc(cons)
            if b:
                self.replaceCons(cons, argMap)


class ConstrainPattern:
    cmp_cons = []
    eq_cons = []
    imply_cons = []
    logic_cons = []

    def __init__(self):
        pass

    def getPattern(self, constrains):
        for consItem in constrains.allCons:
            assert consItem[0] == 'constraint'
            if consItem[1][0] in cmp_symbol:
                if consItem[1][0][0] == '<':
                    consItem[1][1], consItem[1][2] = consItem[1][2], consItem[1][1]
                consItem[1][0] = consItem[1][0].replace('<', '>')
                self.cmp_cons.append(consItem[1])
            elif consItem[1][0] == '=>':
                self.imply_cons.append(consItem[1])
            elif consItem[1][0] in logic_symbol:
                self.logic_cons.append(consItem[1])
            elif consItem[1][0] == '=':
                self.eq_cons.append(consItem[1])

    def buildGuess(self):
        # TODO: check whether symbol appears in grammar finally
        if (len(self.imply_cons) > 0):
            # array_search
            pass
        elif (len(self.cmp_cons) > 0):
            # max
            pass
        else:
            if (len(self.eq_cons) > 0):
                # process eq
                pass
            if (len(self.logic_cons) > 0):
                # process logic
                pass
