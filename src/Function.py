from __future__ import annotations

__all__ = ['Function', 'Constant', 'Variable']

class Function:
    """A class representing an arbitrary function"""
    __match_args__: tuple[str, ...]

    def __init__(self, *args):
        """Default initializer, used to avoid rewriting __init__ for subclasses"""
        for i, arg in enumerate(args):
            setattr(self, self.__match_args__[i], arg)

    def eval(self, **kwargs) -> Function:
        """Return a new Function computed by "plugging in" the values given in kwargs for the Variables in self"""
        return self.simplify()

    def latex(self) -> str:
        """Return a LaTeX representation of the Function"""
        return str(self.__match_args__[0])

    def __str__(self) -> str:
        """Return a human-readable string representation of the Function"""
        return str(getattr(self, self.__match_args__[0]))

    def __repr__(self) -> str:
        """Return a possible constructor for the Function"""
        cls  = type(self).__name__
        args = ', '.join([getattr(self, arg).__repr__() for arg in self.__match_args__])
        return f'{cls}({args})'

    def simplify(self) -> Function:
        """Return an algebraic of the Function (see docs)"""
        return self
    
    def __call__(self, **kwargs) -> Function:
        """Calling the function just calls eval, should be no need to overwrite this"""
        return self.eval(**kwargs)

class Constant(Function):
    __match_args__ = ('value',)
    value: str

class Variable(Function):
    __match_args__ = ('name',)
    name: str

    def eval(self, **kwargs) -> Function:
        return kwargs[self.name] if self.name in kwargs else self
