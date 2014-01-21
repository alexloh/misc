# Neural network 
# includes perceptron and more general neural net

import random

class NNode:
  weights = []
  num_w = 0
  def __init__(self, num_weights):
    if isinstance(num_weights, int):
      self.weights = [random.uniform(-1,1) for r in xrange(num_weights)]
      self.num_w = num_weights
    else:
      self.weights = num_weights
      self.num_w = len(num_weights)
  def feedforward(self, inputs):
    sum = 0
    for i in xrange(self.num_w - 1):
      sum += inputs[i] * self.weights[i]
    sum += self.weights[self.num_w-1]
    if sum > 0:
      return 1
    else:
      return -1
  def adjust(self, adjustment, inputs):
    for i in xrange(self.num_w - 1):
      self.weights[i] += adjustment * inputs[i]
    self.weights[self.num_w-1] += adjustment
  def __repr__(self):
    return "NNode: "+repr(self.weights)

class Perceptron:
  nodes = []
  num_w = 0
  def __init__(self, num_inputs):
    self.num_w = num_inputs + 1
    self.nodes = [NNode(self.num_w)]
  def guess(self, inputs):
    return self.nodes[0].feedforward(inputs)
  def train(self, count, oracle):
    c = 0.01
    for i in xrange(count):
      inputs = [random.randint(0,999) for r in xrange(self.num_w)]
      g = self.guess(inputs)
      err = oracle(inputs) - g
      for n in self.nodes:
        n.adjust(err * c, inputs)
  def check(self, count, oracle, verbose = False):
    error = 0
    for i in xrange(count):
      pt = [random.randint(0,999) for r in xrange(self.num_w)]
      guess = self.guess(pt)
      actual = oracle(pt)
      if guess != actual:
        error += 1
        if verbose:
          print "error! counterexample: "+repr(pt)
    return 100.0 * (count - error) / count
  def __repr__(self):
    return repr(self.nodes)

class NeuralNet: #currently not working
  num_w = 0
  levels = [] # array of array representing nodes
  to = {} # dictionary of dictionaries of arrays representing where output flows to
          # eg. {1: {4: [0,2]}} means the 4th node in layer 1 connects to 0th and 2nd node in layer 2
  fro = {} # inverse of to
           # eg. fro = {L: {to: [fro1, fro2]}} implies to = {L-1: {fro1: [L], fro2: [L]}}
           # useful for backpropagation
  def __init__(self, num_inputs):
    num_w = num_inputs + 1  #number of weights is one more than number of inputs because of bias
  def add_node(level, fro, to):
    if not level in levels:
      levels[level] = {}

# oracle for whether a pt is above line y = mx + c
# can be linearly separated
def oracle_line(pt):
  m = 2
  c = 5
  if pt[1] > m * pt[0] + c:
    return 1
  else:
    return -1

# oracle for whether a series is sorted. requires a hidden node per adjacent pair of inputs
def oracle_sort(pt):
  if (pt[0] > pt[1] and pt[1] > pt[2]):
    return 1
  else:
    return -1

pp = Perceptron(3)
pp.train(10000, oracle_line)
print pp
print repr(pp.check(1000, oracle_line))+"%"

