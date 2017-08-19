#!/usr/bin/env python
import sys
from math import exp

def sigmoid(x):
    return 1.0/(1.0+exp(-x))
def gradient(y):
    return y*(1-y)

class Network:

    def __init__(self, rate=1.0, debug=0):
        self.rate = rate
        self.debug = debug
        self.nodes = []
        self.error = 0
        return

    def __repr__(self):
        return ('<Network: rate=%r, nodes=%r>' % (self.rate, self.nodes))

    def addInput(self, name):
        node = InputNode(self, name)
        self.nodes.append(node)
        return node

    def addOutput(self, name):
        node = OutputNode(self, name)
        self.nodes.append(node)
        return node
    
    def addHidden(self, name):
        node = HiddenNode(self, name)
        self.nodes.append(node)
        return node
    
    def connect(self, src, dst, weight=0.5):
        print('connect: %r -- %r' % (src, dst))
        link = Link(src, dst, weight)
        src.linkForw.append(link)
        dst.linkBack.append(link)
        return

    def reset(self):
        self.error = 0
        for node in self.nodes:
            node.reset()
        return

    def show(self):
        print('** current error: %r' % self.error)
        for node in self.nodes:
            node.show()
        print()
        return

class Link:

    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight
        return

    def __repr__(self):
        return '%r-%r(%.3f)' % (self.src, self.dst, self.weight)

class Node:

    def __init__(self, network, name):
        self.network = network
        self.name = name
        self.linkForw = []
        self.linkBack = []
        self.bias = 0.1
        return

    def __repr__(self):
        return '<%s>' % self.name

    def show(self):
        print('%r:' % self,
              ', '.join( repr(c) for c in self.linkForw ))
        return

    def reset(self):
        self.vForwNum = 0
        self.vForwTotal = 0
        self.vBackNum = 0
        self.vBackTotal = 0
        self.output = self.gradient = None
        return

    def feedForw(self, value):
        self.vBackNum += 1
        self.vBackTotal += value
        if self.vBackNum < len(self.linkBack): return
        output = sigmoid(self.vBackTotal + self.bias)
        self.send(output)
        return

    def send(self, output):
        self.output = output
        self.gradient = gradient(output)
        for c in self.linkForw:
            c.dst.feedForw(c.weight * output)
        return

    def update(self, delta):
        self.network.error += delta*delta
        delta *= self.gradient
        eta = self.network.rate * delta
        for c in self.linkBack:
            dw = eta * c.src.output
            c.weight += dw
            c.src.feedBack(c.weight * delta)
        return

    def feedBack(self, value):
        assert self.output
        assert self.gradient
        self.vForwNum += 1
        self.vForwTotal += value
        if self.vForwNum < len(self.linkForw): return
        self.update(self.vForwTotal)
        return

class InputNode(Node):

    def feed(self, value):
        self.send(value)
        return

    def feedBack(self, value):
        return

class HiddenNode(Node):

    pass

class OutputNode(Node):

    def learn(self, value):
        assert self.output is not None
        error = value - self.output
        self.feedBack(error)
        #print('*** error: %.3f ***' % self.network.error)
        return

N = Network(2.0)
n1 = N.addInput('n1')
n2 = N.addInput('n2')
n3 = N.addHidden('n3')
n4 = N.addHidden('n4')
n5 = N.addHidden('n5')
n6 = N.addOutput('n6')
N.connect(n1, n3)
N.connect(n1, n4)
N.connect(n2, n4)
N.connect(n2, n5)
N.connect(n3, n6)
N.connect(n4, n6)
N.connect(n5, n6)

for _ in range(1000):
    N.reset()
    n1.feed(0.0)
    n2.feed(0.0)
    n6.learn(0.0)
    N.reset()
    n1.feed(1.0)
    n2.feed(0.0)
    n6.learn(1.0)
    N.reset()
    n1.feed(0.0)
    n2.feed(1.0)
    n6.learn(1.0)
    N.reset()
    n1.feed(1.0)
    n2.feed(1.0)
    n6.learn(0.0)
    
N.show()

N.reset()
n1.feed(0.0)
n2.feed(0.0)
print(n6.output)

N.reset()
n1.feed(1.0)
n2.feed(0.0)
print(n6.output)

N.reset()
n1.feed(0.0)
n2.feed(1.0)
print(n6.output)

N.reset()
n1.feed(1.0)
n2.feed(1.0)
print(n6.output)
