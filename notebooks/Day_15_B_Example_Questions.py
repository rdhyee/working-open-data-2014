# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# **Work in Progress**

# <codecell>

# read population in
import json
import requests
from pandas import DataFrame

# pop_json_url holds a 
pop_json_url = "https://gist.github.com/rdhyee/8511607/raw/f16257434352916574473e63612fcea55a0c1b1c/population_of_countries.json"
pop_list= requests.get(pop_json_url).json()

df = DataFrame(pop_list)
df[:5]

# <markdowncell>

# Q: What is the relationship between `s` and the population of China?
# 
#     s = sum(df[df[1].str.startswith('C')][2])
#     
# 1. `s` is **greater** than the population of China
# 1. `s` is the **same** as the population of China
# 1. `s` is **less** than the population of China
# 1. `s` is not a number.
# 

# <codecell>

from pandas import DataFrame, Series, Index
import numpy as np

s1 = Series(np.arange(1,4))
s1

# <markdowncell>

# Q:  What is
#     
#     s1.apply(lambda k: 2*k).sum()
#    

# <markdowncell>

# Q: What is `s1.cumsum()[1]`?

# <codecell>


