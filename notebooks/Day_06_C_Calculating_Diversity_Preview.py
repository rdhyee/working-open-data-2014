# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab --no-import-all inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd

# <codecell>

import census
import us

import settings

# <markdowncell>

# The census documentation has example URLs but needs your API key to work.  In this notebook, we'll use the IPython notebook HTML display mechanism to help out.

# <codecell>

c = census.Census(key=settings.CENSUS_KEY)

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
# "Whites are coded as blue; African-Americans, green; Asians, red; Hispanics, orange; and all other racial categories are coded as brown."

# <headingcell level=1>

# Planned for next week

# <markdowncell>

# We will be calculating for each of the following geographic entities:
# 
#   * states
#   * counties
#   * places
#   * metropolitan areas
#   * combined statistical areas
# 
# these quantities:
# 
#   * the total number of Hispanics/Latinos vs non-Hispanics/Latinos
#   * numbers of people in the categories found in the [Racial Dot Map](http://bit.ly/rdotmap)
#   * the diversity index 
#   
# With any luck, we'll also plot quantities on maps too.

