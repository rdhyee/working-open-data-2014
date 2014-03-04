# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# 
# * focus on a specific problem with the baby names database: compute the change in the sex of persons with given names

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

mpld3.disable_notebook()
plt.figure()
most_common_names[:50][::-1].plot(kind='barh', figsize=(10,10))

# <codecell>

mpld3.enable_notebook()

# <headingcell level=1>

# Starts and Ends of Names

# <markdowncell>

# We go from 1880 to 2010. 
# 
# It might be helpful to calculate a cumulative sum for all names...
# 
# * For a name start to happen --> look for the the first non-zero value 
# * For a name death to happen, the cumulative sum has to reach max.
# 

# <codecell>

# replace n/a with 0 -- might not actually need to do this

top_births = top_births.fillna(0)

# <codecell>

top_births_cumsum = top_births.apply(lambda s: s.cumsum(), axis=0)

# <codecell>

def start_end_years(s):
    active_years = s.index[s > 0]
    max_years = s.index[s == s.irow(-1)]
    return Series({'start': active_years[0] if len(active_years) else None,
                   'end': max_years[0] })
    
    
top_births_cumsum.apply(start_end_years)

# <headingcell level=2>

# start/end calc with whole data set

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

# <codecell>

def start_end_years(s):
    active_years = s.index[s > 0]
    max_years = s.index[s == s.irow(-1)]
    return Series({'start': active_years[0] if len(active_years) else None,
                   'end': max_years[0] })
    
    
all_start_end = all_births_cumsum.apply(start_end_years)

# <codecell>

#all_start_end.to_pickle('Day_13_Baby_Names_all_start_end.pickle')
#all_start_end = pd.read_pickle('Day_13_Baby_Names_all_start_end.pickle')

# <codecell>

all_start_end.tail()

# <codecell>

vc_start = all_start_end.ix['start'].value_counts()
vc_end = all_start_end.ix['end'].value_counts()

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.ylim(0,2000)
ax1.scatter(vc_start.index, vc_start, c='b')
ax1.scatter(vc_end.index, vc_end, c='r')
ax1.set_xlabel('year')
ax1.set_xlabel('number of starts/ends')

plt.tight_layout()

plt.show()

# <headingcell level=2>

# Names that are both M and F

# <codecell>

# remind ourselves of what's in names

names.head()

# <codecell>

# columns in names

names.columns

# <codecell>

# forgive my use of the non-descriptive k, k1 here

k = names.groupby(['name', 'sex']).apply(lambda g: len(g.groupby('sex')))
k.head()

# <codecell>

k = k.unstack()
k = k.fillna(0)
k.head()

# <codecell>

male_names = set(k[k.M==1].index)
female_names = set(k[k.F==1].index)
ambi_names = male_names & female_names
# alternative calc
# ambigender_names = set(k[k.T.sum()==2].index)
male_only_names = male_names - female_names
female_only_names = female_names - male_names

len(male_only_names), len(female_only_names), len(ambi_names), \
  len(male_only_names) + len(female_only_names) + len(ambi_names)
    
ambi_names_array = np.array(list(ambi_names))

# <codecell>

len(male_only_names), len(female_only_names), len(ambi_names), \
  len(male_only_names) + len(female_only_names) + len(ambi_names)
    

# <codecell>

# this might be a better way to get at the set of male_only, female_only, ambigender names

def another_calc_of_sex_of_names():

    k = names.groupby('sex').apply(lambda s: set(list(s['name'])))
    male_only_names = k['M'] - k['F']
    female_only_names = k['F'] - k['M']
    ambi_names = k['F'] & k['M'] # intersection of two 
    print len(male_only_names), len(female_only_names), len(ambi_names)
    
another_calc_of_sex_of_names()    

# <codecell>

# total number of people in names
names.births.sum()

# <codecell>

k1 = names[np.in1d(names.name,ambi_names_array)][['name', 'sex', 'births','year']][::].pivot_table('births', rows='year', cols=['name','sex'], aggfunc=np.sum)

# <codecell>

# total number of people in k1 -- almost everyone!
k1.sum().sum()

# <codecell>

k1=k1.fillna(0L)
k1.tail()

# <codecell>

# plot M, F in ambigender_names over time
k1.T.xs('M',level='sex').sum().cumsum()

