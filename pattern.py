import copy
cmp_symbol = ['<', '<=', '>=', '>']
logic_symbol = ['and', 'or', '=>', 'not']


def changeSymbol(l):
    if not type(l) == list:
        return
    if l[0] in cmp_symbol and l[0][0] == '<':
        l[0] = l[0].replace('<', '>')
        l[1], l[2] = l[2], l[1]
    for item in l:
        changeSymbol(item)


def checkSymbol(l, funcDef):
    if l[0] == '=>':
        return checkSymbol(l[2], funcDef)
    elif l[0] == '=':
        return (not type(l[1]) == list and str(l[2]) == str(funcDef)) \
            or (not type(l[2]) == list and str(l[1]) == str(funcDef))
    return False


def processOne(cond, then, item, funcDef):
    if item[0] == '=>':
        if item[2][0] == '=':
            cond.append(item[1])
            if str(item[2][1] == str(funcDef)):
                then.append(item[2][2])
            else:
                then.append(item[2][1])
        else:
            cond.append(item[1])
            cond.append(['and'])
            processOne(cond[2], then, item[2], funcDef)


def clean(cur_ret):
    ele = cur_ret[2][0]
    if type(ele) == tuple:
        cur_ret[2] = str(ele[1])
    ele = cur_ret[1]
    while ele[0] == 'and' and len(ele) == 3:
        if len(ele[2]) == 2:
            ele[2] = ele[2][1]
            break
        ele = ele[2]


def getVal(cur_cons, funcDef):
    ele = cur_cons
    while not ele[0] == '=':
        ele = ele[2]
    if str(ele[1]) == str(funcDef):
        return str(ele[2][1])
    else:
        return str(ele[1][1])


def getImplyGuess(l, funcDef):
    ret = []
    cur_ret = ret
    for i in range(len(l)):
        item = l[i]
        cur_ret.append('ite')
        cur_ret.append(['and'])
        cur_ret.append([])
        processOne(cur_ret[1], cur_ret[2], item, funcDef)
        clean(cur_ret)
        if i == len(l) - 2:
            cur_ret.append(getVal(l[i + 1], funcDef))
            break
        cur_ret.append([])
        cur_ret = cur_ret[3]
    # print ret
    return ret


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
    allCons = PreConstrain()

    def __init__(self, preCons):
        self.preConstrain = preCons

    def getPattern(self, constrains):
        self.allCons = constrains
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

    def buildCond(self, left, idx):
        cond = []
        if idx == len(self.cmp_cons) - 1:
            cond.append(self.cmp_cons[idx][0])
            cond.append(left)
            cond.append(self.cmp_cons[idx][2])
            return cond
        cond.append("and")
        cond.append([self.cmp_cons[idx][0], left, self.cmp_cons[idx][2]])
        cond.append(self.buildCond(left, idx + 1))
        return cond

    def buildCmpGuess(self, idx):
        cond = []
        cond.append("ite")
        cond.append(self.buildCond(self.preConstrain.funcArgs[idx], 0))
        cond.append(self.preConstrain.funcArgs[idx])
        if idx == len(self.preConstrain.funcArgs) - 2:
            cond.append(self.preConstrain.funcArgs[idx + 1])
        else:
            cond.append(self.buildCmpGuess(idx + 1))
        return cond

    def buildGuess(self):
        # TODO: check whether symbol appears in grammar finally
        if (len(self.imply_cons) > 0):
            # array_search
            changeSymbol(self.imply_cons)
            for cons in self.imply_cons:
                if not checkSymbol(cons, self.allCons.funcDef):
                    self.imply_cons.remove(cons)
            return getImplyGuess(self.imply_cons, self.allCons.funcDef)
        elif (len(self.cmp_cons) > 0):
            ret = self.buildCmpGuess(0)
            return [ret]
        else:
            if (len(self.eq_cons) > 0):
                # process eq
                pass
            if (len(self.logic_cons) > 0):
                # process logic
                pass
