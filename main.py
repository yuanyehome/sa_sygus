import sys
import sexp
import pprint
import translator
import time
from multiset import *
from pattern import *
# default_file = 'max2.sl'
# default_file = 'max15.sl'
# default_file = 'three.sl'
# default_file = 'my_test.sl'
# default_file = 'tutorial.sl'
default_file = 'array_sum_7_15.sl'
# default_file = 'array_search_2.sl'
exchange_symbol = ['+', '*', 'and', '=']
compare_symbol = ['>', '<', '>=', '<=']
var_symbol = []
searched_set = set()
log_file = open('log.txt', 'w')
log_ter_file = open('log_ter.txt', 'w')
tmp_cnt = 0
all_cnt = 0
firstFlag = True
has_ge_le = False
has_g_l = False

# the following three functions are used for const condition check


def genVarSymbol(SynFunExpr):
    var_symbol.append([item[0] for item in SynFunExpr[2]])
    var_symbol.append([item[0] for item in SynFunExpr[4]])


def condDetCheck(Stmts):
    flag = False
    if type(Stmts) != list:
        return flag
    if Stmts[0] in cmp_symbol and Stmts[1] == Stmts[2] and Stmts[1] in var_symbol[0]:
        return True
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            if condDetCheck(Stmts[i]):
                flag = True
    return flag


def iteDetCheck(Stmts):
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            if iteDetCheck(Stmts[i]):
                return True
        elif Stmts[i] == 'ite':
            if condDetCheck(Stmts[i + 1]):
                return True
    return False


def Extend(Stmts, Productions, depth=0):
    ret = []
    global firstFlag
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            TryExtend = Extend(Stmts[i], Productions)
            if len(TryExtend) > 0:
                for extended in TryExtend:
                    ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        elif Productions.has_key(Stmts[i]):
            for extended in Productions[Stmts[i]]:
                # if extended[0] == 'ite' and depth == 0:
                #     tmp_ret = []
                #     tmp_ret.append(Extend([extended[1]], Productions, 1))
                #     tmp_ret.append(Extend([extended[2]], Productions, 1))
                #     tmp_ret.append(Extend([extended[3]], Productions, 1))
                #     for i1 in range(len(tmp_ret[0])):
                #         for i2 in range(len(tmp_ret[1])):
                #             for i3 in range(len(tmp_ret[2])):
                #                 ret.append(
                #                     Stmts[0:i] + ['ite', tmp_ret[0][i1],
                #                                   tmp_ret[1][i2], tmp_ret[2][i3]] + Stmts[i+1:])
                # else:
                ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        if len(ret) > 0:
            # if firstFlag and type(ret[0][0]) == list and ret[0][0][0] == 'ite':
            #     tmp_ret_new = copy.deepcopy(ret[0][0])
            #     tmp_ret = tmp_ret_new
            #     while depth > 0:
            #         tmp_ret[1] = ['<=', 'x', 'y']
            #         tmp_ret[2] = copy.deepcopy(Productions['Start'][0])
            #         tmp_ret = tmp_ret[2]
            #         tmp_ret[1] = ['=', 'x', 'y']
            #         depth -= 1
            #     firstFlag = False
            #     ret.insert(0, [tmp_ret_new])
            return ret
    return ret


def stripComments(bmFile):
    noComments = '('
    for line in bmFile:
        line = line.split(';', 1)[0]
        noComments += line
    return noComments + ')'


