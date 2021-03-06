from __future__ import annotations
from typing import Any
from abc import ABCMeta, abstractmethod

__all__ = ['FunctionMeta', 'FunctionABCMeta', 'Function']

class FunctionMeta(type):
    """A metaclass whose instances are function classes"""
    def __new__(cls, name: str, bases: tuple[type, ...], dic: dict[str, Any]):
        return super(FunctionMeta, cls).__new__(cls, name, bases, dic)
    
    def __init__(self, name, bases, dic: dict):
        type.__init__(self, name, bases, dic)
        annotations = dic.get('__annotations__', {})

        def init(self, *args):
            for name, arg in zip(annotations, args):
                setattr(self, name, arg)
        
        def iter(self):
            for arg in self.__match_args__:
                yield getattr(self, arg)

        setattr(self, '__init__', init)
        setattr(self, '__iter__', iter)
        setattr(self, '__match_args__', tuple(annotations))

class FunctionABCMeta(FunctionMeta, ABCMeta):
    """Empty class to allow inheritance from Function and ABC"""
    ...

class Function(metaclass=FunctionABCMeta):
    """Abstract base class for function classes"""
    @abstractmethod
    def eval(self, **kwargs) -> Function:  ...

    @abstractmethod
    def __str__(self) -> str: ...

    def latex(self) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        cls, args = type(self).__name__, ', '.join(f'{arg!r}' for arg in self) # type: ignore
        return f'{cls}({args})'
    
    def __call__(self, **kwargs) -> Function:
        return self.eval(**kwargs)
    
    def __eq__(self, other) -> bool:
        if type(self) is type(other):
            return tuple(self) == tuple(other) # type: ignore
        return False
    
    def _simplify(self) -> Function:
        return self
    
    def simplify(self) -> Function:
        simplified = self._simplify()
        if simplified == simplified._simplify():
            return simplified
        else:
            return simplified.simplify()
