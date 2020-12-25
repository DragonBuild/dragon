from DragonGen import DragonGen 
import os, sys
try:
    DragonGen.main()
except FileNotFoundError as exception:
    print('Error: No project files found', file=sys.stderr)

    DragonGen.handle(exception)
    sys.exit(2)
except KeyError as exception:
    print('KeyError: Missing value in variables array.', file=sys.stderr)
    print(str(exception), file=sys.stderr)

    DragonGen.handle(exception)
    sys.exit(2)
except IndexError as exception:
    print("IndexError: List index out of range.", file=sys.stderr)
    print(str(exception), file=sys.stderr)

    DragonGen.handle(exception)
    sys.exit(2)
except Exception as exception:
    print('Error: An undocumented error has been hit', file=sys.stderr)
    print('Please contact a maintainer', file=sys.stderr)

    DragonGen.handle(exception)
    sys.exit(-1)
