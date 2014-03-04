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

# <headingcell level=2>

# Calculating ambigendered names

# <codecell>

# calculate set of male_only, female_only, ambigender names

def calc_of_sex_of_names():

    k = names.groupby('sex').apply(lambda s: set(list(s['name'])))
    male_only_names = k['M'] - k['F']
    female_only_names = k['F'] - k['M']
    ambi_names = k['F'] & k['M'] # intersection of two 
    return {'male_only_names': male_only_names, 
            'female_only_names': female_only_names,
            'ambi_names': ambi_names }
    
names_by_sex = calc_of_sex_of_names() 
ambi_names_array = np.array(list(names_by_sex['ambi_names']))

[(k, len(v)) for (k,v) in names_by_sex.items()]

# <codecell>

# total number of people in names
names.births.sum()

# <codecell>

# pivot table of ambigendered names to aggregate 

names_ambi = names[np.in1d(names.name,ambi_names_array)]
ambi_names_pt = names_ambi.pivot_table('births',
                            rows='year', 
                            cols=['name','sex'], 
                            aggfunc='sum')

# <codecell>

# total number of people in k1 -- almost everyone!

ambi_names_pt.sum().sum()

# <codecell>

# fill n/a with 0 and look at the table at the end

ambi_names_pt=ambi_names_pt.fillna(0L)
ambi_names_pt.tail()

# <codecell>

# plot M, F in ambigender_names over time
ambi_names_pt.T.xs('M',level='sex').sum().cumsum()

# <codecell>

ambi_names_pt.T.xs('F',level='sex').sum().cumsum()

# <codecell>

# don't know what pivot table has type float
# https://github.com/pydata/pandas/issues/3283
ambi_names_pt['Raymond', 'M'].dtype

# <codecell>

# calculate proportion of males for given name

def prop_male(name):
    return (ambi_names_pt[name]['M']/ \
    ((ambi_names_pt[name]['M'] + ambi_names_pt[name]['F'])))

def prop_c_male(name):
    return (ambi_names_pt[name]['M'].cumsum()/ \
    ((ambi_names_pt[name]['M'].cumsum() + ambi_names_pt[name]['F'].cumsum())))

# <codecell>

prop_c_male('Leslie').plot()

# <codecell>

# I couldn't figure out a way of iterating over the names rather than names/sex combo in
# a vectorized way.  

from itertools import islice

names_to_calc = list(islice(list(ambi_names_pt.T.index.levels[0]),None))

m = [(name_, ambi_names_pt[name_]['M']/(ambi_names_pt[name_]['F'] + ambi_names_pt[name_]['M']))  \
     for name_ in names_to_calc]
p_m_instant = DataFrame(dict(m))
p_m_instant.tail()

# <codecell>

# similar calculation except instead of looking at the proportions for a given year only,
# we look at the cumulative number of male/female babies for given name

from itertools import islice

names_to_calc = list(islice(list(ambi_names_pt.T.index.levels[0]),None))

m = [(name_, ambi_names_pt[name_]['M'].cumsum()/(ambi_names_pt[name_]['F'].cumsum() + ambi_names_pt[name_]['M'].cumsum()))  \
     for name_ in names_to_calc]
p_m_cum = DataFrame(dict(m))
p_m_cum.tail()

# <codecell>

p_m_cum['Donnie'].plot()

# <codecell>

# some metrics that attempt to measure how a time series s has changed

def min_max_range(s):
    """range of s signed -- positive if slope between two points p +ve and negative
    otherwise; 0 if slope is 0"""
    # note np.argmax, np.argmin returns the position of first occurence of global max, min
    sign = np.sign(np.argmax(s) - np.argmin(s))
    if sign == 0:
        return 0.0
    else:
        return sign*(np.max(s) - np.min(s))

def last_first_diff(s):
    """difference between latest and earliest value"""
    s0 = s.dropna()
    return (s0.iloc[-1] - s0.iloc[0])
    

# <codecell>

# population distributions of ambinames 
# might want to remove from consideration instances when total ratio is too great
# or range of existence of a name/sex combo too short

total_pop_ambiname = all_births.sum()[np.in1d(all_births.sum().index, ambi_names_array)]
total_pop_ambiname.sort(ascending=False)
total_pop_ambiname.plot(logy=True)

# <codecell>

# now calculate a DataFrame to visualize results

# calculate the total population, the change in p_m from last to first appearance, 
# the change from max to min in p_m, and the percentage of males overall for name

df = DataFrame()
df['total_pop'] = total_pop_ambiname
df['last_first_diff'] = p_m_cum.apply(last_first_diff)
df['min_max_range'] = p_m_cum.apply(min_max_range)
df['abs_min_max_range'] = np.abs(df.min_max_range)
df['p_m'] = p_m_cum.iloc[-1]

# distance from full ambigender -- p_m=0.5 leads to 1, p_m=1 or 0 -> 0
df['ambi_index'] = df.p_m.apply(lambda p: 1 - 2* np.abs(p-0.5))

df.head()

# <codecell>

# plot: x -> log10 of total population, y->how p_m has changed from first to last
# turn off d3 for this plot

mpld3.disable_notebook()
plt.scatter(np.log10(df.total_pop), df.last_first_diff, s=1)

# <codecell>

# turn d3 back on

mpld3.enable_notebook()

# <codecell>

# general directionality counts -- looking for over asymmetry

df.groupby(np.sign(df.last_first_diff)).count()

# <codecell>

# let's concentrate on more populous names that have seen big swings in the cumulative p_m

# you can play with the population and range filter
popular_names_with_shifts = df[(df.total_pop>5000) & (df.abs_min_max_range >0.7)]
popular_names_with_shifts.sort_index(by="abs_min_max_range", ascending=False)

# <codecell>

popular_names_with_shifts.groupby(np.sign(df.last_first_diff)).count()

# <codecell>

#popular_names_with_shifts.to_pickle('popular_names_with_shifts.pickle')

# <codecell>

fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
x = np.log10(popular_names_with_shifts.total_pop)
y = popular_names_with_shifts.min_max_range 

scatter = ax.scatter(x, y)

ax.grid(color='white', linestyle='solid')
ax.set_title("Populous Names with Major Sex Shift", size=20)
ax.set_xlabel('log10(total_pop)')
ax.set_ylabel('min_max_range')

#labels = ['point {0}'.format(i + 1) for i in range(len(x))]
labels = list(popular_names_with_shifts.index)
tooltip = plugins.PointLabelTooltip(scatter, labels=labels)
plugins.connect(fig, tooltip)

# <codecell>

prop_c_male('Leslie').plot()

# <codecell>


