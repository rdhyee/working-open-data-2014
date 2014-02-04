# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# our usual pylab import
%pylab --no-import-all inline

# <headingcell level=1>

# Goal

# <markdowncell>

# For background, see [Mapping Census Data](http://www.udel.edu/johnmack/frec682/census/), including the 
# [scan of the 10-question form](http://www.udel.edu/johnmack/frec682/census/census_form.png).  Keep in mind what people were asked and the range of data available in the census.
# 
# Using the census API to get an understanding of some of the geographic entities in the **2010 census**.  We'll specifically be using the variable `P0010001`, the total population.  
# 
# What you will do in this notebook:
# 
#  * Sum the population of the **states** (or state-like entity like DC) to get the total population of the **nation**
#  * Add up the **counties** for each **state** and validate the sums
#  * Add up the **census tracts** for each **county** and validate the sums
#  
# We will make use of `pandas` in this notebook.

# <markdowncell>

# I often have the following [diagram](http://www.census.gov/geo/reference/pdfs/geodiagram.pdf) in mind to help understand the relationship among entities.  Also use the [list of example URLs](http://api.census.gov/data/2010/sf1/geo.html)  -- it'll come in handy.

# <markdowncell>

# <a href="http://www.flickr.com/photos/raymondyee/12297467734/" title="Census Geographic Hierarchies by Raymond Yee, on Flickr"><img src="http://farm4.staticflickr.com/3702/12297467734_af8882d310_c.jpg" width="618" height="800" alt="Census Geographic Hierarchies"></a>

# <headingcell level=1>

# Working out the geographical hierarchy for Cafe Milano

# <markdowncell>

# It's helpful to have a concrete instance of a place to work with, especially when dealing with rather intangible entities like census tracts, block groups, and blocks.  You can use the [American FactFinder](http://factfinder2.census.gov/faces/nav/jsf/pages/index.xhtml) site to look up for any given US address the corresponding census geographies.  
# 
# Let's use Cafe Milano in Berkeley as an example. You can verify the following results by typing in the address into http://factfinder2.census.gov/faces/nav/jsf/pages/searchresults.xhtml?refresh=t.  
# 
# https://www.evernote.com/shard/s1/sh/dc0bfb96-4965-4fbf-bc28-c9d4d0080782/2bd8c92a045d62521723347d62fa2b9d
# 
# 2522 Bancroft Way, BERKELEY, CA, 94704
# 
# * State: California
# * County: Alameda County
# * County Subdivision: Berkeley CCD, Alameda County, California
# * Census Tract: Census Tract 4228, Alameda County, California
# * Block Group: Block Group 1, Census Tract 4228, Alameda County, California
# * Block: Block 1001, Block Group 1, Census Tract 4228, Alameda County, California
# 

# <codecell>

# YouTube video I made on how to use the American Factfinder site to look up addresses
from IPython.display import YouTubeVideo
YouTubeVideo('HeXcliUx96Y')

# <codecell>

#  standard numpy, pandas, matplotlib imports

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd

# <codecell>

# check that CENSUS_KEY is defined
import census
import us

import requests

import settings
assert settings.CENSUS_KEY is not None

# <markdowncell>

# The census documentation has example URLs but needs your API key to work.  In this notebook, we'll use the IPython notebook HTML display mechanism to help out.

# <codecell>

c = census.Census(key=settings.CENSUS_KEY)

# <markdowncell>

# Note:  we can use `c.sf1` to access 2010 census (SF1: Census Summary File 1 (2010, 2000, 1990) available in API -- 2010 is the default)
# 
# see documentation: [sunlightlabs/census](https://github.com/sunlightlabs/census)

# <headingcell level=1>

# Summing up populations by state    

# <markdowncell>

# Let's make a `DataFrame` named `states_df` with columns `NAME`, `P0010001` (for population), and `state` (to hold the FIPS code).  **Make sure to exclude Puerto Rico.**

# <codecell>

# call the API and instantiate `df`
df = DataFrame(c.sf1.get('NAME,P0010001', geo={'for':'state:*'}))
# convert the population to integer
df['P0010001'] = df['P0010001'].astype(np.int)
df.head()

# <markdowncell>

# You can filter Puerto Rico (PR) in a number of ways -- use the way you're most comfortable with. 
# 
# Optional fun: filter PR in the following way
# 
# * calculate a `np.array` holding the the fips of the states
# * then use [numpy.in1d](http://docs.scipy.org/doc/numpy/reference/generated/numpy.in1d.html), which is a analogous to the [in](http://stackoverflow.com/a/3437130/7782) operator to test membership in a list

