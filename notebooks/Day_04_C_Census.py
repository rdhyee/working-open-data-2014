# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab --no-import-all inline

# <headingcell level=1>

# Some Context

# <markdowncell>

# The US Census is complex....so it's good, even essential, to have a framing question to guide your explorations so that you don't get distracted or lost.
# 
# I got into thinking of the census in 2002 when I saw a woman I knew in the following SF Chronicle article: 
# 
# [Claremont-Elmwood / Homogeneity in Berkeley? Well, yeah - SFGate](http://www.sfgate.com/bayarea/article/Claremont-Elmwood-Homogeneity-in-Berkeley-3306778.php)
# 
# I thought at that point it should be easy for regular people to do census calculations....
# 
# In the summer of 2013, I wrote the following note to Greg Wilson about diversity calculations:
# 
# [notes for Greg Wilson about an example Data Science Workflow](https://www.evernote.com/shard/s1/sh/b3f79cbc-c0c3-48a3-87b6-91da1b939783/1857ddee32d7baa04c55e629da05e0a7)
# 
# There's a whole cottage industry in musing on "diversity" in the USA:
# 
# * [The Most Diverse Cities In The US - Business Insider](http://www.businessinsider.com/the-most-diverse-cities-in-the-us-2013-7) -- using 4 categories:  Vallejo.
# 
# * [Most And Least Diverse Cities: Brown University Study Evaluates Diversity In The U.S.](http://www.huffingtonpost.com/2012/09/07/most-least-diverse-cities-brown-university-study_n_1865715.html)
# 
# * [The Top 10 Most Diverse Cities in America](http://www.cnbc.com/id/43066296) -- LA?
# 
# and let's not forget the [Racial Dot Map](http://bit.ly/rdotmap) and [some background](http://bit.ly/rdotmapintro).

# <codecell>

# Shows the version of pandas that we are using
!pip show pandas

# <codecell>

#  import useful classes of pandas
import numpy as np
import pandas as pd
from pandas import Series, DataFrame, Index

# <markdowncell>

# http://www.census.gov/developers/
# 
# Dependency: to start with -- let's use the Python module: https://pypi.python.org/pypi/census/
# 
#     pip install -U  census

# <markdowncell>

# Things we'd like to be able to do:
# 
# * calculate the population of California.
# * then calculate the population of every geographic entity going down to census block if possible.
# * for a given geographic unit, can we get the racial/ethnic breakdown?

# <headingcell level=1>

# Figuring out the Census Data is a Big Jigsaw Puzzle

# <markdowncell>

# Some starting points:
#     
#    * [Developers - U.S. Census Bureau](http://www.census.gov/developers/)
#    * [census/README.rst at master · sunlightlabs/census](https://github.com/sunlightlabs/census/blob/master/README.rst)
#     
# 
# We focus first on the API -- and I hope we can come back to processing the bulk data from [Census FTP site](http://www2.census.gov/)

# <headingcell level=1>

# Prerequisites: Getting and activating key

# <markdowncell>

# * fill out form at http://www.census.gov/developers/tos/key_request.html 
# 
# "Your request for a new API key has been successfully submitted. Please check your email. In a few minutes you should receive a message with instructions on how to activate your new key."
# 
# * click on link you'll get http://api.census.gov/data/KeySignup?validate={key}
# 
# Then create a settings.py in the same directory as this notebook (or somewhere else in your Python path) to hold `settings.CENSUS_KEY`

# <codecell>

import settings

# <codecell>

# This cell should run successfully if you have a string set up to represent your census key

try:
    import settings
    assert type(settings.CENSUS_KEY) == str or type(settings.CENSUS_KEY) == unicode
except Exception as e:
    print "error in importing settings to get at settings.CENSUS_KEY", e

# <headingcell level=1>

# states module

# <codecell>

# let's figure out a bit about the us module, in particular, us.states
# https://github.com/unitedstates/python-us

from us import states

for (i, state) in enumerate(states.STATES):
    print i, state.name, state.fips

# <markdowncell>

# Questions to ponder: How many states are in the list? Is DC included the states list?  How to access the territories?

# <headingcell level=1>

# Formulating URL requests by hand

# <markdowncell>

# It's immensely useful to be able to access the census API directly but creating a URL with the proper parameters -- as well as using the `census` package.

# <codecell>

import requests

# <codecell>

# get the total population of all states
url = "http://api.census.gov/data/2010/sf1?key={key}&get=P0010001,NAME&for=state:*".format(key=settings.CENSUS_KEY)

# <codecell>

# note the structure of the response
r = requests.get(url)

# <headingcell level=1>

# Total Population

# <codecell>

# FILL IN
# drop the header record
from itertools import islice
# total population including PR is 312471327



# <codecell>

# FILL IN
# exclude PR:  308745538

# <codecell>

# let's now create a DataFrame from r.json()

df = DataFrame(r.json()[1:], columns=r.json()[0])
df.head()

# <codecell>

# FILL IN
# calculate the total population using df



# <codecell>

# FILL IN -- now calculate the total population excluding Puerto Rico




# <headingcell level=1>

# Focusing on sf1 +2010 census

# <markdowncell>

# How to map out the geographical hierachy and pull out total population figures?
# 
#  1. Nation
#  1. Regions
#  1. Divisions
#  1. State
#  1. County
#  1. Census Tract
#  1. Block Group
#  1. Census Block
#  
# Questions
#  
# * What identifiers are used for these various geographic entities?  
# * Can we get an enumeration of each of these entities?
# * How to figure out which census tract, block group, census block one is in?
#  

# <headingcell level=2>

# Total Population of California

# <markdowncell>

# [2010 Census Summary File 1](http://www.census.gov/prod/cen2010/doc/sf1.pdf)
# 
# P0010001 is found in [2010 SF1 API Variables \[XML\]](http://www.census.gov/developers/data/sf1.xml) = "total population"

# <codecell>

from settings import CENSUS_KEY
import census

c=census.Census(settings.CENSUS_KEY) 
c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})

# <codecell>

"population of California: {0}".format(
        int(c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})[0]['P0010001']))

# <markdowncell>

# Let's try to get at the counties of California and their populations

# <codecell>

ca_counties = c.sf1.get(('NAME', 'P0010001'), geo={'for': 'county:*', 'in': 'state:%s' % states.CA.fips})

# <codecell>

# create a DataFrame, convert the 'P0010001' column
# show by descending population
df = DataFrame(ca_counties)
df['P0010001'] = df['P0010001'].astype('int')
df.sort_index(by='P0010001', ascending=False)

# <codecell>

#http://stackoverflow.com/a/13130357/7782
count,division = np.histogram(df['P0010001'])
df['P0010001'].hist(bins=division)