# <codecell>

k1.T.xs('F',level='sex').sum().cumsum()

# <codecell>

(k1.T.xs('M',level='sex').sum().cumsum() / k1.T.xs('F',level='sex').sum().cumsum()).plot()

# <codecell>

# don't know what pivot table has type float
# https://github.com/pydata/pandas/issues/3283
k1['Raymond', 'M'].dtype

# <codecell>

(k1['Leslie']['M']/(k1['Leslie']['M'] + k1['Leslie']['F'])).plot()

# <codecell>

k1.T.ix[:].apply(lambda s: type(s),axis=1)

# <codecell>

from itertools import islice

names_to_calc = list(islice(list(k1.T.index.levels[0]),None))

m = [(name_, k1[name_]['M']/(k1[name_]['F'] + k1[name_]['M']))  \
     for name_ in names_to_calc]
p_m_instant = DataFrame(dict(m))
p_m_instant.tail()

# <codecell>

from itertools import islice

names_to_calc = list(islice(list(k1.T.index.levels[0]),None))

m = [(name_, k1[name_]['M'].cumsum()/(k1[name_]['F'].cumsum() + k1[name_]['M'].cumsum()))  \
     for name_ in names_to_calc]
p_m_cum = DataFrame(dict(m))
p_m_cum.tail()

# <codecell>

p_m_cum['Donnie'].plot()

# <codecell>

# first pass

p_m_diff = p_m_cum.apply(lambda s:s[2010]-s[1880])

# <codecell>

p_m_diff.sort()
p_m_diff.dropna()

# <codecell>

def start_end_years(s):
    active_years = s.index[s > 0]
    max_years = s.index[s == s.irow(-1)]
    return Series({'start': active_years[0] if len(active_years) else None,
                   'end': max_years[0] })

def max_slope0(s):
    
    sign = np.sign(np.argmax(s) - np.argmin(s))
    if sign == 0:
        return 0.0
    else:
        return 100*sign*(np.max(s) - np.min(s))

def max_slope(s):
    """grab earliest and latest value"""
    s0 = s.dropna()
    return 100*(s0.iloc[-1] - s0.iloc[0])
    
slope = p_m_cum.apply(max_slope)

# <codecell>

slope.sort()
slope.tail()

# <codecell>


# <codecell>

# population distributions of ambinames 
# might want to remove from consideration instances when total ratio is too great
# or range of existence of a name/sex combo too short

total_pop_ambiname = all_births.sum()[np.in1d(all_births.sum().index, ambi_names_array)]
total_pop_ambiname.sort(ascending=False)
total_pop_ambiname.plot(logy=True)

# <codecell>

# population distribution of ambigender names
plt.hist(all_births.sum()[np.in1d(all_births.sum().index, ambi_names_array)], bins=50, log=True)

# <codecell>

# something wrong with this plot

plt.scatter(total_pop_ambiname, slope, c="red", s=1)

# <codecell>

k2 = DataFrame()
k2['total_pop'] = total_pop_ambiname
k2['slope'] = slope
k2.head()

# <codecell>


plt.scatter(np.log10(k2.total_pop), k2.slope, s=1)

# <codecell>

# general directionality counts

k2.groupby(np.sign(k2.slope)).count()

# <codecell>

popular_names_with_shifts = k2[(k2.total_pop>10000) & (abs(k2.slope)>80)]
popular_names_with_shifts.sort_index(by="slope", ascending=False)


# <codecell>

popular_names_with_shifts.groupby(np.sign(k2.slope)).count()

# <codecell>

plt.scatter(np.log10(popular_names_with_shifts.total_pop), popular_names_with_shifts.slope)

# <codecell>

#popular_names_with_shifts.to_pickle('popular_names_with_shifts.pickle')

# <codecell>

fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
x, y = np.log10(popular_names_with_shifts.total_pop), popular_names_with_shifts.slope


scatter = ax.scatter(x, y)

ax.grid(color='white', linestyle='solid')

ax.set_title("Scatter Plot (with tooltips!)", size=20)

#labels = ['point {0}'.format(i + 1) for i in range(len(x))]
labels = list(popular_names_with_shifts.index)
tooltip = plugins.PointLabelTooltip(scatter, labels=labels)
plugins.connect(fig, tooltip)

# <codecell>


