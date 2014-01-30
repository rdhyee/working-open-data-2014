# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# http://ipython.org/ipython-doc/rel-1.1.0/api/generated/IPython.core.magics.pylab.html#
%pylab --no-import-all inline

# <headingcell level=1>

# Warm up with sequences, lists

# <headingcell level=2>

# Warm-up exercise I:  verifying sum of integers calculated by (young) Gauss

# <markdowncell>

# ![C. F. Gauss](http://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Carl_Friedrich_Gauss.jpg/220px-Carl_Friedrich_Gauss.jpg)
# 
# http://mathandmultimedia.com/2010/09/15/sum-first-n-positive-integers/
# 
# >  Gauss displayed his genius at an early age. According to anecdotes, when he was in primary school, he was punished by his teacher due to misbehavior.  He was told to add the numbers from 1 to 100. He was able to compute its sum, which is 5050, in a matter of seconds.
# 
# >  Now, how on earth did he do it?
# 
# See also:
# 
# * http://en.wikipedia.org/wiki/Carl_Friedrich_Gauss#Anecdotes
# * [The Gauss Christmath Special](http://youtu.be/sxnX5_LbBDU?t=4m52s) by [Vi Hart](http://en.wikipedia.org/wiki/Vi_Hart)
# 
# **Let's verify this result in a number of ways.  Take some time now to write some code to add up 1 to 100.**
# 
# Specifically:
# 
# * make use of [range](http://docs.python.org/2/library/functions.html#range)
# * try [xrange](http://docs.python.org/2/library/functions.html#xrange)
# * try an explicit loop vs `sum`
# * bonus:  try [itertool.count](http://docs.python.org/2/library/itertools.html#itertools.count) and [itertool.islice](http://docs.python.org/2/library/itertools.html#itertools.islice) -- these functions are Python *iterators*. 
# * See [Build a Basic Python Iterator](http://stackoverflow.com/a/24377/7782) and 
# [The Python yield keyword explained](http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained)
# 
# 
# **Beware:  in ipython w/ pylab mode, `sum` might be overwritten by numpy's sum -- use `__builtin__.sum` if you want http://docs.python.org/2/library/functions.html#sum as opposed to http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html** 

# <codecell>

# using loop and xrange

n = 100

s = 0L
for i in xrange(n+1):
    s += i
print s

# <codecell>

# using builtin sum and range

print range(101)
sum(range(101))

# <codecell>

# xrange
sum(xrange(101))

# <codecell>

# itertools is a great library
# http://docs.python.org/2/library/itertools.html#itertools.count
# itertools.count(start=0, step=1):
# "Make an iterator that returns evenly spaced values starting with step."

from itertools import islice, count
c = count(0, 1)

# <codecell>

# look at how count() works by repetively calling c.next()
print c.next()
print c.next()
print c.next()

# <codecell>

# let's add up using count and islice to limit how high we count

# also make sure we're also using the builtin sum 
# http://docs.python.org/2/library/functions.html#sum

__builtin__.sum(islice(count(0,1), 101L))

# <codecell>

# generator for the lowercase English alphabet

import string

def alpha1():
    m = list(string.lowercase)
    while m:
        yield m.pop(0)
    

# <codecell>

import string

# make a generator comprehension -- generate items on demand

k = (s for s in list(string.lowercase))
k

# <codecell>

k.next()

# <codecell>

# compare to k1, a list comprehension
k1 = [s for s in list(string.lowercase)]
k1

# <codecell>

# create my own version of itertools.count

def my_count(start, step):
    n = start
    while True:
        yield n
        n += step
        
__builtin__.sum(islice(my_count(0,1), 101L))

# <headingcell level=3>

# Triangular numbers

# <markdowncell>

# $T_n= \sum_{k=1}^n k = 1+2+3+ \dotsb +n = \frac{n(n+1)}{2} = {n+1 \choose 2}$

# <codecell>

from itertools import islice

def triangular():
    n = 1
    i = 1
    while True:
        yield n
        i +=1
        n += i

# <codecell>

for i, n in enumerate(islice(triangular(), 10)):
    print i+1, n

# <codecell>

list(islice(triangular(), 100))[-1]

# <codecell>

list(islice(triangular(),99,100))[0]

# <headingcell level=2>

# Warm Up Exercise II: Wheat and chessboard problem

# <markdowncell>

