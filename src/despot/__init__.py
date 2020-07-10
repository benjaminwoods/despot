"""
Despot.
"""

from . import rulers, util
from . import classes

from .util.reg import register
from .classes import Despot

register(rulers.nero, 'nero')
register(classes.Despot, 'Despot')