# Simple AVL tree in Python

import sys, random

class AVLTree:
  class DummyNode:
    def weight(self):
      return 0
    def height(self):
      return 0
    def add(self, newval, parentbf=0):
      return AVLTree(newval)
    def traverse(self, fun):
      return 0

  dummy = DummyNode()

  def __init__(self, initialval):
    self.val = initialval
    self.left = AVLTree.dummy
    self.right = AVLTree.dummy
  def add(self, newval, parentbf=0):
    bf = self.right.height() - self.left.height()
    if newval < self.val:
      bf = bf - 1
      self.left = self.left.add(newval, bf)
    elif newval >= self.val:
      bf = bf + 1
      self.right = self.right.add(newval, bf)
    mid = self
    #balance this tree first
    if bf>1:
      mid = mid.rotate_left()
    elif bf<-1:
      mid = mid.rotate_right()
    #rotate for parent if needed
    if parentbf>1 and bf<0: #rotate right in preparation for right-left
      mid = mid.rotate_right()
    elif parentbf<-1 and bf>0: #rotate left in preparation for left-right
      mid = mid.rotate_left()
    return mid
#  def remove(self, val):
  def rotate_left(self):
    print "rotating left on %d" % self.val
    mid = self.right
    self.right = mid.left
    mid.left = self
    mid.draw()
    return mid
  def rotate_right(self):
    print "rotating right on %d" % self.val
    mid = self.left
    self.left = mid.right
    mid.right = self
    mid.draw()
    return mid
  def height(self):
    return max(self.left.height(), self.right.height()) + 1
  def weight(self):
    return self.left.weight() + self.right.weight() + 1
  def draw(self, indent=""):
    print(str(self.val))
    if self.left!=AVLTree.dummy:
      sys.stdout.write(indent + "|-")
      self.left.draw(indent + "| ")
    if self.right!=AVLTree.dummy:
      sys.stdout.write(indent + "\-")
      self.right.draw(indent + "  ")
  def traverse(self, fun):
    self.left.traverse(fun)
    fun(self)
    self.right.traverse(fun)

tree = AVLTree(10)
print "Tree initialized"
tree.draw()

print "depth = %s, weight = %s" % (tree.height(), tree.weight())
tree = tree.add(1)
print "1 added"
tree = tree.add(2)
print "2 added"
tree = tree.add(3)
print "3 added"
tree.draw()
print "depth = %s, weight = %s" % (tree.height(), tree.weight())

# randomly generate a tree of size and make sure that it is balanced at every node
def test(size):
  tree = AVLTree.dummy
  for i in xrange(size):
    newval = random.randint(0, size*50)
    print "adding %s" % newval
    tree = tree.add(newval)
    tree.draw()
  tree.draw()
  print "depth = %s, weight = %s" % (tree.height(), tree.weight())
  def g(x): 
    sys.stdout.write(str(x.val)+" ")
    if abs(x.left.height() - x.right.height()) > 1:
      raise Exception("FAILURE >>> Tree is not balanced")
  tree.traverse(g)
  print ""

test(10)
