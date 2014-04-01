# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# *Working with Open Data* Midterm (March 18, 2014)
# 
# There are **94** points in this exam:  2 each for the **47 questions**.  The questions are either **multiple choice** or **short answers**.  For **multiple choice**, just write the **number** of the choice selected.
# 
# 
# 
# Name: `______________________________________`
# 
# 
# `

# <headingcell level=1>

# World Population

# <markdowncell>

# Consider this code to construct a DataFrame of populations of countries.

# <codecell>

import json
import requests
from pandas import DataFrame

# read population in from JSON-formatted data derived from the Wikipedia
pop_json_url = "https://gist.github.com/rdhyee/8511607/" + \
     "raw/f16257434352916574473e63612fcea55a0c1b1c/population_of_countries.json"
pop_list= requests.get(pop_json_url).json()

df = DataFrame(pop_list)
df[:5]

# <markdowncell>

# Note the `dtypes` of the columns.

# <codecell>

df.dtypes

# <codecell>

s = sum(df[df[1].str.startswith('C')][2])
s

# <markdowncell>

# **Q1**: What is the relationship between `s` and the population of China, where `s` is defined as
# 
#     s = sum(df[df[1].str.startswith('C')][2])
#     
# 1. `s` is **greater** than the population of China
# 2. `s` is the **same** as the population of China
# 3. `s` is **less** than the population of China
# 4. `s` is not a number.
# 

# <markdowncell>

# **A1**:
# <pre>
# 1
# </pre>

# <codecell>

s2 = sum(df[df[1].str.startswith('X')][2])
s2

# <markdowncell>

# **Q2**: What is the relationship between `s2` and the population of China, where `s2` is defined by:
# 
#     s2 = sum(df[df[1].str.startswith('X')][2])
#     
# 1. `s2` is **greater** than the population of China
# 1. `s2` is the **same** as the population of China
# 1. `s2` is **less** than the population of China
# 1. `s2` is not a number.

# <markdowncell>

# **A2**:
# <pre>
# 3
# </pre>

# <codecell>

df.columns = ['Number','Country','Population']

# <markdowncell>

# **Q3**: What happens when the following statement is run?
# 
#     df.columns = ['Number','Country','Population']
#     
# 1. Nothing
# 1. `df` gets a new attribute called `columns`
# 1. `df`'s columns are renamed based on the list
# 1. Throws an exception

# <markdowncell>

# **A3**:
# <pre>
# 3
# </pre>

# <codecell>

try:
    df.columns = ['Number','Country']
except Exception as e:
    print e

# <markdowncell>

# **Q4**: This statement does the following
# 
#     df.columns = ['Number','Country']
#     
# 1. Nothing
# 1. `df` gets a new attribute called `columns`
# 1. `df`'s columns are renamed based on the list
# 1. Throws an exception

# <markdowncell>

# **A4**:
# <pre>
# 4
# 
# </pre>

# <codecell>

df.columns = ['Number','Country','Population']
s=sum(df[df['Country'].str.startswith('C')]['Population'])
s

# <markdowncell>

# **Q5**: How would you rewrite the following statement to get the same result as
# 
#     s = sum(df[df[1].str.startswith('C')][2])
# 
# after running:
# 
#     df.columns = ['Number','Country','Population']

# <markdowncell>

# **A5**:
# <pre>
# 
# 
# s=sum(df[df['Country'].str.startswith('C')]['Population'])
# 
# 
# </pre>

# <codecell>

len(df[df["Population"]>1000000000])

# <markdowncell>

# **Q6**.  What is
# 
# ```Python
#     len(df[df["Population"] > 1000000000])
# ```

# <markdowncell>

# **A6**:
# <pre>
# 
# 2
# </pre>

# <codecell>

";".join(df[df['Population']>1000000000]['Country'].apply(lambda s: s[0]))

# <markdowncell>

# **Q7**. What is
# 
# ```Python
#     ";".join(df[df['Population']>1000000000]['Country'].apply(lambda s: s[0]))
# ```

# <markdowncell>

# **A7**:
# <pre>
# C;I
# 
# </pre>

# <codecell>

len(";".join(df[df['Population']>1000000000]['Country'].apply(lambda s: s[0])))

