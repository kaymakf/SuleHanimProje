from fractions import Fraction
import math
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
from sympy import sympify
from sympy.core.sympify import kernS


def normalizeFraction(f):
    return Fraction(f.numerator % f.denominator, f.denominator)


def simpleContinuedFraction(f):
    n = [0]
    b = f

    while b.numerator != 1:
        b = Fraction(1/b)
        n.append(int(math.floor(b.numerator/b.denominator)))
        b = normalizeFraction(b)

    n.append(b.denominator)
    return n


def fareySum(f1, f2):
    return Fraction(f1.numerator + f2.numerator, f1.denominator + f2.denominator)


def findThePath(n):
    G = nx.Graph()
    numOfNodes = 2

    for val in n:
        numOfNodes += val

    for i in range(-1, -numOfNodes - 1, -1):
        G.add_node(i)

    G.add_edge(-1, -2)

    c = -2
    i = 1
    while i < len(n):
        G.add_edge(c, c - n[i])
        c -= n[i]
        i += 1

    c = -3
    pb = -1
    b = -2
    for i in range(len(n) - 1):
        G.add_edge(pb, c)
        for j in range(n[i + 1] - 1):
            G.add_edge(c, b)
            G.add_edge(c, c + 1)
            G.add_edge(c, c - 1)
            c -= 1
        c -= 1
        pb = b
        b -= n[i + 1]

    G.nodes[-1]['value'] = math.inf
    G.nodes[-2]['value'] = Fraction(0, 1)
    G.nodes[-3]['value'] = Fraction(1, 1)

    for i in range(-4, -numOfNodes - 1, -1):
        adjList = sorted(list(G.neighbors(i)), reverse=True)
        G.nodes[i]['value'] = fareySum(G.nodes[adjList[0]]['value'], G.nodes[adjList[1]]['value'])

    if G.nodes[-numOfNodes]['value'] != f:
        print("something is wronh!!!")

    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()

    shortestPaths = list(nx.all_shortest_paths(G, -1, -numOfNodes))
    shortestPathValues = []
    spaths = []

    for j in range(len(shortestPaths)):
        for i in shortestPaths[j]:
            shortestPathValues.append(G.nodes[i]['value'])
        spaths.append(shortestPathValues.copy())
        shortestPathValues.clear()

    return spaths


def tamsayiSurekliKesri(p):
    c = [p[1]]
    x = Symbol('x')
    for i in range(1, len(p)-1):
        eq = "(" + str(c[0])
        for j in range(1, i):
            eq += "-(1/(" + str(c[j])
        eq += "-(1/(x"
        for k in range(2*i+1): eq += ")"
        eq += "-(" + str(p[i+1]) + ")"
        eq = sympify(eq)
        c.append(list(solve(eq, x)).pop())

    for o in c:
        print(o, end=", ")











while True:
    inp = input("Enter a fraction(as a/b): ")
    if re.match("[0-9]+\/[1-9][0-9]*", inp):
        break
    else:
        print("Wrong input.\n")

f = Fraction(int(inp.split('/')[0]), int(inp.split('/')[1]))
f = normalizeFraction(f)

print(simpleContinuedFraction(f))

n = simpleContinuedFraction(f)

sp = findThePath(n)

for s in sp:
    print(s)


tamsayiSurekliKesri(sp[0])


