from DragonGen import DragonGen 
from DragonGen.util import *
import os, sys
try:
    DragonGen.main()
except FileNotFoundError as exception:
    dberror('Error: No project files found')

    DragonGen.handle(exception)
    sys.exit(2)
except KeyError as exception:
    dberror('KeyError: Missing value in variables array.')
    dberror(str(exception))

    DragonGen.handle(exception)
    sys.exit(2)
except IndexError as exception:
    dberror("IndexError: List index out of range.")
    dberror(str(exception))

    DragonGen.handle(exception)
    sys.exit(2)
except Exception as exception:
    dberror('Error: An undocumented error has been hit')
    dberror('Please contact a maintainer')

    DragonGen.handle(exception)
    sys.exit(-1)