# <markdowncell>

# **Q8**. What is
# 
#  ```Python
#       len(";".join(df[df['Population']>1000000000]['Country'].apply(lambda s: s[0])))
#  ```

# <markdowncell>

# **A8**:
# <pre>
# 
# 3
# </pre>

# <headingcell level=1>

# Pandas Series

# <codecell>

from pandas import DataFrame, Series
import numpy as np

s1 = Series(np.arange(-1,4))
s1

# <codecell>

s1 + 1

# <markdowncell>

# **Q9**: What is
# 
# ```Python
#     s1 + 1
# ```

# <markdowncell>

# **A9**:
# <pre>
# 0    0
# 1    1
# 2    2
# 3    3
# 4    4
# </pre>

# <codecell>

s1.apply(lambda k: 2*k).sum()

# <markdowncell>

# **Q10**: What is
# 
# ```Python
# s1.apply(lambda k: 2*k).sum()
# ```

# <markdowncell>

# **A10**:
# <pre>
# 10
# </pre>

# <codecell>

s1.cumsum()[3]

# <markdowncell>

# **Q11**: What is 
# 
# ```Python
#     s1.cumsum()[3]
# ```

# <markdowncell>

# **A11**:
# <pre>
# 2
# </pre>

# <codecell>

s1.cumsum() - s1.cumsum()

# <markdowncell>

# **Q12**: What is
# 
#     s1.cumsum() - s1.cumsum()

# <markdowncell>

# **A12**:
# <pre>
# 0    0
# 1    0
# 2    0
# 3    0
# 4    0
# </pre>

# <codecell>

len(s1.cumsum() - s1.cumsum())

# <markdowncell>

# **Q13**. What is
# 
# ```Python
#     len(s1.cumsum() - s1.cumsum())
# ```

# <markdowncell>

# **A13**:
# <pre>
# 5
# </pre>

# <codecell>

np.any(s1 > 2)

# <markdowncell>

# **Q14**: What is
# 
#     np.any(s1 > 2)

# <markdowncell>

# **A14**:
# <pre>
# True
# </pre>

# <codecell>

np.all(s1<3)

# <markdowncell>

# **Q15**. What is
# 
# ```Python
#     np.all(s1<3)
# ```

# <markdowncell>

# **A15**:
# <pre>
# False
# </pre>

# <headingcell level=1>

# Census API

# <markdowncell>

# Consider the following code to load population(s) from the Census API.

# <codecell>

from census import Census
from us import states

import settings

c = Census(settings.CENSUS_KEY)
c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})

# <markdowncell>

# **Q16**: What is the purpose of `settings.CENSUS_KEY`?
# 
# 1. It is the password for the Census Python package
# 1. It is an API Access key for authentication with the Census API
# 1. It is an API Access key for authentication with Github
# 1. It is key shared by all users of the Census API

# <markdowncell>

# **A16**:
# <pre>
# 2
# </pre>

# <markdowncell>

# **Q17**. When we run
# 
# ```bash
# pip install census
# ```
# 
# we are:
# 
# 1. installing a Python module from PyPI
# 1. installing the Python module census from continuum.io's repository
# 1. signing ourselves up for a census API key
# 1. None of the above

# <markdowncell>

# **A17**:
# <pre>
# 1
# </pre>

# <markdowncell>

# Consider `r1` and `r2`:

# <codecell>

r1 = c.sf1.get(('NAME', 'P0010001'), {'for': 'county:*', 'in': 'state:%s' % states.CA.fips})
r2 = c.sf1.get(('NAME', 'P0010001'), {'for': 'county:*', 'in': 'state:*' })

len(r1), len(r2)

# <markdowncell>

# **Q18**: What is the difference between `r1` and `r2`?
# 
# ```Python
#     r1 = c.sf1.get(('NAME', 'P0010001'), {'for': 'county:*', 'in': 'state:%s' % states.CA.fips})
#     r2 = c.sf1.get(('NAME', 'P0010001'), {'for': 'county:*', 'in': 'state:*' })
# ```

# <markdowncell>