# http://en.wikipedia.org/wiki/Wheat_and_chessboard_problem :
# 
# > If a chessboard were to have wheat placed upon each square such that one grain were placed on the first square, two on the second, four on the third, and so on (doubling the number of grains on each subsequent square), how many grains of wheat would be on the chessboard at the finish?
# 
# > The total number of grains equals 18,446,744,073,709,551,615, which is a much higher number than most people intuitively expect.
# 
# * try using [pow](http://docs.python.org/2/library/functions.html#pow)

# <codecell>

# Legend of the Chessboard YouTube video

from IPython.display import YouTubeVideo
YouTubeVideo('t3d0Y-JpRRg')

# <codecell>

# generator comprehension

k  = (pow(2,n) for n in xrange(64))
k.next()

# <codecell>

__builtin__.sum((pow(2,n) for n in xrange(64)))

# <codecell>

pow(2,64) -1

# <headingcell level=1>

# Slicing/Indexing Review

# <markdowncell>

# http://stackoverflow.com/a/509295/7782
# 
# Use on any of the **sequence** types ([python docs on sequence types](http://docs.python.org/2/library/stdtypes.html#sequence-types-str-unicode-list-tuple-bytearray-buffer-xrange)):
# 
# > There are seven sequence types: strings, Unicode strings, lists, tuples, bytearrays, buffers, and xrange objects.
# 
# The use of square brackets are for accessing *slices* of sequence.

# <markdowncell>

# Let's remind ourselves of how to use slices
# 
# * `s[i]`
# * `s[i:j]`
# * `s[i:j:k]`
# * meaning of negative indices
# * 0-base counting
# 

# <codecell>

m = range(10)
m

# <codecell>

m[0]

# <codecell>

m[-1]

# <codecell>

m[::-1]

# <codecell>

m[2:3]

# <codecell>

import string
alphabet = string.lowercase

alphabet

# <codecell>

# 13 letter of the alphabet
alphabet[12]

# <markdowncell>

# **We will revisit generalized slicing in NumPy.**

# <headingcell level=1>

#  Import/naming conventions and pylab mode

# <markdowncell>

# <http://my.safaribooksonline.com/book/programming/python/9781449323592/1dot-preliminaries/id2699702>
# 
#     import numpy as np
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from pandas import Series, DataFrame
#     
# These imports done for you in `pylab` mode.
# 
# ## pylab mode
# 
#     ipython --help
#     
# yields
# 
#     --pylab=<CaselessStrEnum> (InteractiveShellApp.pylab)
#         Default: None
#         Choices: ['tk', 'qt', 'wx', 'gtk', 'osx', 'inline', 'auto']
#         Pre-load matplotlib and numpy for interactive use, selecting a particular
#         matplotlib backend and loop integration.

# <codecell>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame

# <headingcell level=1>

# NumPy

# <markdowncell>

# <http://www.numpy.org/>:
# 
# NumPy is the **fundamental package for scientific computing with Python**. It contains among other things:
# 
# * a powerful N-dimensional array object [let's start with 1 and 2 dimensions]
# * sophisticated (**broadcasting**) functions [what is *broadcasting*?]
# * tools for integrating C/C++ and Fortran code [why useful?]
# * useful linear algebra, Fourier transform, and random number capabilities
# 
# Besides its obvious scientific uses, NumPy can also be used as an efficient
# multi-dimensional container of **generic data**. **Arbitrary data-types** can be
# defined. This allows NumPy to seamlessly and speedily integrate with a wide
# variety of databases.
# 
# See `PfDA`, Chapter 4

# <headingcell level=2>

# ndarray.ndim, ndarray.shape

# <codecell>

# first: a numpy array of zero-dimension

a0 = np.array(5)
a0

# <markdowncell>

# use [shape](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.shape.html) to get a tuple of array dimensions

# <codecell>

a0.ndim, a0.shape

# <codecell>

# 1-d array
a1 = np.array([1,2])
a1.ndim, a1.shape

# <codecell>

# 2-d array

a2 = np.array(([1,2], [3,4]))
a2.ndim, a2.shape

# <headingcell level=2>

# dtype:  type of given ndarray

# <codecell>

a2.dtype

# <headingcell level=2>

# np.arange

# <markdowncell>

# [arange](http://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html#numpy.arange) is one instance of [`ndarray` creating function in NumPy](http://docs.scipy.org/doc/numpy/reference/routines.array-creation.html)
# 
# Compare to `xrange`.

