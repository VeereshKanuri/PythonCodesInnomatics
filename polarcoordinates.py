import math , cmath
a=complex(input())
x = a.real
y = a.imag
print(math.sqrt(x**2+y**2))
print(cmath.phase(complex(x,y)))