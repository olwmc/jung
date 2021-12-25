# Lexer for stack machine assignment 3

import re

token_specs = [
#   type:          value:
    ('CALL',       r'call'),
    ('RETURN',     r'return'),
    ('PUSH_FRAME', r'push_frame'),
    ('POP_FRAME',  r'pop_frame'),
    ('POP',        r'pop'),
    ('PUSH',       r'push'),
    ('PRINT_STR',  r'print_str'),
    ('PRINT',      r'print'),
    ('NEWLINE',    r'newline'),
    ('STORE',      r'store'),
    ('ASK',        r'ask'),
    ('DUP',        r'dup'),
    ('JUMPT',      r'jumpt'),
    ('JUMPF',      r'jumpf'),
    ('JUMP',       r'jump'),
    ('STOP',       r'stop'),
    ('NOOP',       r'noop'),

    ('ADD',        r'add'),
    ('SUB',        r'sub'),
    ('MUL',        r'mul'),
    ('DIV',        r'div'),
    ('MOD',        r'mod'),
    
    ('EQU',        r'equ'),
    ('NEQ',        r'neq'),
    ('LT',         r'lt'),
    ('LEQ',        r'leq'),
    ('GT',         r'gt'),
    ('GEQ',        r'geq'),
    
    ('AND',        r'and'),
    ('OR',         r'or'),
    ('NOT',        r'not'),
#    ('XOR',        r'xor'),
    
    ('NUMBER',     r'[+-]?([0-9]*[.])?[0-9]+'),
    ('NAME',       r'[a-zA-Z_\$][a-zA-Z0-9_\$]*'),
    ('MSG',        r'"([^"]|\\"|\\)*"'),
    ('SEMI',       r';'),
    ('COLON',      r':'),
    ('COMMENT',    r'#.*'),
    ('WHITESPACE', r'[ \t\n]+'),
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