# <codecell>

from numpy import arange

# <codecell>

type(arange(10))

# <codecell>

for k in arange(10):
    print k

# <codecell>

list(arange(10)) == list(xrange(10))

# <headingcell level=2>

# NumPy.ndarray.reshape

# <codecell>

#how to map 0..63 -> 2x2 array
a3 = np.arange(64).reshape(8,8)
a3

# <codecell>

# 2nd row, 3rd column --> remember index starts at 0
a3[1,2]

# <codecell>

# check that reshape works

for i in range(8):
    for j in range(8):
        if a3[i,j] != i*8 + j:
            print i, j

# <markdowncell>

# ##scalar multiplication
# 
# example of [broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html):
# 
# > The term broadcasting describes how numpy treats arrays with different shapes during arithmetic operations. Subject to certain constraints, the smaller array is “broadcast” across the larger array so that they have compatible shapes. Broadcasting provides a means of vectorizing array operations so that looping occurs in C instead of Python. It does this without making needless copies of data and usually leads to efficient algorithm implementations. There are, however, cases where broadcasting is a bad idea because it leads to inefficient use of memory that slows computation.

# <codecell>

2*a3

# <headingcell level=2>

# add 2 to all elements in a3

# <codecell>

a3+2

# <headingcell level=2>

# sorting

# <codecell>

# reverse sort -- best way?
#http://stackoverflow.com/a/6771620/7782

np.sort(np.arange(100))[::-1]

# <headingcell level=2>

# Boolean slice:  important novel type of slicing

# <markdowncell>

# **This stuff is a bit tricky** (see PfDA, pp. 89-92)
# 
# Consider example of picking out whole numbers less than 20 that are evenly divisible by 3.  Generate a list of such numbers

# <codecell>

# list comprehension

[i for i in xrange(20) if i % 3 == 0]

# <codecell>

a3 = np.arange(20) 
a3

# <codecell>

# basic indexing

print a3[0]
print a3[::-1]
print a3[2:5]

# <codecell>

np.mod(a3, 3)

# <codecell>

np.mod(a3, 3) == 0

# <codecell>

divisible_by_3 = np.mod(a3, 3) == 0

# <codecell>

a3[divisible_by_3]

# <codecell>

# if you want to understand this in terms of the overloaded operators -- don't worry if you don't get this.
a3.__getitem__(np.mod(a3,3).__eq__(0))

# <headingcell level=2>

# Exercise:  Calculate a series that holds all the squares less than 100

# <markdowncell>

# Use arange, np.sqrt, [astype](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.astype.html)

# <codecell>

a4 = arange(100)
a4sqrt = np.sqrt(a4)
a4[a4sqrt == a4sqrt.astype(np.int)]

# <headingcell level=2>

# We will come back to indexing later.

# <markdowncell>

# http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html

# <headingcell level=1>

# Pandas

# <headingcell level=2>

# pandas.Series

# <markdowncell>

# Make a series out of an array

# <codecell>

s1 = Series(arange(5))

# <markdowncell>

#   confirm that the type of s1 is  what you would expect

# <codecell>

type(s1)

# <markdowncell>

# show that the series is also an array

# <codecell>

s1.ndim, isinstance(s1, np.ndarray)

# <codecell>

s1.index

# <codecell>

import string
allTheLetters = string.lowercase
allTheLetters

# <codecell>

s2 = Series(data=arange(5), index=list(allTheLetters)[:5])
s2

# <codecell>

s2.index

# <markdowncell>

# http://my.safaribooksonline.com/book/programming/python/9781449323592/5dot-getting-started-with-pandas/id2828378 :
# 
# > Compared with a regular NumPy array, you can use values in the index when selecting single values or a set of values

# <codecell>

# can use both numeric indexing and the labels
s2[0], s2['a']

# <codecell>

for i in range(len(s2)):
    print i, s2[i]

# <markdowncell>

# it is possible conflict in indexing -- consider

# <codecell>

s3 = Series(data=['albert', 'betty', 'cathy'], index=[3,1, 0])
s3

# <codecell>

s3[0], list(s3)[0]

# <markdowncell>

# but slicing works to return specific numeric index

# <codecell>

s3[::-1]

# <codecell>

for i in range(len(s3)):
    print i, s3[i:i+1]

# <codecell>

s3.name = 'person names'
s3.name

# <codecell>

