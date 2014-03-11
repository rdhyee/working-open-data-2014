# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Midterm
# 
# The upcoming midterm: (Day 17, 2014-03-18). It will probably consist of mostly multiple choice questions.
# 
# *The goal of this notebook is to help students to prepare for the midterm* through providing highlights of what we've covered so far.

# <markdowncell>

# ## Suggestions about How to Prepare
# 
# * read through all the materials from the course so far and outline what you understand and don't.
# * focus on key concepts and those programming constructs that are repeated often.

# <markdowncell>

# # Open Data
# 
# [Working definition of open data](http://rdhyee.github.io/wwod14/day01.html#(19)
# 
# 
# From <http://en.wikipedia.org/w/index.php?title=Special:Cite&page=Open_data&id=532390265>:
# 
# > Open data is the idea that certain data should be freely available to everyone
# to use and republish as they wish, without restrictions from copyright, patents
# or other mechanisms of control.
# 
# <http://opendefinition.org/>:
# 
# > A piece of content or data is open if anyone is free to use, reuse, and
# redistribute it — subject only, at most, to the requirement to attribute and/or
# share-alike.

# <markdowncell>

# ## Examples of Open Data
# 
# [Day 1: OKFestival /OKCon as indicator of vibrancy of the international open data community](http://rdhyee.github.io/wwod14/day01.html#(20%29)
# 
# [Day 1: Examples of Open Data](http://rdhyee.github.io/wwod14/day01.html#(31%29)

# <markdowncell>

# ## [Readings from Day 1](http://rdhyee.github.io/wwod14/day01.html#%2825%29)
# 
#    * read  [Python for Data Analysis Chap 1. Preliminaries : Safari Books Online](http://my.safaribooksonline.com/book/programming/python/9781449323592/1dot-preliminaries/id2664030) The instructions for using
#      Enthought Python Distribution are out of date.  If you are
#      looking for a distribution, follow  [the installation
#      instructions for Anaconda](https://github.com/rdhyee/working-open-data-2014/wiki/IPython-Installation-Options#2-anaconda)  for your computer platform.
#    * read `PfDA`, Chap 3 [Python for Data Analysis > 3. IPython: An Interactive Computing and Development Environment](http://my.safaribooksonline.com/book/programming/python/9781449323592/3dot-ipython-an-interactive-computing-and-development-environment/id2545624)
#    * skim `PfDA`, [Appendix: Python Language Essentials](http://my.safaribooksonline.com/book/programming/python/9781449323592/adot-python-language-essentials/id2819503) -- to help remind yourself of key elements of standard Python 
#    * skim `PfDA`, Chap 2 Introductory Examples

# <markdowncell>

# # World Populations
# 
# [Day_01_B_World_Population.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_01_B_World_Population.ipynb)
# 
# * How was the JSON data from the Wikipeida and the CIA Factbook produced?
# * Why do the totals from the two sources differ?

# <markdowncell>

# # Racial Dot Map (as a framing example)
# 
# [The Racial Dot Map: One Dot Per Person | Weldon Cooper Center for Public Service](http://www.coopercenter.org/demographics/Racial-Dot-Map)
# 
# 
# * What is the Racial Dot Map displaying?
# * How would you get data relevant to the Racial Dot Map from the Census API?

# <headingcell level=1>

# Census API

# <markdowncell>

# [Day_02_A_US_Census_API.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_02_A_US_Census_API.ipynb)
# 
# * What's the purpose of an API key?
# * What is `pip` and how to use it?
# * Remember the issues of sometimes having to filter to Puerto Rico

# <codecell>

# set up your census object
# example from https://github.com/sunlightlabs/census

from census import Census
from us import states

import settings

c = Census(settings.CENSUS_KEY)
for (i, state) in enumerate(states.STATES):
    print i, state.name, state.fips

# <markdowncell>

# [Formulating-URL-requests-to-the-API-explicitly](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_02_A_US_Census_API.ipynb#Formulating-URL-requests-to-the-API-explicitly)

# <codecell>

import requests
# get the total population of all states
url = "http://api.census.gov/data/2010/sf1?key={key}&get=P0010001,NAME&for=state:*".format(key=settings.CENSUS_KEY)
r = requests.get(url)

r.json()[:5]

# <markdowncell>

# [#Total-Population-of-California](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_02_A_US_Census_API.ipynb#Total-Population-of-California)