if __name__ == '__main__':
    TE_set = set()
    begin_t = time.time()
    file_name = 'open_tests/' + default_file
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
    benchmarkFile = open(file_name)
    bm = stripComments(benchmarkFile)
    bmExpr = sexp.sexp.parseString(bm, parseAll=True).asList()[
        0]  # Parse string to python list
    # pprint.pprint(bmExpr)
    checker, is_ite_prior, is_cmp_prior, preCons = translator.ReadQuery(bmExpr)
    # print (checker.check('(define-fun f ((x Int)) Int (mod (* x 3) 10)  )'))
    # raw_input()
    SynFunExpr = []
    StartSym = 'My-Start-Symbol'  # virtual starting symbol
    for expr in bmExpr:
        if len(expr) == 0:
            continue
        elif expr[0] == 'synth-fun':
            SynFunExpr = expr
    FuncDefine = ['define-fun']+SynFunExpr[1:4]  # copy function signature
    FuncDefineStr = translator.toString(FuncDefine, ForceBracket=True)
    # print(FuncDefine)
    BfsQueue = [[StartSym]]  # Top-down
    Productions = {StartSym: []}
    Type = {StartSym: SynFunExpr[3]}  # set starting symbol's return type

    genVarSymbol(SynFunExpr)

    pattern = ConstrainPattern(preCons)
    pattern.getPattern(preCons)
    limit_cnt = len(preCons.allCons)*2000
    for NonTerm in SynFunExpr[4]:  # SynFunExpr[4] is the production rules
        NTName = NonTerm[0]
        NTType = NonTerm[1]
        if NTType == Type[StartSym]:
            Productions[StartSym].append(NTName)
        Type[NTName] = NTType
        # Productions[NTName] = NonTerm[2]
        Productions[NTName] = []
        for NT in NonTerm[2]:
            if type(NT) == tuple:
                # deal with ('Int',0). You can also utilize type information, but you will suffer from these tuples.
                if NT[1] not in pattern.numbers:
                    continue
                Productions[NTName].append(str(NT[1]))
            elif type(NT) == list and NT[0] == 'ite' and is_ite_prior:
                Productions[NTName].insert(0, NT)
            elif type(NT) == list and NT[0] in compare_symbol and is_cmp_prior:
                Productions[NTName].insert(0, NT)
            else:
                if type(NT) == list and NT[0] in ['>=', '<='] and has_ge_le:
                    continue
                if type(NT) == list and NT[0] in ['>=', '<=']:
                    has_ge_le = True
                if type(NT) == list and NT[0] in ['>', '<'] and has_g_l:
                    continue
                if type(NT) == list and NT[0] in ['>', '<']:
                    has_g_l = True
                if type(NT) == list and NT[0] in math_symbol and \
                        len(pattern.mathSymbols) == 0:
                    continue
                Productions[NTName].append(NT)
    Count = 0
    CountX = 0
    flag = True

    # firstGuess = pattern.buildGuess()
    success = False
    # if firstGuess != None:
    #     # print firstGuess
    #     firstGuess = translator.toString(firstGuess)
    #     Str = FuncDefineStr[:-1]+' ' + firstGuess+FuncDefineStr[-1]
    #     print Str
    #     if (checker.check(Str) == None):
    #         success = True
    #         Ans = Str
    try:
        while(len(BfsQueue) != 0 and not success):
            CountX += 1
            Curr = BfsQueue.pop(0)
            # print("Extending "+str(Curr))
            TryExtend = Extend(Curr, Productions, pattern.numCall - 2)
            for Stmt in TryExtend:
                if iteDetCheck(Stmt):
                    TryExtend.remove(Stmt)
            if(len(TryExtend) == 0):  # Nothing to extend
                # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE    ARGUMENT ForceBracket = True.
                CurrStr = translator.toString(Curr)
                # SynFunResult = FuncDefine+Curr
                # Str = translator.toString(SynFunResult)
                # insert Program just before the last bracket ')'
                Str = FuncDefineStr[:-1]+' ' + CurrStr+FuncDefineStr[-1]
                Count += 1
                # print (Count)
                # print Curr
                # print (Str)
                # if Count % 100 == 1:
                # print (Count)
                # print (Str)
                # raw_input()
                # print '1'
                # print >> log_ter_file, Str
                counterexample = checker.check(Str)
                # print counterexample
                if(counterexample == None):  # No counter-example
                    Ans = Str
                    break
                # print '2'
            # print(TryExtend)
            # raw_input()
            # BfsQueue+=TryExtend
            if CountX >= limit_cnt and flag:
                finalGuess = pattern.buildGuess()
                if finalGuess != None:
                    finalGuess = translator.toString(finalGuess)
                    Str = FuncDefineStr[:-1]+' ' + finalGuess+FuncDefineStr[-1]
                    if (checker.check(Str) == None):
                        Ans = Str
                        break
                flag = False

            for TE in TryExtend:
                all_cnt += 1
                TE_str = str(TE)
                # if type(TE[0]) == list and TE[0][0] in exchange_symbol:
                #     tmp_TE = []
                #     for item in TE[0][1:]:
                #         tmp_TE.append(str(item))
                #     this_sym = str(Multiset(tmp_TE))
                #     if (this_sym in searched_set):
                #         tmp_cnt += 1
                #         continue
                #     searched_set.add(this_sym)
                # Don't delete it! It is useless now. But may be used in future!
                if not TE_str in TE_set:
                    BfsQueue.append(TE)
                    # print >> log_file, TE_str
                    TE_set.add(TE_str)
    except:
        finalGuess = pattern.buildGuess()
        if finalGuess != None:
            finalGuess = translator.toString(finalGuess)
            Str = FuncDefineStr[:-1]+' ' + finalGuess+FuncDefineStr[-1]
            if (checker.check(Str) == None):
                Ans = Str
    print(Ans)
    end_t = time.time()
    print "\033[32mPass time: \033[0m" + str(end_t - begin_t) + ' s'

    # Examples of counter-examples
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int 0)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int x)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (+ x y))'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (ite (<= x y) y x))'))
