from stackmachine.stackmachine_interp_state import state

# lookahead sets for parser
instr_lookahead = [
    'PRINT_STR',
    'PRINT',
    'NEWLINE',
    'PUSH',
    'POP',
    'STORE',
    'ASK',
    'DUP',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'EQU',
    'NEQ',
    'AND',
    'OR',
    'NOT',
    'LT',
    'LEQ',
    'GT',
    'GEQ',
    'JUMPT',
    'JUMPF',
    'JUMP',
    'STOP',
    'CALL',
    'RETURN',
    'PUSH_FRAME',
    'POP_FRAME',
    'NOOP',
    ]
labeled_instr_lookahead = instr_lookahead + ['NAME']

def instr_list(stream):
  while stream.pointer().type in labeled_instr_lookahead:
    labeled_instr(stream)
  return None

def labeled_instr(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        l = label_def(stream)
        i = instr(stream)
        state.label_table[l] = state.call_stack.pointer()
        state.program.append(i)
        state.call_stack.next()
        return None
    elif token.type in instr_lookahead:
        i = instr(stream)
        state.program.append(i)
        state.call_stack.next()
        return None
    else:
        raise SyntaxError("labeled_instr: syntax error at {}"
                          .format(token.value))

def label_def(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        l = label(stream)
        stream.match('COLON')
        return l
    else:
        raise SyntaxError("label_def: syntax error at {}"
                          .format(token.value))

def instr(stream):
    token = stream.pointer()
    if token.type in ['PRINT']:
        stream.match('PRINT')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('PRINT', tk.value)
        else:
            t = ('PRINT', None)
        stream.match('SEMI')
        return t
    elif token.type in ['PRINT_STR']:
        stream.match('PRINT_STR')
        msg = stream.pointer().value
        stream.match('MSG')
        stream.match('SEMI')
        return ('PRINT_STR', msg)

    elif token.type in ['NEWLINE']:
        stream.match('NEWLINE')
        stream.match('SEMI')
        return ('NEWLINE',)

    elif token.type in ['PUSH']:
        stream.match('PUSH')
        if stream.pointer().type == 'NUMBER':
            e = num(stream)
        elif stream.pointer().type == 'NAME':
            e = var(stream)
        else:
            raise SyntaxError("push: syntax error at {}"
                              .format(stream.pointer().value))
        stream.match('SEMI')
        return ('PUSH', e)
    elif token.type in ['POP']:
        stream.match('POP')
        stream.match('SEMI')
        return ('POP',)
    elif token.type in ['STORE']:
        stream.match('STORE')
        v = var(stream)
        stream.match('SEMI')
        return ('STORE',v)
    elif token.type in ['ASK']:
        stream.match('ASK')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('ASK', tk.value)
        else:
            t = ('ASK', None)
        stream.match('SEMI')
        return t
    elif token.type in ['DUP']:
        stream.match('DUP')
        stream.match('SEMI')
        return ('DUP',)
    elif token.type in ['ADD']:
        stream.match('ADD')
        stream.match('SEMI')
        return ('ADD',)
    elif token.type in ['SUB']:
        stream.match('SUB')
        stream.match('SEMI')
        return ('SUB',)
    elif token.type in ['MUL']:
        stream.match('MUL')
        stream.match('SEMI')
        return ('MUL',)
    elif token.type in ['DIV']:
        stream.match('DIV')
        stream.match('SEMI')
        return ('DIV',)
    elif token.type in ['MOD']:
        stream.match('MOD')
        stream.match('SEMI')
        return ('MOD',)
    elif token.type in ['EQU']:
        stream.match('EQU')
        stream.match('SEMI')
        return ('EQU',)
    elif token.type in ['NEQ']:
        stream.match('NEQ')
        stream.match('SEMI')
        return ('NEQ',)
    elif token.type in ['AND']:
        stream.match('AND')
        stream.match('SEMI')
        return ('AND',)
    elif token.type in ['OR']:
        stream.match('OR')
        stream.match('SEMI')
        return ('OR',)
    elif token.type in ['NOT']:
        stream.match('NOT')
        stream.match('SEMI')
        return ('NOT',)
    elif token.type in ['LT']:
        stream.match('LT')
        stream.match('SEMI')
        return ('LT',)
    elif token.type in ['LEQ']:
        stream.match('LEQ')
        stream.match('SEMI')
        return ('LEQ',)
    elif token.type in ['GT']:
        stream.match('GT')
        stream.match('SEMI')
        return ('GT',)
    elif token.type in ['GEQ']:
        stream.match('GEQ')
        stream.match('SEMI')
        return ('GEQ',)
    elif token.type in ['JUMPT']:
        stream.match('JUMPT')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMPT', l)
    elif token.type in ['JUMPF']:
        stream.match('JUMPF')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMPF', l)
    elif token.type in ['JUMP']:
        stream.match('JUMP')
        l = label(stream)
        stream.match('SEMI')
        return ('JUMP', l)

    elif token.type in ['CALL']:
        stream.match('CALL')
        l = label(stream)
        stream.match('SEMI')
        return ('CALL', l)

    elif token.type in ["RETURN"]:
        stream.match('RETURN')
        stream.match('SEMI')
        return ('RETURN',)

    elif token.type in ["PUSH_FRAME"]:
        stream.match('PUSH_FRAME')
        stream.match('SEMI')
        return ('PUSH_FRAME',)

    elif token.type in ["POP_FRAME"]:
        stream.match('POP_FRAME')
        stream.match('SEMI')
        return ('POP_FRAME',)

    elif token.type in ['STOP']:
        stream.match('STOP')
        if stream.pointer().type == 'MSG':
            tk = stream.match('MSG')
            t = ('STOP', tk.value)
        else:
            t = ('STOP', None)
        stream.match('SEMI')
        return t
    elif token.type in ['NOOP']:
        stream.match('NOOP')
        stream.match('SEMI')
        return ('NOOP',)
    else:
        raise SyntaxError("instr: syntax error at {}"
                          .format(token.value))


# label : {NAME} NAME
def label(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        stream.match('NAME')
        return token.value
    else:
        raise SyntaxError("label: syntax error at {}"
                          .format(token.value))

# var : {NAME} NAME
def var(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        stream.match('NAME')
        return ('NAME', token.value)
    else:
        raise SyntaxError("var: syntax error at {}"
                          .format(token.value))

# num : {NUMBER} NUMBER
def num(stream):
    token = stream.pointer()
    if token.type in ['NUMBER']:
        stream.match('NUMBER')
        return ('NUMBER', float(token.value))
    else:
        raise SyntaxError("num: syntax error at {}"
                          .format(token.value))

# parser top-level driver
def parse(stream):
    from stackmachine.stackmachine_lexer import Lexer
    token_stream = Lexer(stream)
    instr_list(token_stream) # call the parser function for start symbol
    if not token_stream.end_of_file():
        raise SyntaxError("parse: syntax error at {}"
                          .format(token_stream.pointer().value))
