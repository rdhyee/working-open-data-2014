# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# * learn from how `PfDA` treats the baby names database
# * focus on a specific problem with the baby names database: compute the change in the sex of persons with given names

# <codecell>

%pylab --no-import-all inline

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

from pylab import figure, show

from pandas import DataFrame, Series
import pandas as pd

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

# <headingcell level=2>

# Start with one year 1880

# <codecell>

# take a look at some lines from each of the names files

import os
os.path.join(NAMES_DIR,'yob1880.txt')
yob1880_path = os.path.join(NAMES_DIR,'yob1880.txt')
!head $yob1880_path

# <codecell>

# create a DataFrame for 1880 data

import pandas as pd
import codecs

names1880_file = codecs.open(os.path.join(NAMES_DIR,'yob1880.txt'), encoding='iso-8859-1')
names1880 = pd.read_csv(names1880_file, names=['name', 'sex', 'births'])

names1880.head()

# <codecell>

# how many females represented in the 1880 data?

names1880[names1880.sex=='F']['births'].sum()

# <codecell>

# number of names in 1880 file

len(names1880.groupby('name')) 

# <codecell>

# group by name to find out which names are both M and F -- by looking at which names have more 
# than one sex represented.

name_count = names1880.groupby('name').apply(lambda s: len(s))
set(name_count[name_count > 1].index)

# <codecell>

# number of births by sex for 1880

names1880.groupby('sex').sum()

# <codecell>

# total number of births in 1880

names1880['births'].sum()

# <codecell>

# sort by number of births to get most popular names 

names1880.sort('births', ascending=False)[:10]

# <codecell>

# most popular female names

names1880[names1880.sex == 'F'].sort('births', ascending=False)[:10]

# <codecell>

# try out seaborn if you want
# import seaborn as sns

# <codecell>

num_names1880 = len(names1880['births'].order(ascending=False))
plt.plot(np.arange(num_names1880), names1880['births'].order(ascending=False), 'ro', ms=1)
plt.yscale('log')
plt.xlabel('order of name')
plt.ylabel('number of babies')

# <headingcell level=1>

# Loading all data into Pandas

# <codecell>

!ls $NAMES_DIR

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

# number of names in 1880
#names.groupby('year').apply(lambda s: s.groupby('name').agg('count'))
#len(names1880.groupby('name').agg('count'))
len(names1880.groupby('name'))

# <codecell>

# can groupby more than one column
# 131 years x 2 sexes

len(names.groupby(['year', 'sex']))

# <codecell>

# how many combo of name x year

len(names.groupby(['name','year']))

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

plt.figure()
most_common_names[:50][::-1].plot(kind='barh', figsize=(10,10))

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

def start_year(s):
    active_years = s.index[s > 0]
    if len(active_years):
        return active_years[0]
    else:
        return None
    
def end_year(s):
    max_years = s.index[s == s.irow(-1)]
    return max_years[0]

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

# all_start_end.to_pickle('Day_12_Baby_Names_all_start_end.pickle')

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

# <headingcell level=1>

# Experiments -- don't need to look at closely

# <codecell>

# max / min totals and when? -- awkward -- must be a better way
total_births_sum = names.groupby('year').sum()
max_value = list(total_births_sum.max())[0]
min_value = list(total_births_sum.min())[0]

is_max = total_births_sum.births == max_value
is_min = total_births_sum.births == min_value
is_max[is_max], is_min[is_min]

# <codecell>

# a "derivative" -- when is there great population rate change

total_births_sum.diff().plot()

# <codecell>

# plot multiple names on same plot or as multiple axes

def name_sex_count_in_year(name,sex):
    return names[(names.name==name) & (names.sex==sex)][['year', 'births']].set_index(keys='year')

def name_sex_prop_in_year(name,sex):
    return names[(names.name==name) & (names.sex==sex)][['year', 'prop']].set_index(keys='year')

name_df = DataFrame(index=np.arange(1880,2010))

name_df['Raymond'] = name_sex_count_in_year('Raymond','M')
name_df['Laura'] = name_sex_count_in_year('Laura','F')

name_df.plot()

# <codecell>

# plot proportion instead of absolute births

name_df = DataFrame(index=np.arange(1880,2010))

name_df['Raymond'] = name_sex_prop_in_year('Raymond','M')
name_df['Laura'] = name_sex_prop_in_year('Laura','F')

name_df.plot()

# <codecell>

total_births.plot(title='Total births by sex and year')

# <codecell>

# http://en.wikipedia.org/wiki/Human_sex_ratio
# make an agg figure
fig = figure()

# meaning of 111: http://stackoverflow.com/a/3584933/7782
ax = fig.add_subplot(111)
ax.set_title('Ratio of M to F births')

cum_ratio_by_sex = total_births.M.cumsum() / total_births.F.cumsum()
cum_ratio_by_sex.plot(ax=ax, label="cumulative", color="red")

# add instantaneous ratio

annual_ratio_by_sex = total_births.M / total_births.F
annual_ratio_by_sex.plot(ax=ax, label="annual", color="green")

ax.legend(loc='best')

fig.canvas.draw()

# <codecell>

# number of names over time

names.groupby('year').count()[['name']].plot()

# <codecell>

# first attempt to calculate entropy of names

fig = figure()

# meaning of 111: http://stackoverflow.com/a/3584933/7782
ax = fig.add_subplot(111)
ax.set_title('Entropy of names')

S_male = names[names.sex=='M'].groupby('year').prop.agg(lambda x: sum([-j*np.log(j) for j in x])) # apply(lambda x: -x*log(x))
S_male.plot(ax=ax, label="M", color="blue")

S_female = names[names.sex=='F'].groupby('year').prop.agg(lambda x: sum([-j*np.log(j) for j in x])) # apply(lambda x: -x*log(x))
S_female.plot(ax=ax, label="F", color="red")

ax.legend(loc='best')
ax.set_ylim(0)

fig.canvas.draw()

# <headingcell level=2>

# Names that are both M and F

# <markdowncell>

# Goal:  start to explore names that have been given to both male and female babies. Is there a general trend to feminization of names?  (That is, is it more likely that names start as male names become feminine names than vice versa?)

