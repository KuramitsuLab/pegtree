import os

DebugFlag = 'DEBUG' in os.environ
VerboseFlag = 'VERBOSE' in os.environ


def DEBUG(*x):
    if DebugFlag:
        print('DEBUG', *x)


def VERBOSE(*x):
    if DebugFlag:
        print(*x)
