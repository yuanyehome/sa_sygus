import sys
import sexp
import pprint
import translator
from multiset import *
default_file = 'max2.sl'
exchange_symbol = ['+', '*', 'and', '=']
searched_set = set()
log_file = open('log.txt', 'w')
tmp_cnt = 0
all_cnt = 0


def Extend(Stmts, Productions):
    ret = []
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            TryExtend = Extend(Stmts[i], Productions)
            if len(TryExtend) > 0:
                for extended in TryExtend:
                    ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        elif Productions.has_key(Stmts[i]):
            for extended in Productions[Stmts[i]]:
                ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        if len(ret) > 0:
            return ret
    return ret


def stripComments(bmFile):
    noComments = '('
    for line in bmFile:
        line = line.split(';', 1)[0]
        noComments += line
    return noComments + ')'


if __name__ == '__main__':
    file_name = 'open_tests/' + default_file
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
    benchmarkFile = open(file_name)
    bm = stripComments(benchmarkFile)
    bmExpr = sexp.sexp.parseString(bm, parseAll=True).asList()[
        0]  # Parse string to python list
    # pprint.pprint(bmExpr)
    checker, is_ite_prior = translator.ReadQuery(bmExpr)
    #print (checker.check('(define-fun f ((x Int)) Int (mod (* x 3) 10)  )'))
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
                Productions[NTName].append(str(NT[1]))
            elif type(NT) == list and NT[0] == 'ite' and is_ite_prior:
                Productions[NTName].insert(0, NT)
            else:
                Productions[NTName].append(NT)
    Count = 0
    while(len(BfsQueue) != 0):
        Curr = BfsQueue.pop(0)
        # print("Extending "+str(Curr))
        TryExtend = Extend(Curr, Productions)
        if(len(TryExtend) == 0):  # Nothing to extend
            # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
            CurrStr = translator.toString(Curr)
            # SynFunResult = FuncDefine+Curr
            # Str = translator.toString(SynFunResult)
            # insert Program just before the last bracket ')'
            Str = FuncDefineStr[:-1]+' ' + CurrStr+FuncDefineStr[-1]
            Count += 1
            # print (Count)
            # print (Str)
            # if Count % 100 == 1:
            # print (Count)
            # print (Str)
            # raw_input()
            # print '1'
            counterexample = checker.check(Str)
            # print counterexample
            if(counterexample == None):  # No counter-example
                Ans = Str
                break
            # print '2'
        # print(TryExtend)
        # raw_input()
        # BfsQueue+=TryExtend
        TE_set = set()
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
                print >> log_file, TE_str
                TE_set.add(TE_str)

    print(Ans)

    # Examples of counter-examples
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int 0)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int x)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (+ x y))'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (ite (<= x y) y x))'))