s3.index.name = 'confounding label'
s3.index.name

# <codecell>

s3

# <markdowncell>

# Important points remaining:
# 
# * "NumPy array operations, such as filtering with a boolean array, scalar multiplication, or applying math functions, will preserve the index-value link"
# * "Another way to think about a Series is as a fixed-length, ordered dict, as it is a mapping of index values to data values. It can be substituted into many functions that expect a dict"

# <headingcell level=2>

# Gauss & Chess revisited, using Series

# <markdowncell>

# You get some nice `matplotlib` integration via pandas

# <codecell>

# Gauss addition using np.arange, Series 

from pandas import Series
Series(arange(101).cumsum()).plot()

# <codecell>

from pandas import Series
Series((pow(2,k) for k in xrange(64)), dtype=np.float64).cumsum().plot()

# <headingcell level=2>

# Wheat and Chessboard w/ NumPy

# <markdowncell>

# http://docs.scipy.org/doc/numpy/reference/ufuncs.html

# <codecell>

# http://docs.scipy.org/doc/numpy/reference/generated/numpy.ones.html
from numpy import ones

# <codecell>

2*ones(64, dtype=np.int)

# <codecell>

arange(64)

# <codecell>

sum(np.power(2, arange(64, dtype=np.uint64)))

# <codecell>

sum(np.power(2*ones(64, dtype=np.uint64), arange(64))) 

# <codecell>

precise_ans = sum([pow(2,n) for n in xrange(64)])
np_ans = sum(np.power(2*ones(64, dtype=np.uint64), arange(64)))

precise_ans, np_ans


# <codecell>

# Raise an assertion if two items are not equal up to desired precision.
np.testing.assert_almost_equal(precise_ans, np_ans) is None

# <headingcell level=1>

# DataFrame

# <markdowncell>

# so many ways to use DataFrames....let's try them out in context of the census calculations

# <codecell>

# not really intuitive to me:  reversal of column/row
DataFrame(dict([('06', {'name': 'California', 'abbreviation':'CA'})] ))

# <codecell>

DataFrame([{'name': 'California', 'abbreviation':'CA'}], index= ['06'])

# <codecell>

Series(['06'], name='FIPS')

# <codecell>

DataFrame([{'name': 'California', 'abbreviation':'CA'}], 
          index=Series(['06'], name='FIPS'))

# <headingcell level=1>

# Advanced: Operator Overloading

# <codecell>

n0 = 5
n0 == 5

# <markdowncell>

# Now I thought I'd be able to use a `n0.__eq__(5)` but nope -- it's complicated -- see http://stackoverflow.com/questions/2281222/why-when-in-python-does-x-y-call-y-eq-x#comment2254663_2282795

# <codecell>

try:
    n0.__eq__(5)
except Exception as e:
    print e

# <markdowncell>

# can do: `int.__cmp__(x)`

# <codecell>

(n0.__cmp__(4), n0.__cmp__(5), n0.__cmp__(6))

# <markdowncell>

# how about ndarray?

# <codecell>

arange(5) == 2 

# <codecell>

# 
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.array_equal.html
np.array_equal(arange(5) == 2 , arange(5).__eq__(2))

# <headingcell level=2>

# Appendix: underlying mechanics of slicing

# <markdowncell>

# Useful if you want to understand how the slicing syntax really works.

# <codecell>

isinstance([1,2], list)

# <codecell>

isinstance(arange(5), list) # what does that mean -- could still be list-like

# <codecell>

l1 = range(5)

# <codecell>

type(l1)

# <codecell>

l1[0], l1.__getitem__(0), l1[0] == l1.__getitem__(0)

# <codecell>

l1[::-1], l1.__getitem__(slice(None, None, -1))

# <codecell>

ar1 = arange(5)
ar1[3], ar1.__getitem__(3)

# <codecell>

ar1 == 2

# <codecell>

ar1[ar1 == 2].shape

# <codecell>

ar1.__eq__(2)

# <codecell>

ar1.__getitem__(slice(2, 4, None))

# <codecell>

slice(ar1.__eq__(2), None, None)

# <codecell>

ar1.__getitem__(ar1.__eq__(2))

# <codecell>

ar1[:2], ar1.__getitem__(slice(2))

# <codecell>

ar1 + 7

# <codecell>

ar1.__add__(7)

# <codecell>

min(ar1 + 7)

# <codecell>

alphabet[:]

