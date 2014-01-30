# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# How to use Python for Data Analysis (PfDA)

# <markdowncell>

# 
# *Reading Assigned a while ago from PfDA*
# 
#    * read [`PfDA`, Chap 1  Preliminaries](http://proquest.safaribooksonline.com/book/programming/python/9781449323592/1dot-preliminaries/id2664030), especially the installation instructions for EPD Free for your computer platform.  I want you to try installing EPD Free (or EPD Academic) before class on Thursday.
#    * read [`PfDA`, Chap 3](http://proquest.safaribooksonline.com/book/programming/python/9781449323592/3dot-ipython-an-interactive-computing-and-development-environment/id2545624) 
#    * skim [`PfDA`, Appendix: Python Language Essentials](http://proquest.safaribooksonline.com/book/programming/python/9781449323592/adot-python-language-essentials/id2819503) -- to help remind yourself of key elements of standard Python 
#    * skim [`PfDA`, Chap 2 Introductory Examples](http://proquest.safaribooksonline.com/book/programming/python/9781449323592/2dot-introductory-examples/id423077) 

# <markdowncell>

# * Github repo for book: [pydata/pydata-book](https://github.com/pydata/pydata-book)
# * [Confirmed Errata | O'Reilly Media Python for Data Analysis](http://www.oreilly.com/catalog/errata.csp?isbn=0636920023784)
# * [Unconfirmed Errata | O'Reilly Media Python for Data Analysis](http://www.oreilly.com/catalog/errataunconfirmed.csp?isbn=0636920023784)

# <markdowncell>

# I suggest cloning the repo somewhere on your computer
# 
# my own setup: I've git cloned 
# 
#     https://github.com/pydata/pydata-book.git
# 
# into 
# 
#     /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/
#     
# and put a symbolic link to /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ in my working-with-open-data-2014 repo parallel to the notebooks directory.

# <codecell>

%%bash
# this is what I ran on my mac to make this link
cd ..
ln -s /Users/raymondyee/D/Document/Working_with_Open_Data/pydata-book/ pydata-book

# <codecell>

%%bash
# in my case, I had been adding other notebooks
ls ../pydata-book/

# <headingcell level=1>

# Calculate PFDA_PATH (for RY's relative dir setup) or set it manually

# <codecell>

#http://stackoverflow.com/a/17295128/7782
import os
PFDA_PATH  = os.path.abspath(os.path.join(os.getcwd(), 
                                          os.path.join(os.path.pardir, "pydata-book")
                                        ))
PFDA_PATH

# <codecell>

assert os.path.exists(PFDA_PATH)

# <headingcell level=1>

# Chapter 1

# <codecell>

# locat the bitly file and make sure it exists
import os

path = os.path.join(PFDA_PATH,'ch02/usagov_bitly_data2012-03-16-1331923249.txt')
print "bit.ly data file exists: ", os.path.exists(path)

# <codecell>

# let's try some of the code from PfDA
# read a line
open(path).readline()

# <codecell>

import json
records = [json.loads(line) for line in open(path)]
time_zones = [rec.get('tz') for rec in records]

# <codecell>

time_zones

# <headingcell level=2>

# Jumping to "Counting Time Zones with pandas" (p.21) 

# <codecell>

from pandas import DataFrame, Series
import pandas as pd

# <codecell>

frame = DataFrame(records)  # records is a list of dicts

# <codecell>

frame['tz'].value_counts()

# <codecell>

# fill missing


clean_tz = frame['tz'].fillna('Missing')
clean_tz.value_counts()

# <codecell>

clean_tz[clean_tz==''] = 'Unknown'

# <codecell>

clean_tz.value_counts()

# <codecell>

# let's embed the plot inline
%pylab --no-import-all inline

# <codecell>

tz_counts = clean_tz.value_counts()

# <codecell>

tz_counts[:10].plot(kind='barh', rot=0)

# <markdowncell>

# And so on....

