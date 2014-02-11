# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab --no-import-all inline

# <codecell>

#  import useful classes of pandas
import pandas as pd
from pandas import Series, DataFrame, Index

# <codecell>

import settings
import census

c = census.Census(key=settings.CENSUS_KEY)

# <headingcell level=1>

# Fields in SF1

# <codecell>

sf1_fields = c.sf1.fields(year=2010)

# <codecell>

sorted(sf1_fields.keys())

# <markdowncell>

# Let's parse more of pieces that are in the fields

# <codecell>

# let's just parse sf1.xml ourselves to get the concepts
# http://lxml.de/parsing.html

from lxml import etree
from itertools import islice
import re

def parse_concept_name(concept_name):
    if concept_name != 'Geographic Characteristics':
        m = re.search("(.+\.)\s+(.*)\s+(\[\d+\])",concept_name)
        if m: 
           return {'label':m.group(1),
                  'clean_name':m.group(2),
                  'num_vars':re.search("\[(\d+)\]", m.group(3)).group(1)
                  }
       # print m.groups()
        else:
           m1 = re.search("(.+\.)\s+(.*)\s+",concept_name)
           return {'label':m1.group(1),
                  'clean_name':m1.group(2),
                  'num_vars':0
                 }
    else:
        return None
    
def concepts_2010_sf1():
    # http://www.census.gov/developers/data/sf1.xml
    SF1_XML_PATH  = "/Users/raymondyee/D/Document/Working_with_Open_Data/working-open-data-2014/data/sf1.xml"

    doc = etree.parse(SF1_XML_PATH)
    for concept in doc.findall("//concept"):
        concept_name = concept.attrib['name']
        
        if concept_name != 'Geographic Characteristics':
            m = re.search("(.+\.)\s+(.*)\s+(\[\d+\])",concept_name)
            if m: 
               yield {'label':m.group(1),
                      'clean_name':m.group(2),
                      'num_vars':re.search("\[(\d+)\]", m.group(3)).group(1)
                      }
           # print m.groups()
            else:
               m1 = re.search("(.+\.)\s+(.*)\s+",concept_name)
               yield {'label':m1.group(1),
                      'clean_name':m1.group(2),
                      'num_vars':0
                     }
            
k = list(concepts_2010_sf1())    

# <codecell>

df = DataFrame(k, columns=('label','clean_name','num_vars'))
df.head()

# <codecell>

import re

def sort_label(label):
    (l1, l2, l3) = re.search("([A-Z,a-z]+)(\d+)([A-Z,a-z]*)\.",label).groups()
    return l1 + " " + "{l2:03d}".format(l2=int(l2)) + l3

df['sort_label'] = df.label.apply(sort_label)

# <codecell>

df[df.label.str.startswith("P5")]

# <codecell>

# let's go right for the variables and generate a dict, DF

from lxml import etree
from itertools import islice
from collections import OrderedDict

SF1_XML_PATH  = "/Users/raymondyee/D/Document/Working_with_Open_Data/working-open-data-2014/data/sf1.xml"

doc = etree.parse(SF1_XML_PATH)
variables = doc.findall("//variable")

variables_dict = OrderedDict([(v.attrib['name'], 
                               {'concept':v.attrib['concept'],
                                'text': v.text
                                }) for v in variables])


# <codecell>

variables_dict['P0050001']

# <codecell>

def P005_range(n0,n1): 
    return tuple(('P005'+ "{i:04d}".format(i=i) for i in xrange(n0,n1)))

P005_vars = P005_range(1,18)
P005_vars_str = ",".join(P005_vars)

[(v,variables_dict[v]['text']) for v in P005_vars]

# <codecell>

variables_df = DataFrame(variables_dict)
variables_df.head()

# <codecell>

variables_df.T.concept.apply(parse_concept_name)

# <codecell>

parse_concept_name(variables_dict['P0050001']['concept'])

# <headingcell level=1>

# api.json

# <codecell>

# http://www.census.gov/developers/

import requests
url = "http://api.census.gov/data.json"
api_json = requests.get(url).json()
api_json

# <codecell>

len(api_json)

# <codecell>

[(api['c_vintage'], api['c_dataset'], api['c_variablesLink']) for api in api_json]

# <headingcell level=1>

# variables.json

# <codecell>

import requests
url = "http://api.census.gov/data/2010/sf1/variables.json"
var_json = requests.get(url).json()
sorted(var_json['variables'].keys())

# <codecell>

var_json['variables']['P0050002']

# <codecell>

from pandas import DataFrame
DataFrame(var_json['variables']).T

# <headingcell level=1>

# Plotting Age Distribution By Gender (Population Pyramid)

# <markdowncell>

# This example written by AJ Renold.

# <codecell>

sf1_fields = c.sf1.fields(year=2010)

# Get the sf1 fields that are only P12 Sex By Age
gender_population_fields = sf1_fields.get('P12. Sex By Age [49]')

# Separate the by male and female
male_fields = { key: val for key, val in gender_population_fields.items() 
                                 if 'Male' in val and val != ' Male: ' }
female_fields = { key: val for key, val in gender_population_fields.items() 
                                   if 'Female' in val and val != ' Female: '}

# <codecell>

# Query the census API with the gender_population_fields
query_results = c.sf1.get(('NAME', ','.join(gender_population_fields.keys())), geo={'for': 'state:*'})

# Create a DataFrame
gender_df = pd.DataFrame(query_results)

# <codecell>

# Set the Index to the NAME column
gender_df = gender_df.set_index(gender_df['NAME'])

# <codecell>

# Recast all numeric columns to be type int
for col in gender_df.columns:
    if col != "state" and col != "NAME":
        gender_df[col] = gender_df[col].astype(int)

# <codecell>

from numpy import arange

def showPopulationPyramidPlot(df, state, male_fields, female_fields):
    
    # create a series with the row of the state
    s = Series(df.ix[state])
    #del s['NAME']
    #del s['state']
    
    # get the plot values and labels from the series
    male_list = sorted([ [key, s[key]] for key in s.keys() if key in male_fields ])
    female_list = sorted([ [key, s[key]] for key in s.keys() if key in female_fields ]) 
    
    # calculate the bar locations and the maximum value
    bar_ypos = arange(len(male_list))+.5
    max_val = max([ val for label, val in male_list + female_list ])
    
    # create the figures for the plots
    fig, (ax2, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(18,8))
    fig.suptitle('Population Age Pyramid for {state}'.format(state=state), fontsize=14)
    
    # plot the male populations
    bar1 = ax1.barh(bar_ypos, [ val for label, val in male_list ], align='center')
    ax1.set_xlim((0,max_val))
    ax1.set_yticks(bar_ypos)
    ax1.set_yticklabels([ male_fields[label][male_fields[label].find('!!')+3:] for label, val in male_list ])
    ax1.set_xlabel('People')
    ax1.set_title('Male Population by Age')
    ax1.grid(True)
    
    # plot the the female populations
    bar2 = ax2.barh(bar_ypos,[ val for label, val in female_list ], align='center', color='red')
    ax2.set_yticks([])
    #ax2.yaxis.tick_right()
    ax2.set_xlim(ax1.get_xlim()[::-1]) # reverses the x axis direction
    ax2.set_xlabel('People')
    ax2.set_title('Female Population by Age')
    ax2.grid(True)
    
    plt.subplots_adjust(wspace=0.22, hspace=0.0)
    plt.show()

# <codecell>

showPopulationPyramidPlot(gender_df, 'Illinois', male_fields, female_fields)

# <codecell>


