# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# One student emailed with the following question:
# 
# <blockquote>
# <p>
# Right now I'm trying to edit the example entropy function to the one you wrote on the board in class. 
# </p>
# <p>
# My question is the example code only has one P_s, right? Our goal is to add four different values but I don't understand how to code P_w, P_h and so on. Would you give me more details and advice on this?
# </p>
# </blockquote>
#    
# As a hint, I will rewrite the `entropy` formula I wrote to explicitly look up the various categories.
#    

# <codecell>

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

# <codecell>

# supporint imports 

import numpy as np
from pandas import Series

# <codecell>

def entropy_term(p):
    """Individual Shannon entropy term -- handles the case in which p is 0"""
    if p == 0:
        return 0
    else:
        return -p*np.log(p)

def entropy5_explicit_labels(series):
    """entropy5 calculation for an input Series with 5 categories"""
    # calculate the normalizing term -- what's the maximum entropy
    # there are five categories here
    max_s = -np.log(1.0/5)
    total = float(series['White']+series['Black']+series['Asian']+ \
                  series['Hispanic']+series['Other'])
    
    s = entropy_term(series['White']/total) + \
        entropy_term(series['Black']/total) + \
        entropy_term(series['Asian']/total) + \
        entropy_term(series['Hispanic']/total) + \
        entropy_term(series['Other']/total)
    
    s = s/max_s
    return s

def entropy4_explicit_labels(series):
    """entropy4 calculation for an input Series with 4 categories"""
    # calculate the normalizing term -- what's the maximum entropy
    # there are five categories here
    max_s = -np.log(1.0/4)
    # don't include Other in the total
    total = float(series['White']+series['Black']+series['Asian']+ \
                  series['Hispanic'])
    
    s = entropy_term(series['White']/total) + \
        entropy_term(series['Black']/total) + \
        entropy_term(series['Asian']/total) + \
        entropy_term(series['Hispanic']/total) 
    
    s = s/max_s
    return s    

# <codecell>

# Using the population figures for the Houston Metro Area
# Make a pandas Series out of the dict

houston = Series({'Asian': 384596,
 'Black': 998883,
 'Hispanic': 2099412,
 'Other': 103437,
 'White': 2360472})

# <markdowncell>

# Note how the `entropy` function can be used to do both the entropy5 and entropy4 calculation
# by just changing the subset of the `houston` Series being passed into `entropy`

# <codecell>

# comparing two ways of doing the entropy5 calculation
(entropy(houston[['White', 'Black', 'Asian', 'Hispanic', 'Other']]),
 entropy5_explicit_labels(houston))

# <codecell>

# comparing two ways of doing the entropy4 calculation 
# don't include Other

(entropy(houston[['White', 'Black', 'Asian', 'Hispanic']]),
 entropy4_explicit_labels(houston))

# <markdowncell>

# Calculating a `entropy_rice` function is left to the reader....

# <codecell>


