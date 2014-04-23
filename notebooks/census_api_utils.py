# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 06:38:41 2014

@author: raymondyee
"""

import numpy as np
import pandas as pd
from pandas import Series


import census
import us

import settings

c = census.Census(key=settings.CENSUS_KEY)

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


def msas(variables="NAME"):
    
     for state in us.STATES:
        geo = {'for':'metropolitan statistical area/micropolitan statistical area:*', 
               'in':'state:{state_fips}'.format(state_fips=state.fips)
               }
    
        for msa in c.sf1.get(variables, geo=geo):
            yield msa
            
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
            
            

def census_labels(prefix='P005', n0=1, n1=17, field_width=4, include_name=True, join=False):
    """convenience function to generate census labels"""
    
    label_format = "{i:0%dd}" % (field_width)
    
    variables = [prefix + label_format.format(i=i) for i in xrange(n0,n1+1)]
    if include_name:
        variables = ['NAME'] + variables

    if join:
        return ",".join(variables)
    else:
        return variables

def rdot_labels(other=True):
    if other:
        return ['White', 'Black', 'Asian', 'Hispanic', 'Other']
    else:
        return ['White', 'Black', 'Asian', 'Hispanic']
    
FINAL_LABELS = ['NAME', 'Total'] + rdot_labels() + ['p_White', 'p_Black', 'p_Asian', 'p_Hispanic', 'p_Other'] + ['entropy5', 'entropy4', 'entropy_rice', 'gini_simpson']
    
def convert_to_rdotmap(row):
    """takes the P005 variables and maps to a series with White, Black, Asian, Hispanic, Other
    Total"""
    return pd.Series({'Total':row['P0050001'],
                      'White':row['P0050003'],
                      'Black':row['P0050004'],
                      'Asian':row['P0050006'],
                      'Hispanic':row['P0050010'],
                      'Other': row['P0050005'] + row['P0050007'] + row['P0050008'] + row['P0050009'],
                      }, index=['Total', 'White', 'Black', 'Hispanic', 'Asian', 'Other'])


def normalize(s):
    """take a Series and divide each item by the sum so that the new series adds up to 1.0"""
    total = np.sum(s)
    return s.astype('float') / total
    
def normalize_relabel(s):
    """take a Series and divide each item by the sum so that the new series adds up to 1.0
    Also relabel the indices by adding p_ prefix"""
    total = np.sum(s)
    new_index = list(Series(s.index).apply(lambda x: "p_"+x))
    return Series(list(s.astype('float') / total),new_index)

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

def entropy_rice(series):
    """hard code how Rice U did calculation """
    # pass in a Series with 
    # 'Asian','Black','Hispanic','White','Other'
    # http://kinder.rice.edu/uploadedFiles/Urban_Research_Center/Media/Houston%20Region%20Grows%20More%20Ethnically%20Diverse%202-13.pdf

    s0 = normalize(series)
    s_other = s0['Other']*np.log(s0['Other']) if s0['Other'] > 0 else 0.0
    return (np.log(0.2)*entropy(series) - s_other)/np.log(0.25)

def diversity(df):
    """Takes a df with the P005 variables and does entropy calculation"""
    # convert populations to int
    df[census_labels(include_name=False)] = df[census_labels(include_name=False)].astype('int')
    df = pd.concat((df, df.apply(convert_to_rdotmap, axis=1)),axis=1)
    df = pd.concat((df,df[rdot_labels()].apply(normalize_relabel,axis=1)), axis=1)
    df['entropy5'] = df.apply(lambda x:entropy(x[rdot_labels()]), axis=1)
    df['entropy4'] = df.apply(lambda x:entropy(x[rdot_labels(other=False)]), axis=1)
    df['entropy_rice'] = df.apply(lambda x:entropy_rice(x[rdot_labels()]), axis=1)
    df['gini_simpson'] = df.apply(lambda x:gini_simpson(x[rdot_labels()]), axis=1)
    return df
    

 