# <codecell>

c.sf1.get(('NAME', 'P0010001'), {'for': 'state:%s' % states.CA.fips})

# <markdowncell>

# # Execution environments for programs
# 
# [Day 3: Key Concept for Today: Execution Environment of Python](http://rdhyee.github.io/wwod14/day03.html#(13%29)
# 
# [Day 3: How I use conda](http://rdhyee.github.io/wwod14/day03.html#(17%29)

# <headingcell level=1>

# Learning the Basics of NumPy and Pandas

# <markdowncell>

#    * read  [Python for Data Analysis Chap 1. Preliminaries : Safari Books Online](http://my.safaribooksonline.com/book/programming/python/9781449323592/1dot-preliminaries/id2664030) The instructions for using
#      Enthought Python Distribution are out of date.  If you are
#      looking for a distribution, follow  [the installation
#      instructions for Anaconda](https://github.com/rdhyee/working-open-data-2014/wiki/IPython-Installation-Options#2-anaconda)  for your computer platform.
#    * skim `PfDA`, [Appendix: Python Language Essentials](http://my.safaribooksonline.com/book/programming/python/9781449323592/adot-python-language-essentials/id2819503) -- to help remind yourself of key elements of standard Python 
#    * read `PfDA`, Chap 3 [Python for Data Analysis > 3. IPython: An Interactive Computing and Development Environment](http://my.safaribooksonline.com/book/programming/python/9781449323592/3dot-ipython-an-interactive-computing-and-development-environment/id2545624)
#    * read `PfDA`, Chap 2 Introductory Examples

# <markdowncell>

#    
# [Day 4](http://rdhyee.github.io/wwod14/day04.html#(7%29): Work through [Day_04_B_numpy_and_pandas_series.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_04_B_numpy_and_pandas_series.ipynb) (everything before [Advanced: Operator Overloading](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_04_B_numpy_and_pandas_series.ipynb#Advanced:-Operator-Overloading))

# <markdowncell>

# # Census API skills
# 
# You should be able to [calculate the total population of the US](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_04_C_Census.ipynb#Total-Population) in the fill-in section of  [Day_04_C_Census.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_04_C_Census.ipynb).
# 
# You should be able to [calculate the population of California by totaling the county populations](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_04_C_Census.ipynb#Total-Population-of-California). 
# 
# For [Day 5: Geographical Hierarchies in the Census](http://rdhyee.github.io/wwod14/day05.html#(1%29), study:
# 
# * [Day_05_A_Geographical_Hierarchies.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_05_A_Geographical_Hierarchies.ipynb) 
# * and answers ([Day_05_B_Geographical_Hierarchies.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_05_B_Geographical_Hierarchies.ipynb) 
# 
# 
# [Day_06_C_Calculating_Diversity_Preview.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_06_C_Calculating_Diversity_Preview.ipynb) and 
# [Day_06_D_Assignment](https://bcourses.berkeley.edu/courses/1189091/assignments/4634716)

# <markdowncell>

# # Generators 
# 
# generators  [Day 6: Generators for Geographic Entities](http://rdhyee.github.io/wwod14/day06.html)

# <markdowncell>

# [Day_06_D_Assignment.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_06_D_Assignment.ipynb):  exercise to write a generator for Census Places (answer: [Day_06_E_Assignment_Answers.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_06_E_Assignment_Answers.ipynb))

# <codecell>

# You should understand how this works.

import pandas as pd
from pandas import DataFrame

import census
import settings
import us

from itertools import islice

c=census.Census(settings.CENSUS_KEY)

def places(variables="NAME"):
    
    for state in us.states.STATES:
        print state
        geo = {'for':'place:*', 'in':'state:{s_fips}'.format(s_fips=state.fips)}
        for place in c.sf1.get(variables, geo=geo):
            yield place

r = list(islice(places("NAME,P0010001"), None))
places_df = DataFrame(r)
places_df.P0010001 = places_df.P0010001.astype('int')

places_df['FIPS'] = places_df.apply(lambda s: s['state']+s['place'], axis=1)

print "number of places", len(places_df)
print "total pop", places_df.P0010001.sum()
places_df.head()

assert places_df.P0010001.sum() == 228457238
# number of places in 2010 Census
assert len(places_df) == 29261

# <markdowncell>

# # Apply and lambda functions
# 
# apply + lambda functions: [Day_06_A_Apply_Lambda.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_06_A_Apply_Lambda.ipynb)

