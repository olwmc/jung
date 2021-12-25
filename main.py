import sys
from jung.cc import cc
from stackmachine.stackmachine_interp import interp
from argparse import ArgumentParser

if __name__ == "__main__":
    # parse command line args
    aparser = ArgumentParser()
    aparser.add_argument('input', metavar='input_file', help='cuppa1 input file')
    aparser.add_argument('-o', metavar='output_file', help='exp1bytecode output file')

    args = vars(aparser.parse_args())

    f = open(args['input'], 'r')
    input_stream = f.read()
    f.close()

    # run the compiler
    bytecode = cc(input_stream)

    if not args['o']:
        interp(bytecode)
    else:
        f = open(args['o'], 'w')
        f.write(bytecode)
