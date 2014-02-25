# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# **Chapter 2, 3 of PDA**

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

USAGOV_BITLY_PATH = os.path.join(os.pardir, "pydata-book", "ch02", "usagov_bitly_data2012-03-16-1331923249.txt")
MOVIELENS_DIR = os.path.join(os.pardir, "pydata-book", "ch02", "movielens")
NAMES_DIR = os.path.join(os.pardir, "pydata-book", "ch02", "names")

assert os.path.exists(USAGOV_BITLY_PATH)
assert os.path.exists(MOVIELENS_DIR)
assert os.path.exists(NAMES_DIR)

# <markdowncell>

# **Please make sure the above assertions work**

# <headingcell level=1>

# usa.gov bit.ly example

# <markdowncell>

# (`PfDA`, p. 18)
# 
# *What's in the data file?*
# 
# <http://my.safaribooksonline.com/book/programming/python/9781449323592/2dot-introductory-examples/id2802197> :
#     
# > In 2011, URL shortening service bit.ly partnered with the United States government website usa.gov to provide a feed of anonymous data gathered from users who shorten links ending with .gov or .mil.
#     
# Hourly archive of data: <http://bitly.measuredvoice.com/bitly_archive/?C=M;O=D>

# <codecell>

open(USAGOV_BITLY_PATH).readline()

# <codecell>

import json
records = [json.loads(line) for line in open(USAGOV_BITLY_PATH)]  # list comprehension

# <headingcell level=2>

# Counting Time Zones with pandas

# <markdowncell>

# Recall what `records` is

# <codecell>

len(records)

# <codecell>

# list of dict -> DataFrame

frame = DataFrame(records)
frame.head()

# <headingcell level=1>

# movielens dataset

# <markdowncell>

# PDA p. 26 
# 
# http://www.grouplens.org/node/73 --> there's also a 10 million ratings dataset -- would be interesting to try out to test scalability
# of running IPython notebook on laptop
# 

# <codecell>

# let's take a look at the data

# my local dir: /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ch02/movielens

!head $MOVIELENS_DIR/movies.dat

# <codecell>

# how many movies?
!wc $MOVIELENS_DIR/movies.dat

# <codecell>

!head $MOVIELENS_DIR/users.dat

# <codecell>

!head $MOVIELENS_DIR/ratings.dat

# <codecell>

import pandas as pd
import os

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(MOVIELENS_DIR, 'users.dat'), sep='::', header=None,
  names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(MOVIELENS_DIR, 'ratings.dat'), sep='::', header=None,
  names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(os.path.join(MOVIELENS_DIR, 'movies.dat'), sep='::', header=None,
  names=mnames, encoding='iso-8859-1')

# <codecell>

movies[:100]

# <codecell>

import traceback

try:
    movies[:100]
except:
    traceback.print_exc()

# <codecell>

# explicit encoding of movies file

import pandas as pd
import codecs


unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(MOVIELENS_DIR, 'users.dat'), sep='::', header=None,
  names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(MOVIELENS_DIR, 'ratings.dat'), sep='::', header=None,
  names=rnames)


movies_file = codecs.open(os.path.join(MOVIELENS_DIR, 'movies.dat'), encoding='iso-8859-1')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movies_file, sep='::', header=None,
  names=mnames)


# <codecell>

movies[:100]

# <codecell>

users[:5]

# <codecell>

movies[:100]

# <markdowncell>

# hmmm...age 1?  Where to learn about occupation types?  We have zip data...so it'd be fun to map.  Might be useful to look at
# distribution of age, gender, and zip.

# <headingcell level=2>

# check on encoding of the movie files

# <codecell>

import codecs
from itertools import islice

fname = os.path.join(MOVIELENS_DIR, "movies.dat")

f = codecs.open(fname, encoding='iso-8859-1')
for line in islice(f,100):
    print line

# <codecell>

import pandas as pd
import codecs

movies_file = codecs.open(os.path.join(MOVIELENS_DIR, 'movies.dat'), encoding='iso-8859-1')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(movies_file, sep='::', header=None,
  names=mnames)

print (movies.ix[72]['title'] == u'Misérables, Les (1995)')

# <headingcell level=1>

# Baby names dataset

# <codecell>

import pandas as pd
import codecs

names1880_file = codecs.open(os.path.join(NAMES_DIR,'yob2010.txt'), encoding='iso-8859-1')
names1880 = pd.read_csv(names1880_file, names=['name', 'sex', 'births'])

names1880

# <codecell>

# sort by name

names1880.sort('births', ascending=False)[:10]

# <codecell>

names1880[names1880.sex == 'F'].sort('births', ascending=False)[:10]

# <codecell>

names1880['births'].plot()

# <codecell>

names1880['births'].count()

# <codecell>