# <markdowncell>

# # P005* variables in the census
# 
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

# <markdowncell>

# # Some graphics demonstrations you should try
# 
# [Day 7: Preview of Plotting Graphs and Maps](http://rdhyee.github.io/wwod14/day07.html#(3%29)
# 
# Do the following notebooks work for you to show basic graphics.
# 
# * [Day_07_A_D3_Choropleth.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_A_D3_Choropleth.ipynb)
# 
# * [Day_07_B_Google_Chart_Example.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_B_Google_Chart_Example.ipynb)
# 
# * [Day_07_C_Google_Map_API.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_C_Google_Map_API.ipynb)
# 
# * [Day_07_D_Matplotlib.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_D_Matplotlib.ipynb)
# 
# * [Day_13_D_Vincent_Examples.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_D_Vincent_Examples.ipynb)

# <markdowncell>

# # Census has lots of interesting data (optional)
# 
# [Day_07_E_Census_fields.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_E_Census_fields.ipynb)
# is an exploration of the concepts and variables in the 2010 Census.

# <markdowncell>

# # Groupby
# 
# [Day_07_F_Groupby.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_F_Groupby.ipynb):  gives you backgruond on how to understand and use `groupby` in Pandas.  Don't miss AJ's [Day_10_Groupby_Examples.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_10_Groupby_Examples.ipynb), which should be helpful, especially if you found [Day_10_Groupby_Examples.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_10_Groupby_Examples.ipynb) obscure.

# <markdowncell>

# # Census Metro Diversity Exercise
# 
# [Day_07_G_Calculating_Diversity.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_G_Calculating_Diversity.ipynb):  a prelude to the big diversity-calculation assignment [Day_08_A_Metro_Diversity.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_08_A_Metro_Diversity.ipynb)

# <markdowncell>

# # Projects
# 
#  not a focal point for the midterm (though, of course, it's good for projects to be in the background of your thinking)
# 
# Relevant references:
# 
# * [Day 9: Creating Projects](http://rdhyee.github.io/wwod14/day09.html)
# * [Day 9: Creating Projects: Project Topic Ideas](http://rdhyee.github.io/wwod14/day09.html#(5%29)
# * [Project-Starter_OpenContext.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Project-Starter_OpenContext.ipynb)
# * [Day 11: Project Brainstorming](http://rdhyee.github.io/wwod14/day11.html#(6%29)

# <markdowncell>

# # Plotting and Mapping preparation
# 
# I will assume that you've read Chapter 8 of `PfDA` and can run [Day_11_B_Setting_Up_for_PfDA.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_11_B_Setting_Up_for_PfDA.ipynb).
# 
# study overview slide: [Day 12: Overview of Plotting Options](http://rdhyee.github.io/wwod14/day12.html#(3%29).
# 
# Note some fundamental conceptual aspects to `matplotlib` (as I outline in  [Day_12_A_Matplotlib_Intro.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_12_A_Matplotlib_Intro.ipynb)
# and try to make basic plots on your own (line plots, scatter plots, bar plots).

# <markdowncell>

# # Baby Names
# 
# [Day_12_B_Baby_Names_Starter.ipynb#Names-that-are-both-M-and-F](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_12_B_Baby_Names_Starter.ipynb#Names-that-are-both-M-and-F)
# 
# Before you use [Day_13_C_Baby_Names_MF_Completed.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_C_Baby_Names_MF_Completed.ipynb),
# try the approach in [Day_13_B_Baby_Names_MF_Starter.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb)
# 
# Assignment in [nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb):
# 
# > Submit a notebook that describes what you've learned about the nature of
# ambigendered names in the baby names database. (Due date: <s>Monday, March 10</s> Wed, March 12 at
# 11:5pm --> bCourses assignment) I'm interested in seeing what you do
# with the data set in this regard. At the minimum, show that you are able to run
# Day_13_C_Baby_Names_MF_Completed. Be creative and have fun.

# <markdowncell>

# # mpld3
# 
# [Day 13: mpld3 references](http://rdhyee.github.io/wwod14/day13.html#(5%29)
# 
# [Day_13_A_mpl3d.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_A_mpl3d.ipynb)

# <markdowncell>

# # pivot_table
# 
# [Day_14_A_Pivot_table_example.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_14_A_Pivot_table_example.ipynb)

# <codecell>


