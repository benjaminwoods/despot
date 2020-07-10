"""
Despot.
"""

from . import rulers, util
from . import classes

from .util.reg import register
from .classes import Despot

for ruler in ('cleopatra', 'joan', 'nero'):
    register(getattr(rulers, ruler), ruler)

register(classes.Despot, 'Despot')