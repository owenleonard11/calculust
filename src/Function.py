from __future__ import annotations
from typing import Any
from abc import ABCMeta, abstractmethod

__all__ = ['Function', 'Constant', 'Variable', 'FunctionMeta']

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
        setattr(self, '__init__', init)
        setattr(self, '__match_args__', tuple(annotations))

class FunctionABCMeta(FunctionMeta, ABCMeta):
    """Empty class to allow """
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
        cls, match_args = type(self).__name__, getattr(self, '__match_args__')
        args = args = ', '.join([getattr(self, arg).__repr__() for arg in match_args])
        return f'{cls}({args})'
    
    def __call__(self, **kwargs) -> Function:
        return self.eval(**kwargs)
    
    def simplify(self) -> Function:
        return self

class Constant(Function):
    value: Any

    def eval(self, **kwargs) -> Function:
        return Constant(self.value)
    
    def __str__(self) -> str:
        return str(self.value)
        
class Variable(Function):
    name: str

    def eval(self, **kwargs) -> Function:
        return kwargs[self.name] if self.name in kwargs else Variable(self.name)

    def __str__(self) -> str:
        return self.name

