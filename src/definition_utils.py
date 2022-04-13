from Function import Function, FunctionABCMeta
from bases import Constant

__all__ = ['binaryinfix']

def binaryinfix(cls) -> FunctionABCMeta:
    """Decorator for easy definition of infix operators"""
    for attr in ('OP_STR', 'IDENT', 'OP_FUNC'):
        if attr not in cls.__dict__:
            raise 

    def eval(self, **kwargs) -> Function:
        return type(self)(self.l.eval(**kwargs), self.r.eval(**kwargs)).simplify()
    
    def string(self) -> str:
        return f'{self.l} {type(self).OP_STR} {self.r}'
    
    def _simplify(self) -> Function:
        l, r, cls = self.l, self.r, type(self)
        match (l, r):
            case (Constant(x), Constant(y)): # ex: 6 / 3 -> 2
                return Constant(cls.OP_FUNC(x, y))
            case (x, Constant(cls.IDENT)): # ex: (2 - 3) * 1 -> 2 - 3
                return type(x)(*x).simplify()
            case (Constant(cls.IDENT), y): # ex: 0 + sin(x) -> sin(x)
                return type(y)(*y).simplify()
            case _:
                return type(self)(self.l.simplify(), self.r.simplify())
    
    setattr(cls, 'eval', eval)
    setattr(cls, '__str__', string)
    setattr(cls, '_simplify', _simplify)
    dic = cls.__dict__ | {'__annotations__': {'l': Function, 'r': Function}}

    return FunctionABCMeta(cls.__name__, (Function,), dic)