# **A18**:
# `r1` is a list holding the name and total population from the 2010 US Census for every county in California.
# 
# `r2` holds the name and total population from the 2010 US Census for every county in all US states, DC, and Puerto Rico.

# <markdowncell>

# **Q19**. What's the relationship between `len(r1)` and `len(r2)`?
# 
# 1. `len(r1)` is less than `len(r2)`
# 1. `len(r1)` equals `len(r2)`
# 1. `len(r1)` is greater than `len(r2)`
# 1. None of the above

# <markdowncell>

# **A19**:
# <pre>
# 1
# </pre>

# <markdowncell>

# **Q20**: Which is a correct geographic hierarchy?
# 
# Nation > States = Nation is subdivided into States
# 
# 1. Counties > States
# 1. Counties > Block Groups > Census Tracks
# 1. Census Tracts > Block Groups > Census Blocks
# 1. Places > Counties

# <markdowncell>

# **A20**:
# <pre>
# 3
# </pre>

# <codecell>

from pandas import DataFrame
import numpy as np
from census import Census
from us import states

import settings

c = Census(settings.CENSUS_KEY)

r = c.sf1.get(('NAME', 'P0010001'), {'for': 'state:*'})
df1 = DataFrame(r)

df1.head()

# <codecell>

len(df1)

# <markdowncell>

# **Q21**: Why does `df` have 52 items? Please explain

# <markdowncell>

# **A21**:
# 
# When queried for "states", the US Census API returns data for the 50 states, the District of Columbia, and Puerto Rico: (50+1+1 = 52 entities).

# <markdowncell>

# Consider the two following expressions:

# <codecell>

print df1.P0010001.sum()
print
print df1.P0010001.astype(int).sum()

# <markdowncell>

# **Q22**: Why is `df1.P0010001.sum()` different from `df1.P0010001.astype(int).sum()`? 

# <markdowncell>

# **A22**:
# The data type of `df1.P0010001` is a string.  Hence, performing `sum` on it concatenates the string representation of populations into a longer string.  In contrast, once `df1.P0010001` is converted into integers via `df1.P0010001.astype(int)`, a `sum` operation adds up all the populations into a single integer.

# <codecell>

df1.P0010001 = df1.P0010001.astype(int)
df1[['NAME','P0010001']].sort('P0010001', ascending=True).head()

# <markdowncell>

# **Q23**: Describe the output of the following:
# 
# ```Python
# df1.P0010001 = df1.P0010001.astype(int)
# df1[['NAME','P0010001']].sort('P0010001', ascending=True).head()
# ```

# <markdowncell>

# **A23**:
# A DataFrame (with 5 rows and 2 columns (NAME, P0010001)) listing the 5 least populous states in ascending order by population.  

# <codecell>

df1.set_index('NAME', inplace=True)
df1.ix['Nebraska']

# <markdowncell>

# **Q24**: After running:
# 
# ```Python
#     df1.set_index('NAME', inplace=True)
# ```
# 
# how would you access the Series for the state of Nebraska?
# 
# 1. `df1['Nebraska']`
# 1. `df1[1]`
# 1. `df1.ix['Nebraska']`
# 1. `df1[df1['NAME'] == 'Nebraska']`

# <markdowncell>

# **A24**:
# <pre>
# 3
# </pre>

# <codecell>

len(states.STATES)

# <markdowncell>

# **Q25**. What is `len(states.STATES)`?

# <markdowncell>

# **A25**:
# <pre>
# 51
# </pre>

# <codecell>

len(df1[np.in1d(df1.state, [s.fips for s in states.STATES])])

# <markdowncell>

# **Q26**. What is
# 
# ```Python
# len(df1[np.in1d(df1.state, [s.fips for s in states.STATES])])
# ```

# <markdowncell>

# **A26**:
# <pre>
# 51
# </pre>

# <markdowncell>

# In the next question, we will make use of the negation operator `~`.  Take a look at a specific example

# <codecell>

~Series([True, True, False, True])

# <codecell>

list(df1[~np.in1d(df1.state, [s.fips for s in states.STATES])].index)[0]

# <markdowncell>

# **Q27**. What is
# 
# ```Python
#     list(df1[~np.in1d(df1.state, [s.fips for s in states.STATES])].index)[0]
# ```    

