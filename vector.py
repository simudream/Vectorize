class Memoize:
    '''
    This is the decorator class. It takes a function and does a lookup on the
    arguments passed. It simply passes the stored value for arguments already
    seen, otherwise it runs the function and stores the result.
    '''
    def __init__(self, func):
        self.prevs = {}
        self.func = func
    
    def __call__(self, *args):
        '''
        The internal call method allows calling the class instance just like
        a function.
        '''
        if not args in self.prevs:
            self.prevs[args] = self.func(*args)
        return self.prevs[args]

class Vector:

    def __init__(self, start=0, end=0, step=0, steps=0, array=None):
        if array is None:
            if not step:
                if not steps:
                    raise Exception("Must provide either a step value or the number of increments.")
                step = (end-start)/(steps-1)
            self.list = [(start + i*step) for i in range(0, int((end-start)/step)+1)]
        else:
            self.list = array

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)

    def elemult(self, other):
        return Vector(array=[self[i]*other[i] for i in range(0, len(self.list))])

    def _mul(self, other):
        if isinstance(other, Vector):
            if len(other) == len(self):
                return sum(self.list[i]*other.list[i] for i in range(0,len(self)))
            else:
                raise Exception("Vectors must be the same size")
        else:
            return Vector(array=[x*other for x in self.list])

    def __mul__(self, other):
        return self._mul(other)

    def __rmul__(self, other):
        return self._mul(other)

    def _add(self, other):
        if isinstance(other, Vector):
            if not (len(self) == len(other)):
                raise Exception("Vectors must be of the same size.")
            else:
                return Vector(array=[self[i]+other[i] for i in range(len(self))])
        else:
            return Vector(array=[x+other for x in self.list])
				
    def __add__(self, other):
        return self._add(other)

    def __radd__(self, scalar):
        return self._add(other)

    def _sub(self, other):
        if isinstance(other, Vector):
            if not (len(self) == len(other)):
                raise Exception("Vectors must be of the same size.")
            else:
                return Vector(array=[self[i]-other[i] for i in range(len(self))])
				
    def __sub__(self, other):
        return self._sub(other)
        
    def __rsub__(self, other):
        return other._sub(self)

    def __getitem__(self, index):
        return self.list[index]

@Memoize
def cos(v):
	from math import cos as mcos
	if isinstance(v, int) or isinstance(v, float):
		return mcos(v)
	elif isinstance(v, Vector):
		return Vector(array=[mcos(x) for x in v.list])
	else:
		raise Exception("Must provide either an int, a float, or a vector.")

@Memoize
def sin(v):
	from math import sin as msin
	if isinstance(v, int) or isinstance(v, float):
		return msin(v)
	elif isinstance(v, Vector):
		return Vector(array=[msin(x) for x in v.list])
	else:
		raise Exception("Must provide either an int, a float, or a vector.")


if __name__ == "__main__":

	import time
	from math import pi
	from pprint import pprint

	tstart_cpu = time.clock()   # start the CPU timer

	N = 150000           # number of particles
	nsteps = 40                 # number of rotation steps
	dtheta = (2.*pi) / nsteps     # change in theta between steps

	print "Rotating %s particles through %s theta values" % (N, nsteps)

	alpha = Vector(start=0, end=2*pi, steps=N)
	r = 1. + cos(alpha*10)*0.5       # vector with radius for each alpha
	x1 = 2. + r.elemult(cos(alpha))           # vector of x unrotated
	y1 = r.elemult(sin(alpha))                # vector of y unrotated

	for n in range(nsteps+1):
		theta = n*dtheta
		costh = cos(theta)
		sinth = sin(theta)
		x = costh*x1 - sinth*y1
		y = sinth*x1 + costh*y1

	t_cpu = time.clock() - tstart_cpu
	print "CPU time: %12.8f seconds" % t_cpu
