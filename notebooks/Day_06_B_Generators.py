# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# **To practice using generators to yield geographical entities of various types.**  
# 
# Generators are a bit complicated, and I won't try to explain all the intricacies here.  I will show you how to use `yield` in a function definition to return a generator.  From [Definition of a generator](http://docs.python.org/2/glossary.html#term-generator):
# 
# <blockquote>A function which returns an iterator. It looks like a normal function except that it contains yield statements for producing a series a values usable in a for-loop or that can be retrieved one at a time with the next() function. Each yield temporarily suspends processing, remembering the location execution state (including local variables and pending try-statements). When the generator resumes, it picks-up where it left-off (in contrast to functions which start fresh on every invocation)</blockquote>
# 
# For some background on Python generators:
# 
# * [iterator - The Python yield keyword explained - Stack Overflow](http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained/231855#231855)
# * [Improve Your Python: 'yield' and Generators Explained](http://www.jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/) 
# 
# Why use generators: http://stackoverflow.com/a/102632/7782
# 
# <blockquote>Generators are good for calculating large sets of results (in particular calculations involving loops themselves) where you don't know if you are going to need all results, or where you don't want to allocate the memory for all results at the same time. </blockquote>
# 
# Also, let's also practice using [itertools.islice](http://www.python.org/doc//current/library/itertools.html#itertools.islice) and [enumerate](http://docs.python.org/2/library/functions.html#enumerate) -- two of my favorite constructions in Python

# <markdowncell>

# From http://api.census.gov/data/2010/sf1/geo.html, geographic entities we are specifically interested in this exercise:
# 
# * state-county
# * state-county-tract
# 
# * state-place
# * state-metropolitan statistical area/micropolitan statistical area
# * state-metropolitan statistical area/micropolitan statistical area-metropolitan division
# * state-combined statistical area

# <codecell>

# usual imports for numpy, pandas, matplotlib

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd

# <codecell>

# check that CENSUS_KEY is defined

import census
import us

import settings
assert settings.CENSUS_KEY is not None

# <codecell>

# instantiate our Census object

c = census.Census(key=settings.CENSUS_KEY)

# <headingcell level=1>

# A bit of warmup with Generators

# <codecell>

import string
print list(string.lowercase)

# <codecell>

def abcs():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
                'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
                'w', 'x', 'y', 'z']
    """a generator that returns """
    for letter in alphabet:
        yield letter

# a generator that gives you the letters of the alphabet a letter at a time         
say_abcs =  abcs()       

# <codecell>

# run this line over and over again to see the letters one at a time
say_abcs.next()

# <codecell>

# you can use list to grab all the items in an iterator.  But be careful if the number
# of items is large or even infinite!  In this case, we're ok

list(abcs())

# <markdowncell>

# Demonstration of how to use [enumerate](http://docs.python.org/2/library/functions.html#enumerate):
# 
# <blockquote>Return an enumerate object. sequence must be a sequence, an iterator, or some other object which supports iteration. The next() method of the iterator returned by enumerate() returns a tuple containing a count (from start which defaults to 0) and the values obtained from iterating over sequence</blockquote>
# 

# <codecell>

for (i, letter) in enumerate(abcs()):
    print i, letter

# <markdowncell>

# You can use itertools.islice [itertools.islice](http://www.python.org/doc//current/library/itertools.html#itertools.islice) to return parts of the iterator.
# 
# <blockquote>Make an iterator that returns selected elements from the iterable. If start is non-zero, then elements from the iterable are skipped until start is reached. Afterward, elements are returned consecutively unless step is set higher than one which results in items being skipped. If stop is None, then iteration continues until the iterator is exhausted, if at all; otherwise, it stops at the specified position. Unlike regular slicing, islice() does not support negative values for start, stop, or step. Can be used to extract related fields from data where the internal structure has been flattened (for example, a multi-line report may list a name field on every third line).</blockquote>

# <codecell>

# let's get the first 10 letters of the alphabet

from itertools import islice
list(islice(abcs(), 10))

# <codecell>

# you can use None to get all items in islice
# from docs: "If stop is None, then iteration continues until the iterator is exhausted,"

list(islice(abcs(), None))

# <codecell>

# itertools.count can in principle generate an infinite sequence
# http://www.python.org/doc//current/library/itertools.html#itertools.count

from itertools import count

# count starting zero
my_counter = count(0)

