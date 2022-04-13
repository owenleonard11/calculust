from typing import Any

from definition_utils import *
from Function import Function

__all__ = ['Constant', 'Variable']

# constants and variables
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
