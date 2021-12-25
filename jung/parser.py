stmt_body_lookahead = ['STORE', 'PRINT', 'NAME', 'FOR', 'DEFUN', 'RETURN', 'COND']
exp_lookahead = ['NAME', 'NUM', 'LPAREN', 'BOOL']

def prog(stream):
    return stmt_list(stream)

def stmt_list(stream):
    body = []
    while stream.pointer().type == 'LPAREN':
        stream.match('LPAREN')
        body.append(stmt_body(stream))
        stream.match('RPAREN')
    
    return ('STMTS', body)

def stmt_body(stream):
    tok = stream.pointer()

    if tok.type == 'STORE':
        return store_stmt(stream)
    elif tok.type == 'PRINT':
        return print_stmt(stream)
    elif tok.type == 'NAME':
        return call_stmt(stream)
    elif tok.type == 'FOR':
        return for_loop(stream)
    elif tok.type == 'DEFUN':
        return function_def(stream)
    elif tok.type == 'RETURN':
        return return_stmt(stream)
    elif tok.type == 'COND':
        return cond_stmt(stream)
    else:
        raise SyntaxError("Error at stmt_body: {}".format(tok.value))

def store_stmt(stream):
    stream.match('STORE')
    v = var(stream)
    e = exp(stream)
    
    return ('STORE', v, e)

def print_stmt(stream):
    stream.match('PRINT')

    args = []
    
    while stream.pointer().type in exp_lookahead + ['STRING']:
        if stream.pointer().type == 'LPAREN':
            args.append(exp(stream))
        
        elif stream.pointer().type == 'STRING':
            args.append(string(stream))
        
        elif stream.pointer().type == 'NAME':
            args.append(var(stream))
        
        elif stream.pointer().type == 'NUM':
            args.append(num(stream))

        elif stream.pointer().type == 'BOOL':
            args.append(boolean(stream))

    return ('PRINT', args)

def call_stmt(stream):
    v = var(stream)
    args = []

    while(stream.pointer().type in exp_lookahead):
        args.append(exp(stream))

    return ('CALL', v, args)

def invocation(stream):
    v = var(stream)
    args = []

    while(stream.pointer().type in exp_lookahead):
        args.append(exp(stream))

    return ('INVOCATION', v, args)

def for_loop(stream):
    stream.match('FOR')
    stream.match('LBRACKET')
    v = var(stream)
    stream.match('RBRACKET')

    start = exp(stream)
    end = exp(stream)

    body = stmt_list(stream)

    return ('FOR', v, start, end, body)

def function_def(stream):
    stream.match('DEFUN')
    v = var(stream)
    args = arglist(stream)
    body = stmt_list(stream)

    return ('DEFUN', v, args, body)

def return_stmt(stream):
    stream.match('RETURN')
    e = exp(stream)

    return ('RETURN', e)

def cond_stmt(stream):
    stream.match('COND')

    tests = []
    bodies = []

    while(stream.pointer().type in ['LPAREN']):
        stream.match('LPAREN')
        tests.append(exp(stream))
        bodies.append(stmt_list(stream))
        stream.match('RPAREN')

    return ('COND', ('TESTS', tests), ('BODIES', bodies))

def exp(stream):
    tok = stream.pointer()
    if tok.type == 'NUM':
        return num(stream)
    elif tok.type == 'NAME':
        return var(stream)

    elif tok.type == 'BOOL':
        return boolean(stream)

    elif tok.type == 'LPAREN':
        return paren_exp(stream)
    else:
        raise SyntaxError("Error at exp: {}".format(tok.value))

def paren_exp(stream):
    stream.match('LPAREN')
    tok = stream.pointer()

    if tok.type in  ['ADD','SUB', 'MUL', 'DIV', 'MOD']:
        e = arith_exp(stream)
        stream.match('RPAREN')
        return e
    
    elif tok.type in ['EQ', 'NEQ', 'LT', 'LEQ', 'GT', 'GEQ', 'AND', 'OR', 'NOT']:
        e = logic_exp(stream)
        stream.match('RPAREN')
        return e

    elif tok.type == 'ASK':
        stream.match('ASK')
        msg = None
        if stream.pointer().type == 'STRING':
            msg = string(stream)
        stream.match('RPAREN')
        return ('ASK', msg[1])

    elif tok.type in ['NAME']:
        e =  invocation(stream)
        stream.match("RPAREN")
        return e

    else:
        raise SyntaxError("Error at paren_exp: {}".format(tok.value))
    
    # Any other expression is invalid
    
def arith_exp(stream):
    tok = stream.pointer()

    if tok.type == 'ADD':
        stream.match('ADD')

        return ('ADD', exp(stream), exp(stream))
    
    elif tok.type == 'SUB':
        stream.match('SUB')

        return ('SUB', exp(stream), exp(stream))


    elif tok.type == 'MUL':
        stream.match('MUL')

        return ('MUL', exp(stream), exp(stream))
    
    elif tok.type == 'DIV':
        stream.match('DIV')

        return ('DIV', exp(stream), exp(stream))

    elif tok.type == 'MOD':
        stream.match('MOD')
        return ('MOD', exp(stream), exp(stream))

    else:
        raise SyntaxError("Error at arith_exp: {}".format(tok.value))

def logic_exp(stream):
    tok = stream.pointer()

    if tok.type == 'AND':
        stream.match('AND')

        return ('AND', exp(stream), exp(stream))

    elif tok.type == 'OR':
        stream.match('OR')

        return ('OR', exp(stream), exp(stream))
    
    elif tok.type == 'NOT':
        stream.match('NOT')
        
        return ('NOT', exp(stream))

    elif tok.type == 'LT':
        stream.match('LT')

        return ('LT', exp(stream), exp(stream))

    elif tok.type == 'LEQ':
        stream.match('LEQ')

        return ('LEQ', exp(stream), exp(stream))

    elif tok.type == 'GT':
        stream.match('GT')

        return ('GT', exp(stream), exp(stream))

    elif tok.type == 'GEQ':
        stream.match('GEQ')

        return ('GEQ', exp(stream), exp(stream))

    elif tok.type == 'EQ':
        stream.match('EQ')

        return ('EQ', exp(stream), exp(stream))

    elif tok.type == 'NEQ':
        stream.match('NEQ')

        return ('NEQ', exp(stream), exp(stream))
    else:
        raise SyntaxError("Error at logic_exp: {}".format(tok.value))

def var(stream):
    v = stream.pointer().value
    stream.match('NAME')

    return ('VAR', v)

def num(stream):
    v = stream.pointer().value
    stream.match('NUM')
    return ('NUM', v)

def boolean(stream):
    v = stream.pointer().value
    stream.match('BOOL')
    return ('BOOL', int(v=='True'))

def string(stream):
    s = stream.pointer().value
    stream.match('STRING')
    return ('STRING', s)

def arglist(stream):
    stream.match('LBRACKET')
    vs = []

    while(stream.pointer().type == 'NAME'):
        vs.append(var(stream))
    
    stream.match('RBRACKET')
    return ('ARGLIST', vs)

# parser top-level driver
def parse(char_stream=None):
    global __sym_tab__
    __sym_tab__ = dict()

    from jung.lexer import Lexer
    from jung.dumpast import dumpast

    ast = None

    token_stream = Lexer(char_stream)
    ast = prog(token_stream) # call the parser function for start symbol

    try:
        if not token_stream.end_of_file():
            raise SyntaxError("parse: syntax error at {}"
                            .format(token_stream.pointer().value))
    except Exception as e:
        print("error: " + str(e))

    return ast
