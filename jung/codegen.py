def stmts(node):
    (STMTS, lst) = node

    outlst = []
    for stmt in lst:
        outlst += walk(stmt)
    return outlst

def store_stmt(node):
    (STORE, v, e) = node

    code = []
    code += walk(e)
    code += [('store', v[1])]

    return code

def print_stmt(node):
    (PRINT, args) = node

    code = []

    for arg in args:
        if arg[0] == 'STRING':
            code += [('print_str ' + arg[1],)]
        else:
            code += walk(arg)
            code += [('print',)]

    code += [('newline',)]

    return code

def for_stmt(node):
    (FOR, v, start, end, body) = node

    L_A = label()
    L_B = label()

    begin = walk(start)
    stop = walk(end)
    body_code = walk(body)

    code = list()

    # Push the frame
    code += [('push_frame',)]
    code += begin

    # Store variable
    code += [('store', v[1])]
    
    # Compare begin to end
    code += begin
    code += stop
    code += [('leq',)]
    code += [('jumpt', L_A)]

    code += [('jump', L_B)]


    code += [(L_A + ":",)]
    code += body_code

    code += [('push', v[1])]
    code += [('push', '1')]
    code += [('add',)]
    code += [('store', v[1])]
    # Compare begin to end
    code += [('push', v[1])]
    code += stop
    code += [('leq',)]
    code += [('jumpt', L_A)]

    code += [('jump', L_B)]

    code += [(L_B + ":",)]
    code += [('pop_frame',)]
    code += [('noop',)]

    return code

def defun_stmt(node):
    (DEFUN, v, (ARGLIST, args), body) = node

    # Make label
    code = []
    code += [(v[1] + ":",)]

    # Bind variables
    for arg in args:
        code += [('store', arg[1])]

    code += walk(body)

    # End return
    code += [('push', 0)]
    code += [('return',)]

    return code

def return_stmt(node):
    (RETURN, arg) = node

    code = []
    code += walk(arg)
    code += [('return',)]

    return code

def cond_stmt(node):
    (COND, (TESTS, tests), (BODIES, bodies)) = node

    code = []

    end_label = label()
    labels = []

    for t in tests:
        labels.append(label())
        code += walk(t)
        code += [ ('jumpt', labels[-1]) ]
    
    code +=  [ ('jump', end_label) ]

    for i in range(len(labels)):
        code += [(labels[i] + ":", )]
        code += walk(bodies[i])
        code +=  [ ('jump', end_label) ]

    code += [(end_label + ":", )]
    code += [('noop',)]
    return code

def call_stmt(node):
    (CALL, v, args) = node

    code = []
    for arg in args[::-1]:
        code += [('push', arg[1])]

    code += [('call', v[1])]
    code += [('pop',)]
    return code

def invocation_exp(node):
    (INVOCATION, v, args) = node

    code = []
    for arg in args[::-1]:
        code += walk(arg)

    code += [('call', v[1])]
    return code

def num_exp(node):
    (NUM, value) = node

    return [('push', str(value))]

def bool_exp(node):
    (BOOL, value) = node

    return [('push', str(value))]

def var_exp(node):
    (VAR, v) = node
    return [('push', v)]

def mul_exp(node):
    (MUL, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('mul', )]

    return code

def div_exp(node):
    (DIV, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('div', )]

    return code

def add_exp(node):
    (ADD, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('add', )]

    return code

def sub_exp(node):
    (SUB, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('sub', )]

    return code

def and_exp(node):
    (AND, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('and', )]

    return code

def or_exp(node):
    (OR, v1, v2) = node

    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('or', )]

    return code

def not_exp(node):
    (NOT, v1) = node

    code = []
    code += walk(v1)
    code += [('not', )]

    return code

def mod_exp(node):
    (MOD, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('mod',)]

    return code

def neq_exp(node):
    (NEQ, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('neq',)]

    return code

def eq_exp(node):
    (EQ, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('equ',)]

    return code

def lt_exp(node):
    (LT, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('lt',)]

    return code

def leq_exp(node):
    (LEQ, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('leq',)]

    return code

def gt_exp(node):
    (GT, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('gt',)]

    return code

def geq_exp(node):
    (GEQ, v1, v2) = node
    code = []
    code += walk(v1)
    code += walk(v2)
    code += [('geq',)]

    return code

def ask_exp(node):
    (ASK, msg) = node

    code = [('ask' + (' '+msg if msg else ''), )]

    return code

def walk(node):
    if node == []:
        return []

    node_type = node[0]

    if node_type in dispatch:
        node_function = dispatch[node_type]
        return node_function(node)
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

# a dictionary to associate tree nodes with node functions
dispatch = {
    "STMTS": stmts,
    "STORE": store_stmt,
    "PRINT": print_stmt,
    "CALL": call_stmt,
    "FOR": for_stmt,
    "DEFUN": defun_stmt,
    "RETURN": return_stmt,
    "COND": cond_stmt,
    "NUM": num_exp,
    "VAR": var_exp,
    "ASK": ask_exp,
    "BOOL": bool_exp,
    
    "ADD": add_exp,
    "SUB": sub_exp,
    "MUL": mul_exp,
    "DIV": div_exp,
    "MOD": mod_exp,
    
    "EQ": eq_exp,
    "NEQ": neq_exp,
    "LEQ": leq_exp,
    "LT": lt_exp,
    "GEQ": geq_exp,
    "GT": gt_exp,

    "AND": and_exp,
    "OR": or_exp,
    "NOT": not_exp,

    "INVOCATION": invocation_exp
}

label_id = 0

def label():
    global label_id
    s =  'L' + str(label_id)
    label_id += 1
    return s