# <codecell>

# try it out 
my_counter.next()

# <codecell>

# DON'T do list(count(0))  -> you'll be trying to generate an infinite list
# but use an upper limit

list(islice(count(0),10))

# <codecell>

# start, stop
list(islice(count(),1,3))

# <headingcell level=1>

# Generator for US Counties

# <codecell>

# get the syntax down for getting counties from CA -- so that then we can use it later

r = c.sf1.get('NAME,P0010001', geo={'for':'county:*',
                                'in':'state:{fips}'.format(fips=us.states.CA.fips)})
r[:5]

# <markdowncell>

# With the census API, you can get the counties with one single call to the census API or state-by-state.  The `counties` generator below takes the first approach while `counties2` takes the second approach. Although `counties` is more efficient in most cases I can think of, it will be useful to know how to do calls on a state-by-state basis.  For example, when we to query on a census tract level or below, we will need to work on a state-by-state basis. 

# <codecell>

def counties(variables='NAME'):
    """ask for all the states"""
    
    # tabulate a set of fips codes for the states
    states_fips = set([s.fips for s in us.states.STATES])
    
    geo={'for':'county:*',
             'in':'state:*'}    
    for county in c.sf1.get(variables, geo=geo):
        # eliminate counties whose states aren't in a state or DC
        if county['state'] in states_fips:
            yield county
        

def counties2(variables='NAME'):
    """generator for all counties"""
    
    # since we can get all the counties in one call, 
    # this function is for demonstrating the use of walking through 
    # the states to get at the counties

    for state in us.states.STATES:
        geo={'for':'county:*',
             'in':'state:{fips}'.format(fips=state.fips)}
        for county in c.sf1.get(variables, geo=geo):
            yield county
        

# <codecell>

counties_list = list(counties('NAME,P0010001'))

# <codecell>

# add up the population to make sure we have the total right
counties_df = DataFrame(counties_list)
counties_df.P0010001 = counties_df.P0010001.astype('int')
counties_df.P0010001.sum()

# <markdowncell>

# One reason for writing all the counties in the form of a Python generator is tha you can easily control the number of counties we work with at any given time -- and then easily scaling out to get all of them. 

# <codecell>

# make a list of the first ten counties

from itertools import islice
list(islice(counties2(),10))

# <headingcell level=1>

# Generator for Census Tracts

# <markdowncell>

# The following generator loops through all the states to get at the individual counties to then get at the census tracts.

# <codecell>

def tracts(variables='NAME'):
    for state in us.states.STATES:
        
        # handy to print out state to monitor progress
        print state.fips, state
        counties_in_state={'for':'county:*',
             'in':'state:{fips}'.format(fips=state.fips)}
        
        for county in c.sf1.get('NAME', geo=counties_in_state):
            
            # print county['state'], county['NAME']
            tracts_in_county = {'for':'tract:*',
              'in': 'state:{s_fips} county:{c_fips}'.format(s_fips=state.fips, 
                                                            c_fips=county['county'])}
            
            for tract in c.sf1.get(variables,geo=tracts_in_county):
                yield tract
        

# <codecell>

r = list(islice(tracts('NAME,P0010001'),10))
tracts_df = DataFrame(r)
tracts_df.P0010001 = tracts_df.P0010001.astype('int')
tracts_df['FIPS'] = tracts_df.apply(lambda s: s['state']+s['county']+s['tract'], axis=1)
print "number of tracts", len(tracts_df)
print "total pop", tracts_df.P0010001.sum()
tracts_df.head()

# <markdowncell>

# Good to save the DataFrame so we can load up the census tracts without having call the census api again.
# 
# I/O: http://pandas.pydata.org/pandas-docs/dev/io.html
# 
# Today, we'll use [pickle format](http://docs.python.org/2/library/pickle.html) and look at other formats.

# <codecell>

TRACT_FILE_PICKLE = "tracts.pickle"

# UNCOMMENT THIS LINE TO SAVE YOUR FILE
# tracts_df.to_pickle(TRACT_FILE_PICKLE)

# <markdowncell>

# Let's read the DataFrame from disk to confirm that we were able to save the file properly.

# <codecell>

df = pd.read_pickle(TRACT_FILE_PICKLE)
df.head()

# <codecell>

# UNCOMMENT TO DO COMPARISON
# you can compare the saved file to the file from disk
# np.all(tracts_df == df)

