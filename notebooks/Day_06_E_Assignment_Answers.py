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

def places(variables="NAME"):
    
    for state in us.states.STATES:
        print state
        geo = {'for':'place:*', 'in':'state:{s_fips}'.format(s_fips=state.fips)}
        for place in c.sf1.get(variables, geo=geo):
            yield place


# <codecell>

r = list(islice(places("NAME,P0010001"), None))
places_df = DataFrame(r)
places_df.P0010001 = places_df.P0010001.astype('int')

places_df['FIPS'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)

print "number of places", len(places_df)
print "total pop", places_df.P0010001.sum()
places_df.head()

# <codecell>

assert places_df.P0010001.sum() == 228457238
# number of places in 2010 Census
assert len(places_df) == 29261

# <codecell>


