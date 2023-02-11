import sys
isDebug = True if sys.gettrace() else False
print('isDebug:', isDebug)