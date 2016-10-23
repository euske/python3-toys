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
    
    def reset(self):
        for node in self.nodes:
            node.reset()
        return

    def show(self):
        for node in self.nodes:
            node.show()
        print()
        return

class Connection:

    def __init__(self, node0, node1, weight):
        self.node0 = node0
        self.node1 = node1
        self.weight = weight
        return

    def __repr__(self):
        return '%r--%r(%.3f)' % (self.node0, self.node1, self.weight)

class Node:

    def __init__(self, network, name):
        self.network = network
        self.name = name
        self.cForw = {}
        self.cBacj = {}
        return

    def __repr__(self):
        return '<%s>' % self.name

    def show(self):
        print('%r:' % self,
              ', '.join( repr(c) for c in self.cForw.values() ))
        return

    def connect(self, node, weight=0.5):
        print('connect: %r -- %r' % (self, node))
        c = Connection(self, node, weight)
        self.cForw[node] = c
        node.cBacj[self] = c
        return

    def reset(self):
        self.vForw = {}
        self.vBacj = {}
        self.output = self.gradient = None
        return

    def recvForw(self, node0, value):
        assert node0 in self.cBacj
        assert node0 not in self.vBacj
        self.vBacj[node0] = value
        if len(self.vBacj) < len(self.cBacj): return
        a = [ (self.cBacj[n], v) for (n,v) in self.vBacj.items() ]
        x = sum( c.weight*v for (c,v) in a )
        if self.network.debug:
            print('forw: %r:' % self,
                  ' + '.join( '%r%.3f*%.3f' % (c.node0,c.weight,v) for (c,v) in a ),
                  '= %.3f' % x)
        (self.output, self.gradient) = sigmoid(x)
        if self.network.debug:
            print('forw: %r: (output=%.3f, gradient=%.3f)' %
                  (self, self.output, self.gradient))
        self.feed(self.output)
        return

    def feed(self, value):
        for node1 in self.cForw.keys():
            node1.recvForw(self, value)
        return

    def recvBacj(self, node1, value):
        assert node1 in self.cForw
        assert node1 not in self.vForw
        self.vForw[node1] = value
        if len(self.vForw) < len(self.cForw): return
        a = [ (self.cForw[n], v) for (n,v) in self.vForw.items() ]
        error = sum( c.weight*v for (c,v) in a )
        if self.network.debug:
            print('bacj: %r:' % self,
                  ' + '.join( '%r%.3f*%.3f' % (c.node1,c.weight,v) for (n,c,v) in a ),
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
        for (node0,c) in self.cBacj.items():
            dw = alpha*error*self.vBacj[node0]
            if self.network.debug:
                print('update: %r + %.3f -> %.3f' % (c, dw, c.weight+dw))
            c.weight += dw
            node0.recvBacj(self, error)
        return

class InputNode(Node):

    def recvBacj(self, node1, value):
        return

class HiddenNode(Node):

    pass

class OutputNode(Node):

    def learn(self, value):
        assert self.output is not None
        error = value - self.output
        print('*** error: %.3f ***' % error)
        self.update(error)
        return

N = Network(2.0)
n1 = N.addInput('n1')
n2 = N.addInput('n2')
n3 = N.addHidden('n3')
n4 = N.addHidden('n4')
n5 = N.addHidden('n5')
n6 = N.addOutput('n6')
n1.connect(n3)
n1.connect(n4)
n2.connect(n4)
n2.connect(n5)
n3.connect(n6)
n4.connect(n6)
n5.connect(n6)

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