# <codecell>

states_fips = np.array([state.fips for state in us.states.STATES])
states_df = df[np.in1d(df.state,states_fips)]

# <markdowncell>

# If `states_df` is calculated properly, the following asserts will pass silently.

# <codecell>

# check that we have three columns
assert set(states_df.columns) == set((u'NAME', u'P0010001', u'state'))

# check that the total 2010 census population is correct
assert np.sum(states_df.P0010001) == 308745538 

# check that the number of states+DC is 51
assert len(states_df) == 51

# <headingcell level=1>

# Counties

# <markdowncell>

# Looking at http://api.census.gov/data/2010/sf1/geo.html, we see
# 
#     state-county: http://api.census.gov/data/2010/sf1?get=P0010001&for=county:*
#     
# if we want to grab all counties in one go, or you can grab counties state-by-state:
# 
#     http://api.census.gov/data/2010/sf1?get=P0010001&for=county:*&in=state:06
#     
# for all counties in the state with FIPS code `06` (which is what state?)

# <codecell>

# Here's a way to use translate 
# http://api.census.gov/data/2010/sf1?get=P0010001&for=county:*
# into a call using the census.Census object

r = c.sf1.get('NAME,P0010001', geo={'for':'county:*'})

# ask yourself what len(r) means and what it should be
len(r)

# <codecell>

# let's try out one of the `census` object convenience methods
# instead of using `c.sf1.get`

r = c.sf1.state_county('NAME,P0010001',census.ALL,census.ALL)
r

# <codecell>

# convert the json from the API into a DataFrame
# coerce to integer the P0010001 column

df = DataFrame(r)
df['P0010001'] = df['P0010001'].astype('int')

# display the first records
df.head()

# <codecell>

# calculate the total population 
# what happens when you google the number you get?

np.sum(df['P0010001'])

# <codecell>

# often you can use dot notation to access a DataFrame column
df.P0010001.head()

# <codecell>

# let's filter out PR -- what's the total population now
sum(df[np.in1d(df.state, states_fips)].P0010001)

# <codecell>

# fall back to non-Pandas solution if you need ton
np.sum([int(county['P0010001']) for county in r if county['state'] in states_fips])

# <codecell>

# construct counties_df with only 50 states + DC
counties_df = df[np.in1d(df.state, states_fips)]
len(counties_df)

# <codecell>

set(counties_df.columns) == set(df.columns)

# <markdowncell>

# Check properties of `counties_df`

# <codecell>

# number of counties
assert len(counties_df) == 3143 #3143 county/county-equivs in US

# <codecell>

# check that the total population by adding all counties == population by adding all states

assert np.sum(counties_df['P0010001']) == np.sum(states_df.P0010001)

# <codecell>

# check we have same columns between counties_df and df
set(counties_df.columns) == set(df.columns)

# <headingcell level=1>

# Using FIPS code as the Index

# <markdowncell>

# From [Mapping Census Data](http://www.udel.edu/johnmack/frec682/census/):
# 
# * Each state (SUMLEV = 040) has a 2-digit FIPS ID; Delaware's is 10.
# * Each county (SUMLEV = 050) within a state has a 3-digit FIPS ID, appended to the 2-digit state ID. New Castle County, Delaware, has FIPS ID 10003.
# * Each Census Tract (SUMLEV = 140) within a county has a 6-digit ID, appended to the county code. The Tract in New Castle County DE that contains most of the the UD campus has FIPS ID 10003014502.
# * Each Block Group (SUMLEV = 150) within a Tract has a single digit ID appended to the Tract ID. The center of campus in the northwest corner of the tract is Block Group100030145022.
# * Each Block (SUMLEV = 750) within a Block Group is identified by three more digits appended to the Block Group ID. Pearson Hall is located in Block 100030145022009.

# <codecell>

# take a look at the current structure of counties_df

counties_df.head()

# <codecell>

# reindex states_df by state FIPS
# http://pandas.pydata.org/pandas-docs/dev/generated/pandas.DataFrame.set_index.html

states_df.set_index(keys='state', inplace=True)
states_df.head()

# <codecell>

# display the result of using set_index
counties_df.head()

# <codecell>

# http://manishamde.github.io/blog/2013/03/07/pandas-and-python-top-10/#create

counties_df['FIPS'] = counties_df.apply(lambda s:s['state'] + s['county'], axis=1)
counties_df.set_index('FIPS', inplace=True)

