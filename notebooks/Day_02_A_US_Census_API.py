# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goal

# <markdowncell>

# Let's get set up to use the US Census API:
# 
#     http://www.census.gov/developers/

# <markdowncell>

# Things we'd like to be able to do:
# 
# * calculate the population of California.
# * then calculate the population of every geographic entity going down to census block if possible.
# * for a given geographic unit, can we get the racial/ethnic breakdown?
# 
# It's useful to make ties to the county-type calculation we do with the downloaded census files.

# <headingcell level=1>

# Installing census, a useful Python module

# <markdowncell>

# Dependency: to start with -- let's use the Python module: https://pypi.python.org/pypi/census/
# 
#     pip install -U  census

# <headingcell level=1>

# Getting and activating an API key

# <markdowncell>

# To use the census API, you will need an API key
# 
# * fill out form at http://www.census.gov/developers/tos/key_request.html 
# 
# "Your request for a new API key has been successfully submitted. Please check your email. In a few minutes you should receive a message with instructions on how to activate your new key."
# 
# * click on link you'll get a link of the form http://api.census.gov/data/KeySignup?validate={key} -- where {key} is the one the Census Bureau will send you.
# 
# Then create a settings.py in the same directory as this notebook (or somewhere else in your Python path) to hold `settings.CENSUS_KEY`.  (I prefer this approach over directly exposing your API key in the notebook code.)

# <codecell>

# This cell should run successfully if you have a string set up to represent your census key

try:
    import settings
    assert type(settings.CENSUS_KEY) == str or type(settings.CENSUS_KEY) == unicode
except Exception as e:
    print "error in importing settings to get at settings.CENSUS_KEY", e

# <headingcell level=1>

# us.states module

# <codecell>

# let's figure out a bit about the us module, in particular, us.states
# https://github.com/unitedstates/python-us

from us import states
assert states.CA.fips == u'06'

# <codecell>

# set up your census object
# example from https://github.com/sunlightlabs/census

from census import Census
from us import states

c = Census(settings.CENSUS_KEY)

# <codecell>

for (i, state) in enumerate(states.STATES):
    print i, state.name, state.fips

# <headingcell level=1>

# Formulating URL requests to the API explicitly

# <codecell>

import requests

# <codecell>

# get the total population of all states
url = "http://api.census.gov/data/2010/sf1?key={key}&get=P0010001,NAME&for=state:*".format(key=settings.CENSUS_KEY)

# <codecell>

r = requests.get(url)

# <headingcell level=1>

# EXERCISE

# <markdowncell>

# Show how to calculate the total population of the USA, including and excluding Puerto Rico.  (I don't know why Puerto Rico is included but not other [unincorporated territories](https://en.wikipedia.org/wiki/Unincorporated_territories_of_the_United_States)

# <codecell>

# FILL IN WITH YOUR CODE



# <headingcell level=1>

# Next Steps: Focusing on sf1 + census

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

c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})

# <codecell>

"population of California: {0}".format(
        int(c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})[0]['P0010001']))

