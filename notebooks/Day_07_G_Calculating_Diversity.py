# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# * Learn about how to use the Census variables around Hispanic origin to calculate quantities around diversity (remembering the [Racial Dot Map](http://bit.ly/rdotmapintro) as our framing example)

# <codecell>

%pylab --no-import-all inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd

from itertools import islice

# <codecell>

import census
import us

import settings

# <markdowncell>

# The census documentation has example URLs but needs your API key to work.  In this notebook, we'll use the IPython notebook HTML display mechanism to help out.

# <codecell>

c = census.Census(key=settings.CENSUS_KEY)

# <codecell>

# generators for the various census geographic entities of interest

def states(variables='NAME'):
    geo={'for':'state:*'}
    states_fips = set([state.fips for state in us.states.STATES])
    # need to filter out non-states
    for r in c.sf1.get(variables, geo=geo):
        if r['state'] in states_fips:
            yield r
            
def counties(variables='NAME'):
    """ask for all the states in one call"""
    
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

            
def tracts(variables='NAME'):
    for state in us.states.STATES:
        
        # handy to print out state to monitor progress
        # print state.fips, state
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

def block_groups(variables='NAME'):
    # http://api.census.gov/data/2010/sf1?get=P0010001&for=block+group:*&in=state:02+county:170
    # let's use the county generator
    for county in counties(variables):
        geo = {'for':'block group:*',
               'in':'state:{state} county:{county}'.format(state=county['state'],
                                                county=county['county'])
               }
        for block_group in c.sf1.get(variables, geo):
            yield block_group
    
    
def blocks(variables='NAME'):
    # http://api.census.gov/data/2010/sf1?get=P0010001&for=block:*&in=state:02+county:290+tract:00100
    
    # make use of the tract generator
    for tract in tracts(variables):
        geo={'for':'block:*',
             'in':'state:{state} county:{county} tract:{tract}'.format(state=tract['state'],
                                                                       county=tract['county'],
                                                                       tract=tract['tract'])
             }
        for block in c.sf1.get(variables, geo):
            yield block
        
       

# <codecell>

# msa, csas, districts, zip_codes

