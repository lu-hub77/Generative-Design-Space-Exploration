#script(python)
import numpy as np
from clingo import *
r=None
def getId(basestr,args):
	return Function(str(basestr) + ''.join(map(str,args.arguments)))

#end.
