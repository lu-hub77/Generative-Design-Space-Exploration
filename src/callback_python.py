#script(python)
import numpy as np
from clingo import *

class ExtraFunctions:
	def getId(self,basestr,args):
		return Function(str(basestr) + ''.join(map(str,args.arguments)))

#end.
