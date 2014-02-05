# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Purpose of This Notebook

# <markdowncell>

# * how to use `apply` on a pandas `Series` and `DataFrame`
# * show a bit about how `lambda` functions work

# <codecell>

# numpy and pandas related imports 

import numpy as np
from pandas import Series, DataFrame
import pandas as pd

# <headingcell level=1>

# Setup:  create Series and DataFrames

# <markdowncell>

# Let's make two Series and a DataFrame to use for our example

# <codecell>

# for example, using lower and uppercase English letters

import string
string.lowercase, string.uppercase

# <codecell>

# we can make a list composed of the individual lowercase letters 

list(string.lowercase)

# <codecell>

# create a pandas Series out of the list of lowercase letters

lower = Series(list(string.lowercase), name='lower')
print type(lower)
lower.head()

# <codecell>

# create a pandas Series out of the list of lowercase letters

upper = Series(list(string.uppercase), name='upper')

# <codecell>

# concatenate the two Series as columns, using axis=1 
# axis = 0 would result in two rows in the DataFrame

df = pd.concat((lower, upper), axis=1)
df.head()

# <headingcell level=1>

# Using apply

# <headingcell level=2>

# Series.apply

# <markdowncell>

# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.apply.html:
#    
#     Series.apply(func, convert_dtype=True, args=(), **kwds)
# 
#     Invoke function on values of Series.

# <codecell>

# Let's start by using Series.apply
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.apply.html

# first of all, it's useful to find a way to use apply to return the exact same Series

def identity(s):
    return s

lower.apply(identity)

# <codecell>

# show that identity yields the same Series -- first on element by element basis

lower.apply(identity) == lower

# <codecell>

# Check that match happens for every element in the Series using numpy.all
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.all.html

np.all(lower.apply(identity) == lower)

# <headingcell level=2>

# Let's use `lambda`

# <markdowncell>

# Sometimes it's convenient to write functions using `lambda`, especially short functions for doing a simple transformation of the parameters.  Only some functions can be rewritten with `lambda`. 

# <codecell>

def add_preface(s):
    return 'letter ' + s

lower.apply(add_preface)

# <codecell>

# rewrite with lambda

lower.apply(lambda s: 'letter ' + s)

# <headingcell level=3>

# Another illustration of apply

# <markdowncell>

# Another illustration of using `apply` -- using `ord` and `chr`

# <codecell>

# ord: Given a string of length one, return an integer representing the Unicode code 
# point of the character when the argument is a unicode object, or the value of the 
# byte when the argument is an 8-bit string. 
# http://docs.python.org/2.7/library/functions.html#ord

ord('a')

# <codecell>

# chr: Return a string of one character whose ASCII code is the integer i.
# http://docs.python.org/2.7/library/functions.html#chr

chr(97)

# <codecell>

# show that for the case of 'a', chr(ord()) returns what we start with:'a'

chr(ord('a')) == 'a'

# <codecell>

# we can test whether chr reverses ord for all the lower case letters
# note how we chain two apply together

np.all(lower.apply(ord).apply(chr) == lower)

# <markdowncell>

# Note that we read off a specific series from the DataFrame

# <codecell>

type(df.upper)

# <codecell>

# transform
df.upper.apply(lambda s: s.lower())

# <headingcell level=2>

# DataFrame.apply

# <markdowncell>

# `apply` can also be applied to a `DataFrame`
# 
# http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.apply.html
# 
#     DataFrame.apply(func, axis=0, broadcast=False, raw=False, reduce=None, args=(), **kwds)
#     Applies function along input axis of DataFrame.
# 
#     Objects passed to functions are Series objects having index either the DataFrame’s index (axis=0) or the columns (axis=1). Return type depends on whether passed function aggregates, or the reduce argument if the DataFrame is empty.

# <codecell>

# let's show that whether we use apply on columns (axis=0) or rows (axis=1), we get the same 
# result

def identity(s):
    return s

np.all(df.apply(identity, axis=0) == df.apply(identity, axis=1))

# <codecell>

# for each column, first lower and then upper, return the index

def index(s):
    return s.index

df.apply(index, axis=0)

# <codecell>

# for each row (axis=1), first lower and then upper, return the index 
# (which are the column names)

def index(s):
    return s.index

df.apply(index, axis=1)

# <codecell>

# it might be easier to see the difference between axis=0 vs axis=1
# by using join

# Consider what you get with

"".join(df.lower)

# <codecell>

# Now compare (axis=0)

df.apply(lambda s: "".join(s), axis=0)

# <codecell>

# join with axis=1

df.apply(lambda s: "".join(s), axis=1)

# <codecell>

# note that you can access use the index in your function passed to apply

df.apply(lambda s: s['upper'] + s['lower'], axis=1)

