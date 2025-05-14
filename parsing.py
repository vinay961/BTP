from lexer import TokenTypes

class Parser():
    """Parse tokens and produce syntactic tree.
    
    Input: list of tokens
    Output: syntactic tree
    
    """
    
    def __init__(self):
        self.tokenlist = []
        self.tokenline = []
        self.currtoken = ("", "", 0)
        self.symboltable = dict()
        self.line_num = 0
    
    def parseTokens(self, tokenList):
        self.tokenlist = tokenList
        self._nextToken()
        return self._doStatementList()
    
    def getSymbolTable(self):
        return self.symboltable
    
    def _nextToken(self):
        
        if not self.tokenline:
            self.tokenline = self.tokenlist.pop(0)
            self.line_num += 1
        
        if(len(self.tokenline) > 0):
            s, type = self.tokenline.pop(0)
            if type == TokenTypes.RESERVED:
                self.currtoken = (s, "", 0)
            elif type == TokenTypes.DIGIT:
                self.currtoken = ("digit", "", int(s))
            elif type == TokenTypes.LABEL:
                self.symboltable[s] = 0
                self.currtoken = ("label", s, 0)
            else:
                print("syntax error: %s at line %d" % (s, self.line_num)) 
        else:
            self.currtoken = ("", "", 0)
    
    def consume(self, expected):
        if self.currtoken[0] == expected:
            self._nextToken()
        else:
            print("Expected " + expected + " not found on line " + str(self.line_num))
            exit(1)
    
    def _doStatementList(self):
        stmts = []
        newstmt = []
        
        while self.currtoken[0] in ["while", "if", "print", "label"]:
            if self.currtoken[0] == "while":
                # ["while", [condition], [statementlist]]
                self.consume("while")
                newstmt = ["while"]
                newstmt.append(self._doCondition())
                newstmt.append(self._doStatementList())
                self.consume("endwhile")
            elif self.currtoken[0] == "if":
                # ["if", [condition], [then part], [else part]]
                self.consume("if")
                newstmt = ["if"]
                newstmt.append(self._doCondition())
                newstmt.append(self._doStatementList())
                if self.currtoken[0] == "else":
                    self.consume("else")
                    newstmt.append(self._doStatementList())
                self.consume("endif")
            elif self.currtoken[0] == "print":
                # ["print", [expression]]
                self.consume("print")
                newstmt = ["print"]
                newstmt.append(self._doExpression())
            elif self.currtoken[0] == "label":
                # [":=", [expression], [expression]]
                label = [self.currtoken[1]]
                self._nextToken()
                self.consume(":=")
                newstmt = [":="]
                newstmt.append(label)
                newstmt.append(self._doExpression())
            else:
                print("Invalid statement: " + self.currtoken[0] + " on line " + str(self.line_num))
            stmts.append(newstmt)
        return stmts
    
    def _doCondition(self):
        exp = self._doExpression()
        # ["==|!=|<|<=|>|>=", [left side], [right side]]
        if self.currtoken[0] in ["==", "!=", "<", "<=", ">", ">="]:
            retval = [self.currtoken[0]]
            retval.append(exp)
            self._nextToken()
            retval.append(self._doExpression())
        else:
            print("Expected ==, !=, <, <=, > or >= not found")
        return retval
        
    def _doExpression(self):
        term = self._doTerm()
        # carry the term in case there's no +|-|*|/
        exp = term
        # ["+|-|*|/", [left side], [right side]]
        while self.currtoken[0] in ["+", "-", "*", "/"]:
            exp = [self.currtoken[0]]
            self._nextToken()
            exp.append(term)
            exp.append(self._doExpression())
        return exp
    
    def _doTerm(self):
        if self.currtoken[0] == "label":
            retval = self.currtoken[1]
            self._nextToken()
        elif self.currtoken[0] == "digit":
            retval = self.currtoken[2]
            self._nextToken()
        else:
            print("Wrong term '%s' at line %d" % (self.currtoken[0], self.line_num))
            exit(1)
        return [retval]