# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# A simple demonstration of pivot_table. [Reshaping and Pivot Tables — pandas 0.13.1 documentation](http://pandas.pydata.org/pandas-docs/stable/reshaping.html)

# <codecell>

import pandas as pd
from pandas import DataFrame, Series

# <codecell>

df = DataFrame([{
'year':1880,
'name':'John',
'sex': 'M',
'births': 13
},
{'year':1880,
'name':'Pat',
'sex': 'M',
'births': 13
},
{'year':1880,
'name':'Pat',
'sex': 'F',
'births': 13
},
{
'year':1880,
'name':'Jane',
'sex': 'F',
'births': 20
}, 
{
'year':1881,
'name':'John',
'sex': 'M',
'births': 90
},
{
'year':1881,
'name':'Jane',
'sex': 'F',
'births': 21
},])

df

# <codecell>

pt  = df.pivot_table(rows='year', cols=['name','sex'])['births']
pt

# <codecell>

# let's make a new table in which there is M/F subindex for all names

names = set(pt.columns.get_level_values(level=0))
sexes = set(pt.columns.get_level_values(level=1))
names, sexes

# <codecell>

# http://pandas.pydata.org/pandas-docs/stable/indexing.html#creating-a-multiindex-hierarchical-index-object

new_index = pd.MultiIndex.from_product([list(names), list(sexes)],
                           names=['name','sex'])
new_index

# <codecell>

# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.reindex.html

pt.T.reindex(new_index).T

# <codecell>

pt.T.reindex(new_index).T.fillna(0)

