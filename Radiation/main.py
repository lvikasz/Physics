# This is a solution for Polish Physics Olympiad's problem.
# The Agent has to deliver a package from point A to B, but in the middle of the AB segment (in point C) there are radiation source.
# Determine (accurate to within 50 m) the radius of a circle, on which Agent absorb least dose.  

from math import pow, sqrt, atan, tan, fabs
from copy import copy

epsilon = 0.01

class Point:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y
        self.R = 0

    def __eq__(self, other):
        if fabs(self.x - other.x) <= epsilon and fabs(self.y - other.y) <= epsilon:
            return True

        return False
    def __ne__(self, other):
        if fabs(self.x - other.x) > epsilon or fabs(self.y - other.y) > epsilon:
            return True

        return False

    def __str__(self):
        return ("x = %f, y = %f, R = %f" % (self.x, self.y, self.R))  

# stałe:
# v - prędkość ziomka
# a - odległość punktów od źródła
# alfa - współczynnik od którego zależy dawka odebrana
# epsilon - dokładość z jaką mamy wyznaczyć promień
# A(0,0) - punkt rozpoczęcia
# B(a, 0) - punkt zakończenia
# C(a/2, a*sqrt(3)/2) - punkt źródła

v = 10
a = 2000
alfa = 1
delx = 0.01

A = Point(0,0)
B = Point(a, 0)
C = Point(a/2, -a*sqrt(3)/2)

# variables:
# D - absorbed dose
# Dchw - temporary dose in a one iteration
# O(a/2, y0) - circle coordinates
# R - temporary radius length in one iteration
# lchw - distance to radiation source

# distance between two points
def distance(p1 : Point, p2 : Point):
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def solveQuadraticExuation(a : float, b : float, c : float):
    delta = b**2 - 4*a*c

    x1 = (-1 * b - sqrt(delta)) / (2*a)
    x2 = (-1 * b + sqrt(delta)) / (2*a)
    return x1, x2

# calculate next agent's position
def countNextPosition(currentPoint : Point, circle : Point, RSquere : float):
    nextPoint = copy(currentPoint)
    nextPoint.x += delx
    
    nextPoint.y = sqrt(RSquere - (nextPoint.x - circle.x) **2) + circle.y
    s = distance(currentPoint, nextPoint)
    t = s/v
    return nextPoint, t
 
def countD(currentPoint : Point, source : Point, t : float):
    D = (alfa * t) / (distance(currentPoint, source)**2)
    return D

def checkCircle(circle : Point, source : Point):
    totalDose = 0

    xSq = circle.x**2
    Rsq = circle.R**2
    currentPoint = A

    while currentPoint != B:
        currentPoint, t = countNextPosition(currentPoint, circle, Rsq)
        totalDose += countD(currentPoint, source, t)

    return totalDose    

def findBest():
    y = 0

    circle = Point(C.x, y)
    circle.R = distance(circle, A)

    previousDose = checkCircle(circle, C)
    while True:
        y -= 50

        circle.R += 25
        circle.y = -sqrt(circle.R**2-circle.x**2)

        nextDose = checkCircle(circle, C)
        print(nextDose)
        print(circle)
        if(previousDose < nextDose):
            print("Koniec.")
            break
        previousDose = nextDose
# findBest()

def makeChart():
    import matplotlib.pyplot as plt

    circle = Point(C.x, 0)
    circle.R = distance(circle, A)

    x = []
    y = []

    for i in range(50):
        x.append(circle.R)
        y.append(checkCircle(circle, C))

        circle.y -= 50
        circle.R = distance(circle, A)

    plt.plot(x,y)
    plt.xlabel("R")
    plt.ylabel("Dose")
    plt.title("Dose of radiation")
    plt.show()
makeChart()
    