import sys

from lexer import doLex
from parsing import Parser
from executioner import Executioner
            
def main():
    
    # file name should be passed as command line argument, like this: python main.py test.txt
    if len(sys.argv) <= 1:
        print("Please enter file name to parse.")
        exit(0)
    
    #open file
    filename = sys.argv[1]
    inputstring = ""
    try:
        inputfile = open(filename, "r")
        inputstring = inputfile.read()
    except IOError:
        print("File '%s' cannot be open for reading." % filename)
        exit(1)
    
    #do lexical analysis
    tokenlist = doLex(inputstring)
    for tlist in tokenlist:
        for name, type in tlist:
            print("(%s, %s)" % (name, type))
    print 
    
    #parse
    parser = Parser()
    stmt = parser.parseTokens(tokenlist)
    for s in stmt:
        print(s)
    print()
    
    print(parser.getSymbolTable())
    print()
    
    #execute
    try:
        executioner = Executioner(parser.getSymbolTable())
        executioner.execStatementList(stmt)
    except Exception as e:
        print("Error at execution!")
        print(e)

if __name__ == "__main__":
    main()