# <codecell>

counties_df.head()

# <codecell>

counties_df.groupby('state').sum().head()

# <codecell>

states_df.P0010001.head()

# <codecell>

# now we're ready to compare for each state, if you add all the counties, do you get the same
# population?
# not that you can do .agg('sum') instead of .sum()
# look at http://pandas.pydata.org/pandas-docs/dev/groupby.html to learn more about agg

np.all(states_df.P0010001 == counties_df.groupby('state').agg('sum').P0010001)

# <headingcell level=1>

# Counties in California

# <markdowncell>

# Let's look at home: California state and Alameda County

# <codecell>

# boolean indexing to pull up California
states_df[states_df.NAME == 'California']

# <codecell>

# use .ix -- most general indexing 
# http://pandas.pydata.org/pandas-docs/dev/indexing.html#different-choices-for-indexing-loc-iloc-and-ix
states_df.ix['06']

# <codecell>

# California counties

counties_df[counties_df.state=='06']

# <codecell>

counties_df[counties_df.NAME == 'Alameda County']

# <codecell>

counties_df[counties_df.NAME == 'Alameda County']['P0010001']

# <markdowncell>

# Different ways to read off the population of Alameda County -- still looking for the best way

# <codecell>

counties_df[counties_df.NAME == 'Alameda County']['P0010001'].to_dict().values()[0]

# <codecell>

list(counties_df[counties_df.NAME == 'Alameda County']['P0010001'].iteritems())[0][1]

# <codecell>

int(counties_df[counties_df.NAME == 'Alameda County']['P0010001'].values)

# <markdowncell>

# If you know the FIPS code for Alameda County, just read off the population using `.ix`

# <codecell>

# this is like accessing a cell in a spreadsheet -- row, col

ALAMEDA_COUNTY_FIPS = '06001'

counties_df.ix[ALAMEDA_COUNTY_FIPS,'P0010001']

# <headingcell level=1>

# Reading off all the tracts in Alameda County

# <codecell>

counties_df.ix[ALAMEDA_COUNTY_FIPS,'county']

# <codecell>

# http://api.census.gov/data/2010/sf1/geo.html
# state-county-tract

geo = {'for': 'tract:*', 
       'in': 'state:%s county:%s' % (us.states.CA.fips, 
                                     counties_df.ix[ALAMEDA_COUNTY_FIPS,'county'])}
        
r = c.sf1.get('NAME,P0010001', geo=geo)

# <codecell>

alameda_county_tracts_df.apply(lambda s: s['state']+s['county']+s['tract'], axis=1)

# <codecell>

#use state_county_tract to make a DataFrame

alameda_county_tracts_df = DataFrame(r)
alameda_county_tracts_df['P0010001'] = alameda_county_tracts_df['P0010001'].astype('int')
alameda_county_tracts_df['FIPS'] = alameda_county_tracts_df.apply(lambda s: s['state']+s['county']+s['tract'], axis=1)
alameda_county_tracts_df.head()

# <codecell>

alameda_county_tracts_df.P0010001.sum()

# <codecell>

# Cafe Milano is in tract 4228
MILANO_TRACT_ID = '422800'
alameda_county_tracts_df[alameda_county_tracts_df.tract==MILANO_TRACT_ID]

# <headingcell level=1>

# Using Generators to yield all the tracts in the country

# <markdowncell>

# http://www.jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/

# <codecell>

import time
import us

from itertools import islice

def census_tracts(variable=('NAME','P0010001'), sleep_time=1.0):
    
    for state in us.states.STATES:
        print state
        for tract in c.sf1.get(variable, 
                    geo={'for':"tract:*", 
                        'in':'state:{state_fips}'.format(state_fips=state.fips)
                        }):
            yield tract
        # don't hit the API more than once a second    
        time.sleep(sleep_time)
 
# limit the number of tracts we crawl for until we're reading to get all of them        
tracts_df = DataFrame(list(islice(census_tracts(), 100)))
tracts_df['P0010001'] = tracts_df['P0010001'].astype('int')

# <codecell>

tracts_df.head()

# <headingcell level=1>

# Compare with Tabulations

# <markdowncell>

# We can compare the total number of tracts we calculate to:
# 
# https://www.census.gov/geo/maps-data/data/tallies/tractblock.html
# 
# and
# 
# https://www.census.gov/geo/maps-data/data/docs/geo_tallies/Tract_Block2010.txt

