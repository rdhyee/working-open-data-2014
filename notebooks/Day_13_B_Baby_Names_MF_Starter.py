# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# The focus of this notebook is on baby names that have been given to both male and female. 

# <codecell>

%matplotlib inline

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

from pylab import figure, show

from pandas import DataFrame, Series
import pandas as pd

# <codecell>

try:
    import mpld3
    from mpld3 import enable_notebook
    from mpld3 import plugins
    enable_notebook()
except Exception as e:
    print "Attempt to import and enable mpld3 failed", e

# <codecell>

# what would seaborn do?
try:
    import seaborn as sns
except Exception as e:
    print "Attempt to import and enable seaborn failed", e

# <headingcell level=1>

# Preliminaries: Assumed location of pydata-book files

# <markdowncell>

# To make it more practical for me to look at your homework, I'm again going to assume a relative placement of files.  I placed the files from 
# 
# https://github.com/pydata/pydata-book
# 
# in a local directory, which in my case is "/Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/" 
# 
# and then symbolically linked (`ln -s`) to the the pydata-book from the root directory of the working-open-data folder.  i.e., on OS X
# 
#     cd /Users/raymondyee/D/Document/Working_with_Open_Data/working-open-data
#     ln -s /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ pydata-book
# 
# That way the files from the pydata-book repository look like they sit in the working-open-data directory -- without having to actually copy the files.
# 
# With this arrangment, I should then be able to drop your notebook into my own notebooks directory and run them without having to mess around with paths.

# <codecell>

import os

NAMES_DIR = os.path.join(os.pardir, "pydata-book", "ch02", "names")

assert os.path.exists(NAMES_DIR)

# <markdowncell>

# **Please make sure the above assertion works.**

# <headingcell level=1>

# Baby names dataset

# <markdowncell>

# discussed in p. 35 of `PfDA` book

# <markdowncell>

# To download all the data, including that for 2011 and 2012: [Popular Baby Names](http://www.ssa.gov/OACT/babynames/limits.html) --> includes state by state data.

# <headingcell level=1>

# Loading all data into Pandas

# <codecell>

# show the first five files in the NAMES_DIR

import glob
glob.glob(NAMES_DIR + "/*")[:5]

# <codecell>

# 2010 is the last available year in the pydata-book repo
import os

years = range(1880, 2011)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = os.path.join(NAMES_DIR, 'yob%d.txt' % year)
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)

# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

# why floats?  I'm not sure.
names.describe()

# <codecell>

# how many people, names, males and females  represented in names?

names.births.sum()

# <codecell>

# F vs M

names.groupby('sex')['births'].sum()

# <codecell>

# total number of names

len(names.groupby('name'))

# <codecell>

# use pivot_table to collect records by year (rows) and sex (columns)

total_births = names.pivot_table('births', rows='year', cols='sex', aggfunc=sum)
total_births.head()

# <codecell>

# You can use groupy to get equivalent pivot_table calculation

names.groupby('year').apply(lambda s: s.groupby('sex').agg('sum')).unstack()['births']

# <codecell>

# how to calculate the total births / year

names.groupby('year').sum().plot(title="total births by year")

# <codecell>

names.groupby('year').apply(lambda s: s.groupby('sex').agg('sum')).unstack()['births'].plot(title="births (M/F) by year")

# <codecell>

# from book: add prop to names

def add_prop(group):
    # Integer division floors
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

# <codecell>

# verify prop --> all adds up to 1

np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

# <codecell>

# number of records in full names dataframe

len(names)

# <headingcell level=1>

# How to do top1000 calculation

# <markdowncell>

# This section on the top1000 calculation is kept in here to provide some inspiration on how to work with baby names

# <codecell>

#  from book: useful to work with top 1000 for each year/sex combo
# can use groupby/apply

names.groupby(['year', 'sex']).apply(lambda g: g.sort_index(by='births', ascending=False)[:1000])

# <codecell>

def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
top1000.head()

# <codecell>

# Do pivot table: row: year and cols= names for top 1000

top_births = top1000.pivot_table('births', rows='year', cols='name', aggfunc=np.sum)
top_births.tail()

# <codecell>

# is your name in the top_births list?

top_births['Raymond'].plot(title='plot for Raymond')

# <codecell>

# for Aaden, which shows up at the end

top_births.Aaden.plot(xlim=[1880,2010])

# <codecell>

# number of names represented in top_births

len(top_births.columns)

# <codecell>

# how to get the most popular name of all time in top_births?

most_common_names = top_births.sum()
most_common_names.sort(ascending=False)

most_common_names.head()

# <codecell>

# as of mpl v 0.1 (2014.03.04), the name labeling doesn't work -- so disble mpld3 for this figure

mpld3.disable_notebook()
plt.figure()
most_common_names[:50][::-1].plot(kind='barh', figsize=(10,10))

# <codecell>

# turn mpld3 back on

mpld3.enable_notebook()

# <headingcell level=1>

# all_births pivot table

# <codecell>

# instead of top_birth -- get all_births

all_births = names.pivot_table('births', rows='year', cols='name', aggfunc=sum)

# <codecell>

all_births = all_births.fillna(0)
all_births.tail()

# <codecell>

# set up to do start/end calculation

all_births_cumsum = all_births.apply(lambda s: s.cumsum(), axis=0)

# <codecell>

all_births_cumsum.tail()

# <headingcell level=2>

# Names that are both M and F

# <codecell>

# remind ourselves of what's in names

names.head()

# <codecell>

# columns in names

names.columns

# <headingcell level=1>

# Approach to exploring ambigendered names

# <markdowncell>

# Some things to think about:
# 
# * calculate a set of ambi_names -- names that are both M and F in the database: `names_ambi`
# * calculate a pivot table `ambi_names_pt` that use a hierarchical index name/sex vs years
# * for a specific name, make a plot of male vs female population to validate your approach
# * think of using cumulative vs year-by-year instantaneous populations
# * think about metrics for measuring the sex shift of names
# * think about how to calculate how ambigendered a name is

# <headingcell level=1>

# Exercise

# <markdowncell>

# Submit a notebook that describes what you've learned about the nature of ambigendered names in the baby names database.  (Due date: Monday, March 10 at 11:5pm --> bCourses assignment to come.)  I'm interested in seeing what you do with the data set in this regard.  At the minimum, show that you are able to run Day_13_C_Baby_Names_MF_Completed.  Be creative and have fun.  

# <codecell>


