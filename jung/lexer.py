# Lexer for stack machine assignment 3

import re

token_specs = [
#   type:          value:
    ('PRINT',      r'\bprint\b'),
    ('STORE',      r'\bstore\b'),
    ('DEFUN',      r'\bdefun\b'),
    ('COND',       r'\bcond\b'),
    ('ASK',        r'\bask\b'),
    ('RETURN',     r'\breturn\b'),
    ('FOR',        r'\bfor\b'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LBRACKET',   r'\['),
    ('RBRACKET',   r'\]'),

    ('ADD',        r'\+'),
    ('MUL',        r'\*'),
    ('DIV',        r'/'),
    ('MOD',        r'%'),
    
    ('NEQ',        r'!='),
    ('LEQ',        r'<='),
    ('LT',         r'<'),
    ('GEQ',        r'>='),
    ('GT',         r'>'),
    
    ('EQ',        r'='),
    
    ('AND',        r'and'),
    ('OR',         r'or'),
    ('NOT',        r'not'),
    ('XOR',        r'xor'),

    ('BOOL',       r'\bTrue\b|\bFalse\b'),
    ('NUM',        r'[+-]?([0-9]*[.])?[0-9]+'),

    ('SUB',        r'-'),
    
    ('NAME',       r'[a-zA-Z_\$][a-zA-Z0-9_\$]*'),
    ('STRING',     r'"([^"]|\\"|\\)*"'),
    ('WHITESPACE', r'[ \t\n]+'),
    ('COMMENT',    r'#.*'),
    ('UNKNOWN',    r'.'),
]

# used for sanity checking in lexer.
token_types = set(type for (type,_) in token_specs)

class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({},{})'.format(self.type,self.value)

def tokenize(code):
    tokens = []
    re_list = ['(?P<{}>{})'.format(type,re) for (type,re) in token_specs]
    combined_re = '|'.join(re_list)
    match_object_list = list(re.finditer(combined_re, code))
    for mo in match_object_list:
        type = mo.lastgroup
        value = mo.group()
        if type == 'MSG':
            # delete the quotes
            value = value[1:-1]
        if type in ['WHITESPACE','COMMENT']:
            continue #ignore
        elif type == 'UNKNOWN':
            raise ValueError("unexpected character '{}'".format(value))
        else:
            tokens.append(Token(type, value))
    tokens.append(Token('EOF', '\eof'))
    return tokens

class Lexer:
    def __init__(self, input_string):
        self.tokens = tokenize(input_string)
        # the following is always valid because we will always have
        # at least the EOF token on the tokens list.
        self.curr_token_ix = 0

    def pointer(self):
        return self.tokens[self.curr_token_ix]

    def next(self):
        if not self.end_of_file():
            self.curr_token_ix += 1
        return self.pointer()

    def match(self, token_type):
        if token_type == self.pointer().type:
            tk = self.pointer()
            self.next()
            return tk
        elif token_type not in token_types:
            raise ValueError("unknown token type '{}'".format(token_type))
        else:
            for t in self.tokens:
                print(t)
            raise SyntaxError('unexpected token {} while parsing, expected {}'
                              .format(self.pointer().type, token_type))

    def end_of_file(self):
        if self.pointer().type == 'EOF':
            return True
        else:
            return False