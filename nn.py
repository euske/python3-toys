#!/usr/bin/env python
import sys
from math import exp

def sigmoid(x):
    y = 1.0/(1.0+exp(-x))
    dy = y*(1-y)
    return (y, dy)

class Network:

    def __init__(self, rate=1.0, debug=0):
        self.rate = rate
        self.debug = debug
        self.nodes = []
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
        for node in self.nodes:
            node.reset()
        return

    def show(self):
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

    def recvForw(self, c, value):
        assert c.dst is self
        self.vBackNum += 1
        self.vBackTotal += c.weight * value
        if self.vBackNum < len(self.linkBack): return
        x = self.vBackTotal
        if self.network.debug:
            print('forw: %r:' % self,
                  ' + '.join( '%r%.3f*%.3f' % (c.src,c.weight,c.src.output) for c in self.linkBack ),
                  '= %.3f' % x)
        (self.output, self.gradient) = sigmoid(x)
        if self.network.debug:
            print('forw: %r: (output=%.3f, gradient=%.3f)' %
                  (self, self.output, self.gradient))
        self.feed(self.output)
        return

    def feed(self, value):
        self.output = value
        for c in self.linkForw:
            c.dst.recvForw(c, value)
        return

    def recvBacj(self, c, value):
        assert c.src is self
        self.vForwNum += 1
        self.vForwTotal += c.weight * value
        if self.vForwNum < len(self.linkForw): return
        error = self.vForwTotal
        if self.network.debug:
            print('bacj: %r:' % self,
                  ' + '.join( '%r%.3f*%.3f' % (c.dst,c.weight,c.dst.output) for c in self.linkForw ),
                  '= %.3f' % error)
        self.update(error)
        return

    def update(self, error):
        assert self.gradient is not None
        if self.network.debug:
            print('update: %r: (error=%.3f, gradient=%.3f)' %
                  (self, error, self.gradient))
        error *= self.gradient
        alpha = self.network.rate
        for c in self.linkBack:
            dw = alpha*error*c.src.output
            if self.network.debug:
                print('update: %r + %.3f -> %.3f' % (c, dw, c.weight+dw))
            c.weight += dw
            c.src.recvBacj(c, error)
        return

class InputNode(Node):

    def recvBacj(self, c, value):
        return

class HiddenNode(Node):

    pass

class OutputNode(Node):

    def learn(self, value):
        assert self.output is not None
        error = value - self.output
        #print('*** error: %.3f ***' % error)
        self.update(error)
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
