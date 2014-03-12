# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [Piazza question](https://piazza.com/class/hqo4ux2fcns3ds?cid=7):
#     
# > Can column and row have the same index? Will it impact retrieval of data?
# 
# > Something on the lines-
#  
#     df = DataFrame([1,2,3,4],index=['a','b','c','d'],columns=['a'])
#  
# > In this case if we use df['a'], what value would be retrieved? I believe we don't specify while selection whether index is for a row or a column in the syntax.

# <markdowncell>

# Let's try it....

# <codecell>

from pandas import DataFrame

df = DataFrame([1,2,3,4],index=['a','b','c','d'],columns=['a'])

# <codecell>

# column a
df['a']

# <codecell>

# index a
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#different-choices-for-indexing-loc-iloc-and-ix

df.ix['a']

# <codecell>

# index b

df.ix['b']

# <codecell>

# column b -- doesn't exist

df['b']

