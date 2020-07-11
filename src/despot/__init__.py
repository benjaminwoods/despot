"""
Despot.
"""

from . import rulers, util
from . import classes

# Shorthand
Despot = classes.Despot
register = util.reg.register

for ruler in ('cleopatra', 'joan', 'nero'):
    register(getattr(rulers, ruler), ruler)

register(Despot, 'Despot')

__all__ = ['rulers', 'util', 'classes',
           'Despot']