# <markdowncell>

# **A27**:
# <pre>
# Puerto Rico
# </pre>

# <markdowncell>

# Consider `pop1` and `pop2`:

# <codecell>

pop1 = df1['P0010001'].astype('int').sum() 
pop2 = df1[np.in1d(df1.state, [s.fips for s in states.STATES])]['P0010001'].astype('int').sum()

pop1-pop2

# <markdowncell>

# **Q28**. What does `pop11 - pop2` represent?

# <markdowncell>

# **A28**:
# The population of Puerto Rico in the 2010 Census.

# <headingcell level=1>

# Generator and range

# <codecell>

sum(range(1, 101))

# <markdowncell>

# **Q29**. Given that
# 
#     range(10)
#     
# is
# 
#     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# 
# How to get the total of every integer from 1 to 100?
# 
# 1. `sum(range(1, 101))`
# 1. `sum(range(100))`
# 1. `sum(range(1, 100))`
# 1. None of the above

# <markdowncell>

# **A29**:
# <pre>
# 1
# </pre>

# <codecell>

# itertools is a great library
# http://docs.python.org/2/library/itertools.html#itertools.count
# itertools.count(start=0, step=1):
# "Make an iterator that returns evenly spaced values starting with step."

from itertools import islice, count
c = count(0, 1)
print c.next()
print c.next()

# <markdowncell>

# **Q30**. What output is produced from
# 
# ```Python
# # itertools is a great library
# # http://docs.python.org/2/library/itertools.html#itertools.count
# # itertools.count(start=0, step=1):
# # "Make an iterator that returns evenly spaced values starting with step."
# 
# from itertools import islice, count
# c = count(0, 1)
# print c.next()
# print c.next()
# ```

# <markdowncell>

# **A30**:
# <pre>
# 0
# 1
# </pre>

# <codecell>

(2*Series(np.arange(101))).sum()

# <markdowncell>

# **Q31**. Recalling that 
# 
#     1+2+3+...+100 = 5050
#     
# what is:
# 
# ```Python
# (2*Series(np.arange(101))).sum()
# ```

# <markdowncell>

# **A31**:
# <pre>
# 10100
# </pre>

# <headingcell level=1>

# Census Places

# <markdowncell>

# Consider the follow generator that we used to query for census places.

# <codecell>

import pandas as pd
from pandas import DataFrame

import census
import settings
import us

from itertools import islice

c=census.Census(settings.CENSUS_KEY)

def places(variables="NAME"):
    
    for state in us.states.STATES:
        geo = {'for':'place:*', 'in':'state:{s_fips}'.format(s_fips=state.fips)}
        for place in c.sf1.get(variables, geo=geo):
            yield place
   

# <markdowncell>

# Now we compute a DataFrame for the places: `places_df`

# <codecell>

r = list(islice(places("NAME,P0010001"), None))
places_df = DataFrame(r)
places_df.P0010001 = places_df.P0010001.astype('int')

print "number of places", len(places_df)
print "total pop", places_df.P0010001.sum()
places_df.head()

# <markdowncell>

# We display the most populous places from California

# <codecell>

places_df[places_df.state=='06'].sort_index(by='P0010001', ascending=False).head()

# <codecell>

places_df['label'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)
places_df.ix[3122]['label']

# <markdowncell>