def msas(variables="NAME"):
    
     for state in us.STATES:
        geo = {'for':'metropolitan statistical area/micropolitan statistical area:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for msa in c.sf1.get(variables, geo=geo):
            yield msa

def csas(variables="NAME"):
    # http://api.census.gov/data/2010/sf1?get=P0010001&for=combined+statistical+area:*&in=state:24
    for state in us.STATES:
        geo = {'for':'combined statistical area:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for csa in c.sf1.get(variables, geo=geo):
            yield csa

def districts(variables="NAME"):
    # http://api.census.gov/data/2010/sf1?get=P0010001&for=congressional+district:*&in=state:24
    for state in us.STATES:
        geo = {'for':'congressional district:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for district in c.sf1.get(variables, geo=geo):
            yield district    
            
def zip_code_tabulation_areas(variables="NAME"):
    # http://api.census.gov/data/2010/sf1?get=P0010001&for=zip+code+tabulation+area:*&in=state:02
    for state in us.STATES:
        geo = {'for':'zip code tabulation area:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for zip_code_tabulation_area in c.sf1.get(variables, geo=geo):
            yield zip_code_tabulation_area    

# <codecell>

list(islice(msas(), 1))

# <codecell>

list(islice(csas(), 1))

# <codecell>

districts_list = list(islice(districts(), 1))
districts_list

# <codecell>

list(islice(zip_code_tabulation_areas(), 1))

# <markdowncell>

# **Note**: There are definitely improvements to be made in these generators.  One of the most important would be to limit the generators to specific geographies -- typically, we don't want to have all the blocks in the country but the ones in a specific area.  A good exercise to rewrite our generators to allow for limited geography.

# <markdowncell>

# We can compare the total number of tracts we calculate to:
# 
# https://www.census.gov/geo/maps-data/data/tallies/tractblock.html
# 
# and
# 
# https://www.census.gov/geo/maps-data/data/docs/geo_tallies/Tract_Block2010.txt

# <headingcell level=1>

# Hispanic or Latino Origin and Racial Subcategories

# <markdowncell>

# http://www.census.gov/developers/data/sf1.xml
# 
# compare to http://www.census.gov/prod/cen2010/briefs/c2010br-02.pdf 
# 
# I think the P0050001 might be the key category
# 
# * P0010001 = P0050001
# * P0050001 = P0050002 + P0050010
# 
# P0050002 Not Hispanic or Latino (total) = 
# 
# * P0050003 Not Hispanic White only 
# * P0050004 Not Hispanic Black only
# * P0050006 Not Hispanic Asian only
# * Not Hispanic Other (should also be P0050002 - (P0050003 + P0050004 + P0050006)
#      * P0050005 Not Hispanic: American Indian/ American Indian and Alaska Native alone
#      * P0050007 Not Hispanic: Native Hawaiian and Other Pacific Islander alone
#      * P0050008 Not Hispanic: Some Other Race alone
#      * P0050009 Not Hispanic: Two or More Races
# 
# * P0050010 Hispanic or Latino
#   
# P0050010 = P0050011...P0050017
# 
# From [Hispanic and Latino Americans (Wikipedia)](https://en.wikipedia.org/w/index.php?title=Hispanic_and_Latino_Americans&oldid=595018646):  
# 
# <blockquote>While the two terms are sometimes used interchangeably, Hispanic is a narrower term which mostly refers to persons of Spanish speaking origin or ancestry, while Latino is more frequently used to refer more generally to anyone of Latin American origin or ancestry, including Brazilians.</blockquote>
# 
# and
# 
# <blockquote>The Census Bureau's 2010 census does provide a definition of the terms Latino or Hispanic and is as follows: “Hispanic or Latino” refers to a person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race. It allows respondents to self-define whether they were Latino or Hispanic and then identify their specific country or place of origin.[52] On its website, the Census Bureau defines "Hispanic" or "Latino" persons as being "persons who trace their origin [to]... Spanish speaking Central and South America countries, and other Spanish cultures".</blockquote>
# 
# In the [Racial Dot Map](http://bit.ly/rdotmap): "Whites are coded as blue; African-Americans, green; Asians, red; Hispanics, orange; and all other racial categories are coded as brown."  
# 
# In this notebook, we will relate the Racial Dot Map 5-category scheme to the P005\* variables.

# <codecell>

# let's get the total population -- tabulated in two variables: P0010001, P0050001
# P0050002 Not Hispanic or Latino (total) 
# P0050010 Hispanic or Latino

r = list(states(('NAME','P0010001','P0050001','P0050002','P0050010')))
r[:5]

# <codecell>

# Hispanic/Latino origin vs not-Hispanic/Latino
# Compare with http://www.census.gov/prod/cen2010/briefs/c2010br-02.pdf Table 1
# Hispanic/Latino: 50477594
# non-Hispanic/Latino: 258267944

df=DataFrame(r)
df[['P0010001', 'P0050001','P0050002','P0050010']] = \
    df[['P0010001', 'P0050001','P0050002','P0050010']].astype('int')
df[['P0010001', 'P0050001', 'P0050002', 'P0050010']].sum()

# <codecell>

# is the total Hispanic/Latino population and non-Hispanic populations the same as reported in 
# http://www.census.gov/prod/cen2010/briefs/c2010br-02.pdf Table 1
(df['P0050010'].sum() == 50477594,
 df['P0050002'].sum() == 258267944)

# <codecell>

# How about the non-Hispanic/Latino White only category?
# P0050003
# total should be 196817552

df = DataFrame(list(states('NAME,P0050003')))
df['P0050003'] = df['P0050003'].astype('int')
df.P0050003.sum()

# <headingcell level=1>

# Converting to Racial Dot Map Categories

# <markdowncell>

# SUGGESTED EXERCISE:  write a function `convert_to_rdotmap(row)` tha takes an input Python dict that has the keys:
#     * NAME
#     * P005001, P005002...,P0050016, P0050017 
#     
# and that returns a Pandas Series with the following columns:
# 
#     * Total
#     * White
#     * Black
#     * Asian
#     * Hispanic
#     * Other
#     * Name  (note lowercase)
#     
# that correspond to those used in the Racial Dot Map.
# 
# Also write a function def convert_P005_to_int(df) that converts all the P005\* columns to `int`

# <codecell>

# USE a little convience function to calculate the variable names to be used

def P005_range(n0,n1): 
    return tuple(('P005'+ "{i:04d}".format(i=i) for i in xrange(n0,n1)))

P005_vars = P005_range(1,18)
P005_vars_str = ",".join(P005_vars)
P005_vars_with_name = ['NAME'] + list(P005_vars)

P005_vars_with_name

# <codecell>

# HAVE YOU TRIED THE EXERCISE....IF NOT....TRY IT....HERE'S ONE POSSIBLE ANSWER# 

# http://manishamde.github.io/blog/2013/03/07/pandas-and-python-top-10/#create

def convert_P005_to_int(df):
    # do conversion in place
    df[list(P005_vars)] = df[list(P005_vars)].astype('int')
    return df

def convert_to_rdotmap(row):
    """takes the P005 variables and maps to a series with White, Black, Asian, Hispanic, Other
    Total and Name"""
    return pd.Series({'Total':row['P0050001'],
                      'White':row['P0050003'],
                      'Black':row['P0050004'],
                      'Asian':row['P0050006'],
                      'Hispanic':row['P0050010'],
                      'Other': row['P0050005'] + row['P0050007'] + row['P0050008'] + row['P0050009'],
                      'Name': row['NAME']
                      }, index=['Name', 'Total', 'White', 'Black', 'Hispanic', 'Asian', 'Other'])

# <codecell>



from census import Census

import settings
from settings import CENSUS_KEY

import time
from itertools import islice

def P005_range(n0,n1): 
    return tuple(('P005'+ "{i:04d}".format(i=i) for i in xrange(n0,n1)))

P005_vars = P005_range(1,18)
P005_vars_str = ",".join(P005_vars)


# http://manishamde.github.io/blog/2013/03/07/pandas-and-python-top-10/#create
def convert_to_rdotmap(row):
    """takes the P005 variables and maps to a series with White, Black, Asian, Hispanic, Other
    Total and Name"""
    return pd.Series({'Total':row['P0050001'],
                      'White':row['P0050003'],
                      'Black':row['P0050004'],
                      'Asian':row['P0050006'],
                      'Hispanic':row['P0050010'],
                      'Other': row['P0050005'] + row['P0050007'] + row['P0050008'] + row['P0050009'],
                      'Name': row['NAME']
                      }, index=['Name', 'Total', 'White', 'Black', 'Hispanic', 'Asian', 'Other'])


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
    
    if len(series) > 1:
        # calculate the maximum possible entropy for given length of input series
        max_s = -np.log(1.0/len(series))
    
        total = float(sum(series1))
        p = series1.astype('float')/float(total)
        return sum(-p*np.log(p))/max_s
    else:
        return 0.0

    
def convert_P005_to_int(df):
    # do conversion in place
    df[list(P005_vars)] = df[list(P005_vars)].astype('int')
    return df
    

def diversity(r):

    """Returns a DataFrame with the following columns
    """
    df = DataFrame(r)
    df = convert_P005_to_int(df)
    # df[list(P005_vars)] = df[list(P005_vars)].astype('int')
    df1 = df.apply(convert_to_rdotmap, axis=1)
    
    df1['entropy5'] = df1[['Asian','Black','Hispanic','White','Other']].apply(entropy,axis=1)
    df1['entropy4'] = df1[['Asian','Black','Hispanic','White']].apply(entropy,axis=1)
    return df1

# <codecell>

# states

r=list(states(P005_vars_with_name))
diversity(r)

# <codecell>

# counties

r = list(counties(P005_vars_with_name))

# <codecell>

df2 = diversity(r)

# <codecell>

df2.sort_index(by='entropy5',ascending=False)

