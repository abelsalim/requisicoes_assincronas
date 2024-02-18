import sys
from IPython.terminal import debugger


def set_trace():
    # Seta o ipython como default para debugger
    debugger.set_trace(sys._getframe().f_back)