# **Q32**. Given
# 
#     places_df[places_df.state=='06'].sort_index(by='P0010001', ascending=False).head()
# 
# is
# 
# <div style="max-height:1000px;max-width:1500px;overflow:auto;">
# <table border="1" class="dataframe">
#   <thead>
#     <tr style="text-align: right;">
#       <th></th>
#       <th>NAME</th>
#       <th>P0010001</th>
#       <th>place</th>
#       <th>state</th>
#     </tr>
#   </thead>
#   <tbody>
#     <tr>
#       <th>2714</th>
#       <td>   Los Angeles city</td>
#       <td> 3792621</td>
#       <td> 44000</td>
#       <td> 06</td>
#     </tr>
#     <tr>
#       <th>3112</th>
#       <td>     San Diego city</td>
#       <td> 1307402</td>
#       <td> 66000</td>
#       <td> 06</td>
#     </tr>
#     <tr>
#       <th>3122</th>
#       <td>      San Jose city</td>
#       <td>  945942</td>
#       <td> 68000</td>
#       <td> 06</td>
#     </tr>
#     <tr>
#       <th>3116</th>
#       <td> San Francisco city</td>
#       <td>  805235</td>
#       <td> 67000</td>
#       <td> 06</td>
#     </tr>
#     <tr>
#       <th>2425</th>
#       <td>        Fresno city</td>
#       <td>  494665</td>
#       <td> 27000</td>
#       <td> 06</td>
#     </tr>
#   </tbody>
# </table>
# <p>5 rows × 4 columns</p>
# </div>
# <br/>
# what is
# 
# ```Python
# places_df.ix[3122]['label']
# ```
# 
# after we add the `label` column with:
# 
# ```Python
# places_df['label'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)
# ```

# <markdowncell>

# **A32**:
# <pre>
# 0668000
# </pre>

# <codecell>

places_df["NAME"][3122]

# <markdowncell>

# **Q33**.  What is
# 
# ```Python
# places_df["NAME"][3122]
# ```

# <markdowncell>

# **A33**:
# <pre>
# San Jose city
# </pre>

# <headingcell level=1>

# Alphabet and apply

# <markdowncell>

# Now let's set up a DataFrame with some letters and properties of letters.

# <codecell>

# numpy and pandas related imports 

import numpy as np
from pandas import Series, DataFrame
import pandas as pd

# for example, using lower and uppercase English letters

import string

lower = Series(list(string.lowercase), name='lower')
upper = Series(list(string.uppercase), name='upper')

df2 = pd.concat((lower, upper), axis=1)
df2['ord'] = df2['lower'].apply(ord)
df2.head()

# <markdowncell>

# Note that `string.upper` takes a letter and returns its uppercase version.  For example:

# <codecell>

string.upper('b')

# <codecell>

np.all(df2['lower'].apply(string.upper) == df2['upper'])

# <markdowncell>

# **Q34**. What is
# 
# ```Python
# np.all(df2['lower'].apply(string.upper) == df2['upper'])
# ```

# <markdowncell>

# **A34**:
# <pre>
# True
# </pre>

# <codecell>

df2.apply(lambda s: s['lower'] + s['upper'], axis=1)[6]

# <markdowncell>

# **Q35**. What is
# 
# ```Python
# df2.apply(lambda s: s['lower'] + s['upper'], axis=1)[6]
# ```

# <markdowncell>

# **A35**:
# <pre>
# gG
# </pre>

# <headingcell level=1>

# Berkeley I School generator

# <markdowncell>

# Please remind yourself what `enumerate` does.

# <codecell>

words = ['Berkeley', 'I', 'School']

for (i, word) in islice(enumerate(words),1):
    print (i, word)

# <codecell>

list(enumerate(words))[2][1]

# <markdowncell>

# **Q36**. What is 
# 
# ```Python
# list(enumerate(words))[2][1]
# ```

# <markdowncell>

# **A36**:
# <pre>
# School
# </pre>

# <markdowncell>

# Now consider the generator `g2`

# <codecell>

def g2():
    words = ['Berkeley', 'I', 'School']
    for word in words:
        if word != 'I':
            for letter in list(word):
                yield letter
            
my_g2 = g2()

# <codecell>

len(list(my_g2))

# <markdowncell>

# **Q37**. What is
# 
# ```Python
# len(list(my_g2))
# ```

# <markdowncell>

# **A37**:
# <pre>
# 14
# </pre>

# <codecell>

def g3():
    words = ['Berkeley', 'I', 'School']
    for word in words:
        yield words

# <codecell>

len(list(g3()))

# <markdowncell>

# **Q38**. What is
# 
# ```Python
# len(list(g3()))
# ```

# <markdowncell>

# **A38**:
# <pre>
# 3
# </pre>

# <headingcell level=1>

# Groupby

# <markdowncell>

# Consider using `groupby` with a DataFrame with states.

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
            
# make a dataframe from the total populations of states in the 2010 Census

