# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# What this notebook is about

# <markdowncell>

# Goal:
#     
#   * to learn about the basics of Pandas groupby operations using the census information about states
#  
# References:
# 
# * [Group By: split-apply-combine — pandas 0.13.1 documentation](http://pandas.pydata.org/pandas-docs/stable/groupby.html)
# 
# * [Python for Data Analysis > 9. Data Aggregation and Group Operations > GroupBy Mechanics : Safari Books Online](http://my.safaribooksonline.com/book/programming/python/9781449323592/9dot-data-aggregation-and-group-operations/id2805988)
# 
# Note the **split-apply-combine** framework of thinking
# 
# 
#  

# <headingcell level=1>

# Version of pandas

# <codecell>

# note version of pandas
import pandas
pandas.__version__

# <headingcell level=1>

# Setup for grabbing state-related census data

# <codecell>

import us
import census
import settings

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from itertools import islice

c = census.Census(settings.CENSUS_KEY)

def states(variables='NAME'):
    geo={'for':'state:*'}
    
    states_fips = set([state.fips for state in us.states.STATES])
    # need to filter out non-states
    for r in c.sf1.get(variables, geo=geo, year=2010):
        if r['state'] in states_fips:
            yield r

# <codecell>

# make a dataframe from the total populations of states in the 2010 Census

df = DataFrame(states('NAME,P0010001'))
df.P0010001 = df.P0010001.astype('int')
df.head()

# <codecell>

# check that that we have the right total population

df.P0010001.sum() == 308745538 

# <codecell>

# add a column with the first letter 
# we'll be grouping states based on the first letter of the state NAME

df['first_letter'] = df.NAME.apply(lambda s:s[0])
df.head()

# <markdowncell>

# [Group By: split-apply-combine — pandas 0.13.1 documentation](http://pandas.pydata.org/pandas-docs/stable/groupby.html)

# <markdowncell>

# Possible to do grouping in [many ways](http://pandas.pydata.org/pandas-docs/stable/groupby.html#splitting-an-object-into-groups).  "The mapping can be specified many different ways":
# 
# * A Python function, to be called on each of the axis labels
# * A list or NumPy array of the same length as the selected axis
# * A dict or Series, providing a label -> group name mapping
# * For DataFrame objects, a string indicating a column to be used to group. Of course df.groupby('A') is just syntactic sugar for df.groupby(df['A']), but it makes life simpler
# * A list of any of the above things
# 
# 
# We can also group by columns, axis=1, but such functionality is not demonstrated in this notebook.

# <codecell>

# we can explicitly name df.first_letter

grouped = df.groupby(df.first_letter)
grouped

# <codecell>

# shorthand for df.first_letter
# same thing as df.groupby(df.first_letter)

grouped = df.groupby('first_letter')
grouped

# <codecell>

# count the number of states with each first letter -- look at top of the resulting DataFrame

grouped.count().head()

# <codecell>

# count the number of states with each first letter -- look at bottom of the resulting DataFrame

grouped.count().tail()

# <codecell>

# we didn't have to explicitly create a new column -- we could groupby on a dynamically generated Series
# note the use of str operations on df.NAME: 
# http://pandas.pydata.org/pandas-docs/stable/basics.html#vectorized-string-methods

df.groupby(df.NAME.str.slice(0,1)).sum()

# <codecell>

# we can get groups of indexes

df.groupby('first_letter').groups

# <codecell>

# loop through all groups --> here just the first one

for name, group in islice(df.groupby('first_letter'),1):
    print(name)
    print type(group) # yes -- a DataFrame
    print group.index
    print(group),

# <codecell>

# how about accessing group 'C'?
# http://stackoverflow.com/a/14734627/7782
# http://stackoverflow.com/questions/19804282/in-pandas-is-there-something-like-a-groupby-get-group-but-with-an-optional-defa
# http://pandas.pydata.org/pandas-docs/dev/generated/pandas.core.groupby.GroupBy.get_group.html

grouped = df.groupby('first_letter')
grouped.get_group('C')

# <codecell>

# total population of states starting with 'C'

grouped.get_group('C').P0010001.sum()

# <headingcell level=1>

# Aggregation

# <codecell>

# generate a Series of total populations by first letter

grouped = df.groupby('first_letter')
s = grouped['P0010001'].sum()
s

# <codecell>

# sort the list to get the most populous groups
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.sort.html
# note sorting in place

s.sort(ascending=False)
s

# <codecell>

s.index

# <codecell>

# first pass at pulling together the letter, the total population, and the list of corresponding states

for k in s.index:
    print k, s[k], list(grouped.get_group(k).NAME)

# <codecell>


# <codecell>

# let's try this again and try to do this in a more idiomatic Pandas fashion
# ideally, generate a DataFrame with a NAME column that is a list of all states with the same first letter

# It turns out that apply can come to the rescue
# here' calculate the list of NAMEs

# http://pandas.pydata.org/pandas-docs/dev/groupby.html#flexible-apply
# http://stackoverflow.com/questions/19530568/can-pandas-groupby-aggregate-into-a-list-rather-than-sum-mean-etc

df.groupby("first_letter").apply(lambda x: list(x['NAME']))

# <codecell>

# apply can be used to add up the populations by group

df.groupby("first_letter").apply(lambda x: np.sum(x['P0010001']))

# <codecell>

# make a tuple out of the list of names and the population

df.groupby("first_letter").apply(lambda x:( list(x['NAME']), np.sum(x['P0010001'])))

# <codecell>

# remind ourselves on how to turn a tuple into a Series with a small example

Series(([1,2],2), index=['one','two'])

# <codecell>

# we're ready to make a new DataFrame

df.groupby("first_letter").apply(lambda x:Series((list(x['NAME']), np.sum(x['P0010001'])), 
                                                 index=['states','total_pop']))

# <codecell>

df2 = df.groupby("first_letter").apply(lambda x:Series((list(x['NAME']), np.sum(x['P0010001'])), 
                                                 index=['states','total_pop'])).sort_index(by='total_pop',ascending=False)

# <codecell>

# make sure you understand the syntax here:
# .ix: http://pandas.pydata.org/pandas-docs/dev/indexing.html#advanced-indexing-with-ix
# ability to grab columns by name to return a new DataFrame

df2.ix['C'][['states','total_pop']]

# <codecell>

print "states that start with 'C'", df2.ix['C']['states']

# <codecell>

print "total population of states that start with 'C'", df2.ix['C']['total_pop']

# <codecell>


