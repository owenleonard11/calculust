from typing import Callable, Any
from Function import *

__all__ = ['binaryop']

def binaryop(name: str, op_str: str, op_func: Callable[[Any, Any], Any]) -> type:
    def __init__(self, l: Function, r: Function):
        self.l = l
        self.r = r
    
    def eval(self, **kwargs) -> Function:
        l, r, cls = getattr(self, 'l'), getattr(self, 'r'), type(self)
        return cls(l.eval(**kwargs), r.eval(**kwargs)).simplify()

    def latex(self) -> str:
            return f'{self.l.latex}{self.op_str}{self.r.latex}'
        
    def __str__(self) -> str:
        return f'{self.l} {self.op_str} {self.r}'
    
    def simplify(self) -> Function:
        l, r, cls = getattr(self, 'l'), getattr(self, 'r'), type(self)
        match (l, r):
            case (Constant(x), Constant(y)):
                return Constant(op_func(x, y))
            case _:
                return cls(l, r)

    op_namespace = {
        '__doc__': f'{name}(l, r) = l {op_str} r',
        '__match_args__': ('l', 'r'),
        '__init__': __init__,
        '__str__': __str__,
        'eval': eval,
        'latex': latex,
        'simplify': simplify
    }
    
    return type(name, (Function,), op_namespace)