df = DataFrame(states('NAME,P0010001'))
df.P0010001 = df.P0010001.astype('int')
df['first_letter'] = df.NAME.apply(lambda s:s[0])

df.head()

# <markdowncell>

# For reference, here's a list of all the states

# <codecell>

print list(df.NAME)

# <codecell>

df.groupby('first_letter').apply(lambda g:list(g.NAME))['C']

# <markdowncell>

# **Q39**. What is
# 
# 
# ```Python
# df.groupby('first_letter').apply(lambda g:list(g.NAME))['C']
# ```

# <markdowncell>

# **A39**:
# <pre>
# [u'California', u'Colorado', u'Connecticut']
# </pre>

# <codecell>

df.groupby('first_letter').apply(lambda g:len(g.NAME))['A']

# <markdowncell>

# **Q40**. What is
# 
# 
# ```Python
# df.groupby('first_letter').apply(lambda g:len(g.NAME))['A']
# ```

# <markdowncell>

# **A40**:
# <pre>
# 4
# </pre>

# <codecell>

df.groupby('first_letter').agg('count')['first_letter']['P']

# <markdowncell>

# **Q41**. What is
# 
# 
# ```Python
# df.groupby('first_letter').agg('count')['first_letter']['P']
# ```

# <markdowncell>

# **A41**:
# <pre>
# 1
# </pre>

# <codecell>

len(df.groupby('NAME'))

# <markdowncell>

# **Q42**. What is
# 
# ```Python
# len(df.groupby('NAME'))
# ```

# <markdowncell>

# **A42**:
# <pre>
# 51
# </pre>

# <headingcell level=1>

# Diversity Index

# <markdowncell>

# Recall the code from the diversity calculations

# <codecell>

def normalize(s):
    """take a Series and divide each item by the sum so that the new series adds up to 1.0"""
    total = np.sum(s)
    return s.astype('float') / total

def entropy(series):
    """Normalized Shannon Index"""
    # a series in which all the entries are equal should result in normalized entropy of 1.0
    
    # eliminate 0s
    series1 = series[series!=0]

    # if len(series) < 2 (i.e., 0 or 1) then return 0
    
    if len(series1) > 1:
        # calculate the maximum possible entropy for given length of input series
        max_s = -np.log(1.0/len(series))
    
        total = float(sum(series1))
        p = series1.astype('float')/float(total)
        return sum(-p*np.log(p))/max_s
    else:
        return 0.0

def gini_simpson(s):
    # https://en.wikipedia.org/wiki/Diversity_index#Gini.E2.80.93Simpson_index
    s1 = normalize(s)
    return 1-np.sum(s1*s1)

# <markdowncell>

# **Q43**.  Suppose you have 10 people and 5 categories, how you would you maximize the Shannon entropy?
# 
# 1. Regardless of how you distribute the people, you'll get the same entropy.
# 1. Put 10 people in any single category, and then 0 in the rest.
# 1. Distribute the people evenly over all the categories.
# 1. Put 5 people in each category.

# <markdowncell>

# **A43**:
# <pre>
# 3
# </pre>

# <codecell>

entropy(Series([0,0,10,0,0]))

# <markdowncell>

# **Q44**. What is
# 
# ```Python
# entropy(Series([0,0,10,0,0]))
# ```

# <markdowncell>

# **A44**:
# <pre>
# 0
# </pre>

# <codecell>

entropy(Series([10,0,0,0,0]))

# <markdowncell>

# **Q45**. What is
# 
# ```Python
# entropy(Series([10,0,0,0,0]))
# ```

# <markdowncell>

# **A45**:
# <pre>
# 0
# </pre>

# <codecell>

entropy(Series([1,1,1,1,1]))

# <markdowncell>

# **Q46**. What is
# 
# ```Python
# entropy(Series([1,1,1,1,1]))
# ```

# <markdowncell>

# **A46**:
# <pre>
# 1
# </pre>

# <codecell>

gini_simpson(Series([2,2,2,2,2]))

# <markdowncell>

# **Q47**. What is
# 
# ```Python
# gini_simpson(Series([2,2,2,2,2]))
# ```

# <markdowncell>

# 
# **A47**:
# <pre>
# 
# 0.8
# </pre>

