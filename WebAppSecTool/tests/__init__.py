import logging

from .test_module1 import *
from .test_module2 import *
__all__ = ['test_module1', 'test_module2']

logging.basicConfig(level=logging.DEBUG)