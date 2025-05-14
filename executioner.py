

class Executioner():
    
    def __init__(self, symboltable):
        self.stack = []
        self.symboltable = symboltable
    
    def execStatementList(self, pgm):
        for stmt in pgm:
            self._execStatement(stmt)
            
    def _execStatement(self, stmt):
        if stmt[0] == "while":
            self._execCondition(stmt[1])
            while self.stack.pop():
                self.execStatementList(stmt[2])
                self._execCondition(stmt[1])
        elif stmt[0] == "if":
            self._execCondition(stmt[1])
            if self.stack.pop():
                self.execStatementList(stmt[2])
            elif len(stmt) == 4:
                self.execStatementList(stmt[3])
        elif stmt[0] == ":=":
            self._execExpression(stmt[2])
            self.symboltable[stmt[1][0]] = self.stack.pop()
        elif stmt[0] == "print":
            self._execExpression(stmt[1])
            print("Output:" + str(self.stack.pop()))
        else:
            print("Invalid statement!")
            exit()
        
    def _execCondition(self, cond):
        self._execExpression(cond[1])
        self._execExpression(cond[2])
        if cond[0] == "==":
            self.stack.append(self.stack.pop(0) == self.stack.pop(0))
        elif cond[0] == "!=":
            self.stack.append(self.stack.pop(0) != self.stack.pop(0))
        elif cond[0] == "<":
            self.stack.append(self.stack.pop(0) < self.stack.pop(0))
        elif cond[0] == "<=":
            self.stack.append(self.stack.pop(0) <= self.stack.pop(0))
        elif cond[0] == ">":
            self.stack.append(self.stack.pop(0) > self.stack.pop(0))
        elif cond[0] == ">=":
            self.stack.append(self.stack.pop(0) >= self.stack.pop(0))
    
    def _execExpression(self, exp):
        if len(exp) == 3:
            self._execExpression(exp[1])
            self._execExpression(exp[2])
            if exp[0] == "+":
                self.stack.append(self.stack.pop(0) + self.stack.pop(0))
            elif exp[0] == "-":
                self.stack.append(self.stack.pop(0) - self.stack.pop(0))
            elif exp[0] == "*":
                self.stack.append(self.stack.pop(0) * self.stack.pop(0))
            elif exp[0] == "/":
                self.stack.append(self.stack.pop(0) / self.stack.pop(0))
            else:
                print("Invalid operator %s!" % exp[0])
                exit(1)
        else:
            if type(exp[0]) is int:
                self.stack.append(exp[0])
            else:
                self.stack.append(self.symboltable[exp[0]])