from Function import Function, Constant, FunctionABCMeta

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
    
    def simplify(self) -> Function:
        l, r, cls = self.l, self.r, type(self)
        match (l, r):
            case (Constant(x), Constant(y)):
                return Constant(cls.OP_FUNC(x, y))
            case (x, cls.IDENT):
                return type(x)(*x)
            case (cls.IDENT, y):
                return type(y)(*y)
            case _:
                return type(self)(self.l, self.r)
    
    setattr(cls, 'eval', eval)
    setattr(cls, '__str__', string)
    setattr(cls, 'simplify', simplify)
    dic = cls.__dict__ | {'__annotations__': {'l': Function, 'r': Function}}

    return FunctionABCMeta(cls.__name__, (Function,), dic)
