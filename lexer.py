import re

class TokenTypes(object):
    RESERVED = 'RESERVED'
    DIGIT = 'DIGIT'
    LABEL = 'LABEL'

token_exprs = [
    (r'[ \n\t]',              None),
    #(r'#[^\n]*',               None),
    (r'\:=',                   TokenTypes.RESERVED),
    (r';',                     TokenTypes.RESERVED),
    (r'\+',                    TokenTypes.RESERVED),
    (r'-',                     TokenTypes.RESERVED),
    (r'\*',                    TokenTypes.RESERVED),
    (r'/',                     TokenTypes.RESERVED),
    (r'<',                     TokenTypes.RESERVED),
    (r'<=',                    TokenTypes.RESERVED),
    (r'>',                     TokenTypes.RESERVED),
    (r'>=',                    TokenTypes.RESERVED),
    (r'==',                    TokenTypes.RESERVED),
    (r'!=',                    TokenTypes.RESERVED),
    (r'and',                   TokenTypes.RESERVED),
    (r'or',                    TokenTypes.RESERVED),
    (r'not',                   TokenTypes.RESERVED),
    (r'if',                    TokenTypes.RESERVED),
    (r'then',                  TokenTypes.RESERVED),
    (r'else',                  TokenTypes.RESERVED),
    (r'endif',                 TokenTypes.RESERVED),
    (r'while',                 TokenTypes.RESERVED),
    (r'endwhile',              TokenTypes.RESERVED),
    (r'print',                 TokenTypes.RESERVED),
    (r'[0-9]+',                TokenTypes.DIGIT),
    (r'[A-Za-z][A-Za-z0-9_]*', TokenTypes.LABEL),
]

def lex(characters, token_exprs):
    """Devides input text to tokens, defined by token_exprs."""
    pos = 0
    tokens = []
    line_tokens = []
    line_num = 1
    old_line_num = 1
    while pos < len(characters):
        
        if line_num != old_line_num:
            tokens.append(line_tokens)
            line_tokens = []
            old_line_num = line_num
        
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if is_newline(text):
                    line_num += 1
                if tag is not None:
                    token = (text, tag)
                    line_tokens.append(token)
                break
        if not match:
            print('Illegal character: %s at line %d' % (characters[pos], line_num))
            exit(1)
        else:
            #set current position just after matched token
            pos = match.end(0)
            
    tokens.append(line_tokens)
    return tokens

def is_newline(str):
    regex = re.compile(r'[\n]')
    match = regex.match(str)
    if match:
        return True
    return False

def doLex(characters):
    return lex(characters, token_exprs)