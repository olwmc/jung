from argparse import ArgumentParser


def label_def(instr_tuple):

    instr_type = instr_tuple[0]

    if instr_type[-1] == ':':
        return True
    else:
        return False

def output(instr_stream):

    output_stream = ''

    for instr in instr_stream:
        if label_def(instr):  # label def - without preceding '\t' or trailing ';'
            output_stream += instr[0] + '\n'

        else:                 # regular instruction - indent and put a ';' at the end
            output_stream += '\t'

            for component in instr:
                output_stream += str(component) + ' '

            output_stream += ';\n'

    return output_stream

def cc(char_stream):
    from jung.parser import parse
    from jung.codegen import walk
    from jung.dumpast import dumpast

    try:
        ast = None

        ast = parse(char_stream) 

        func_defs = []
        rest = []

        for node in ast[1]:
            if node[0] == 'DEFUN':
                func_defs += [node]
            else:
                rest += [node]

        func_defs = ('STMTS', func_defs)
        rest = ('STMTS', rest)

        code = walk(func_defs) + [('_start:',)] + walk(rest) + [('stop', )]
        out_code = output(code)

        return out_code
    except Exception as e:
        print('error: ' + str(e))
        return None
