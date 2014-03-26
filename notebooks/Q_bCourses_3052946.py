# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [Topic: Help with extremely simple reshaping of dataframe](https://bcourses.berkeley.edu/courses/1189091/discussion_topics/3052946):
# 
# >I'm taking advantage of this time to try and understand pandas a little better.
# 
# >I'm trying to do something that seems extremely simple. I have a dataframe with this fake data about a number of people (say, participants in a study). I want to make a frequency matrix like shown below. I've tried various grouping, reindexing, and pivoting with no luck.
# 
# <img src="http://i.imgur.com/7FPimZW.png?1?1043"/>

# <codecell>

from pandas import DataFrame

df = DataFrame({'gender':['F','M','F','M','M','F','M'],
                'major':['Biology','Chemistry','Biology','English','Biology'
                         ,'Chemistry','English']})
df

# <codecell>

df.groupby(['gender','major']).agg('count').unstack()['gender'].fillna(0)

# <codecell>

df.pivot_table(rows='gender',cols='major', aggfunc='count')

# <codecell>

df.pivot_table(rows='gender',cols='major', aggfunc='count')['gender']

# <codecell>

df.pivot_table(rows='gender',cols='major', aggfunc='count')['gender'].fillna(0)

