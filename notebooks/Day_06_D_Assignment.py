# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
from pandas import DataFrame

import census
import settings
import us

from itertools import islice

# instantiate the census object

c=census.Census(settings.CENSUS_KEY)

# <codecell>

## EXERCISE
## FILL in with your generator for all census places in the 2010 census 


def places(variables="NAME"):
    
    # placeholder generator
    # replace with your own code
    for k in []:
        yield k
    


    
    
    
    

# <codecell>

# use this code to run your code
# I recommend replacing the None in islice to a small number to make sure you're on 
# the right track

r = list(islice(places("NAME,P0010001"), None))
places_df = DataFrame(r)
places_df.P0010001 = places_df.P0010001.astype('int')

places_df['FIPS'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)

print "number of places", len(places_df)
print "total pop", places_df.P0010001.sum()
places_df.head()

# <codecell>

# if you've done this correctly, the following asserts should stop complaining

assert places_df.P0010001.sum() == 228457238
# number of places in 2010 Census
assert len(places_df) == 29261

