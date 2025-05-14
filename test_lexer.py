import unittest
from lexer import doLex, TokenTypes


class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = doLex(code)
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', [[]])

    def test_space(self):
        self.lexer_test(' ', [[]])

    def test_label(self):
        self.lexer_test('abc', [[('abc', TokenTypes.LABEL)]])

    def test_keyword_if(self):
        self.lexer_test('if', [[('if', TokenTypes.RESERVED)]])
        self.lexer_test('endif', [[('endif', TokenTypes.RESERVED)]])
    
    def test_keyword_while(self):
        self.lexer_test('while', [[('while', TokenTypes.RESERVED)]])
        self.lexer_test('while', [[('while', TokenTypes.RESERVED)]])

    def test_keyword_print(self):
        self.lexer_test('print', [[('print', TokenTypes.RESERVED)]])
        self.lexer_test('print a', [[('print', TokenTypes.RESERVED), ('a', TokenTypes.LABEL)]])

    def test_id_space(self):
        self.lexer_test('abc  :=  5', [[('abc', TokenTypes.LABEL), (':=', TokenTypes.RESERVED), ('5', TokenTypes.DIGIT)]])

        
    
    
