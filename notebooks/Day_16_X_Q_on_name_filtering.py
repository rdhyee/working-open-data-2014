# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [Topic: How can I filter a dataframe based on comparison against every item in another array?](https://bcourses.berkeley.edu/courses/1189091/discussion_topics/3031283)
# 
# > I have the basic names dataframe.
# 
# > I want to filter it based on whether or not the 'names' column in each row starts with any of the items in another array.
# 
# > How would I go about this? I'm trying something like this but it's sending the whole series of names into my is_in_prefixes function which seems to defeat the purpose of the lambda function, maybe I don't get what those are supposed to be used for
# 
# > target_names = names.apply(lambda x: is_in_prefixes(x.name))

# <codecell>

from pandas import DataFrame

# <codecell>

# make a test DataFrame

composers = DataFrame([{'name': 'Bach', 'date of birth':1685 },
                       {'name': 'Hildegard of Bingen', 'date of birth':1098},
                       {'name': 'Mozart', 'date of birth':1756},
                       {'name': 'Beethoven', 'date of birth':1770},
                       {'name': 'Shaw', 'date of birth': 1982}],
                      columns=['name', 'date of birth'])

# make a list with desired prefixes
desired_prefixes = ['Ba', 'S', "Mo"]

composers.name

# <codecell>

# one solution with regular expressions

import re

# use of alternation: http://docs.python.org/2/howto/regex.html
# make a regexp out of list of desired prefixes

desire_prefix_regexp = "^"+ "|".join(desired_prefixes)
print desire_prefix_regexp


composers[composers.name.apply(lambda s: re.search(desire_prefix_regexp, s) is not None)]

# <codecell>


