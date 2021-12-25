#!/usr/bin/env python

from stackmachine.stackmachine_interp_fe import parse
from stackmachine.stackmachine_interp_state import state

#####################################################################################
def interp_program():
    'execute stack machine'

    # start at the first instruction in program
    state.call_stack.goto(state.label_table.get('_start'))
    
    # keep interpreting until we run out of instructions
    # or we hit a 'stop'
    while True:
        if state.call_stack.pointer() == len(state.program):
            break
        else:
            # get instruction from program
            instr = state.program[state.call_stack.pointer()]

        # instruction format: (type, [arg1, arg2, ...])
        type = instr[0]

        if type == 'PUSH':
            # PUSH NUMBER|VAR
            val = eval_num_var(instr[1])
            state.stack.append(val) # push value
            state.call_stack.next()

        elif type == 'POP':
            # POP
            state.stack.pop()
            state.call_stack.next()

        # interpret instruction
        elif type == 'PRINT_STR':
            # PRINT msg?
            string_val = instr[1]
            print("{}".format(string_val), end='')
            state.call_stack.next()

        # interpret instruction
        elif type == 'PRINT':
            # PRINT msg?
            val = state.stack.pop()
            string_val = instr[1]
            if string_val:
                print("{} {}".format(string_val, val), end='')
            else:
                print("{:g}".format(val), end='')
            state.call_stack.next()

        elif type == 'NEWLINE':
            print('',end='\n')
            state.call_stack.next()

        elif type == 'STORE':
            # STORE VAR
            var_tree = instr[1]
            (NAME, var_name) = var_tree
            val = state.stack.pop()
            state.symbol_table.update(var_name, val)
            state.call_stack.next()

        elif type == 'ASK':
            # ask
            prompt = instr[1]
            if prompt:
                val = input(prompt)
            else:
                val = input()
            try:
                state.stack.append(int(val))
            except:
                # rethrow the exception
                raise ValueError("Error: {} not valid integer".format(val))
            state.call_stack.next()

        elif type == 'JUMPT':
            # JUMPT label
            val = state.stack.pop()
            if val:
                state.call_stack.goto(state.label_table.get(instr[1]))
            else:
                state.call_stack.next()

        elif type == 'JUMPF':
            # JUMPF label
            val = state.stack.pop()
            if not val:
                state.call_stack.goto(state.label_table.get(instr[1]))
            else:
                state.call_stack.next()

        elif type == 'JUMP':
            state.call_stack.goto(state.label_table.get(instr[1]))

        elif type == 'CALL':
            loc = instr[1]
            state.symbol_table.push()
            state.call_stack.push(state.label_table.get(instr[1]))
        
        elif type == 'RETURN':
            state.symbol_table.pop()
            state.call_stack.pop()
            state.call_stack.next()

        elif type == 'PUSH_FRAME':
            state.symbol_table.push()
            state.call_stack.next()

        elif type == 'POP_FRAME':
            state.symbol_table.pop()
            state.call_stack.next()

        elif type == 'STOP':
            # STOP msg?
            if instr[1]:
                print("{}".format(instr[1]))
            break

        elif type == 'NOOP':
            # NOOP
            state.call_stack.next()

        elif type == 'DUP':
            # DUP
            val = state.stack.pop()
            state.stack.append(val)
            state.stack.append(val)
            state.call_stack.next()

        elif type == 'ADD':
            # ADD
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(val2 + val1)
            state.call_stack.next()

        elif type == 'SUB':
            # SUB
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(val2 - val1)
            state.call_stack.next()

        elif type == 'MUL':
            # MUL
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(val2 * val1)
            state.call_stack.next()

        elif type == 'DIV':
            # DIV
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(val2 / val1)
            state.call_stack.next()

        elif type == 'MOD':
            # MOD
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(val2 % val1)
            state.call_stack.next()

        elif type == 'EQU':
            # EQU
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 == val1 else 0)
            state.call_stack.next()

        elif type == 'NEQ':
            # NEQ
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 != val1 else 0)
            state.call_stack.next()

        elif type == 'AND':
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 and val1 else 0)
            state.call_stack.next()

        elif type == 'OR':
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 or val1 else 0)
            state.call_stack.next()

        elif type == 'NOT':
            val1 = state.stack.pop()
            state.stack.append(1 if not(val1) else 0)
            state.call_stack.next()

        elif type == 'LT':
            # LT
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 < val1 else 0)
            state.call_stack.next()

        elif type == 'LEQ':
            # LEQ
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 <= val1 else 0)
            state.call_stack.next()


        elif type == 'GT':
            # GT
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 > val1 else 0)
            state.call_stack.next()

        elif type == 'GEQ':
            # GEQ
            val1 = state.stack.pop()
            val2 = state.stack.pop()
            state.stack.append(1 if val2 >= val1 else 0)
            state.call_stack.next()

        else:
            raise ValueError("Unexpected instruction type: {}".format(type))


#####################################################################################
# evaluate a number or variable and return an integer value
def eval_num_var(node):

    # tree nodes are tuples (TYPE, [arg1, arg2,...])

    type = node[0]

    if type == 'NAME':
        # 'NAME' var_name
        return state.symbol_table.get(node[1])

    elif type == 'NUMBER':
        # NUMBER val
        return node[1]

#####################################################################################
def interp(input_stream):

    try:
        state.initialize()  # initialize our abstract machine
        parse(input_stream) # build the IR
        interp_program()    # interpret the IR
    except Exception as e:
        print("error: "+str(e))
        raise e

#####################################################################################
if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) == 1: # no args - read stdin
        char_stream = sys.stdin.read()
    else: # last arg is filename to open and read
        input_file = sys.argv[-1]
        if not os.path.isfile(input_file):
            print("unknown file {}".format(input_file))
            sys.exit(0)
        else:
            f = open(input_file, 'r')
            char_stream = f.read()
            f.close()

    interp(char_stream)
