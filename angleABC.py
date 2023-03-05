from math import atan, degrees
x = int(input())
y = int(input())

angC = atan(x/y)
print((round(degrees(angC))),chr(176),sep='')