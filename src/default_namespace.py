import operator as op
from definition_utils import *

@binaryinfix
class Add:
    OP_STR = '+'
    IDENT = 0
    OP_FUNC = op.add

@binaryinfix
class Sub:
    OP_STR = '-'
    IDENT = 0
    OP_FUNC = op.sub
