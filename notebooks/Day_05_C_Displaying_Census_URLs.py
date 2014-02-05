# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab --no-import-all inline

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series, Index
import pandas as pd

# <codecell>

# check that CENSUS_KEY is defined

import settings
assert settings.CENSUS_KEY is not None

# <markdowncell>

# The census documentation has example URLs but needs your API key to work.  In this notebook, we'll use the IPython notebook HTML display mechanism to help out.

# <codecell>

# http://api.census.gov/data/2010/sf1/geo.html

# <codecell>

from IPython.core.display import HTML

# <codecell>

HTML("<iframe src='http://api.census.gov/data/2010/sf1/geo.html' width='800px'/>")

# <codecell>

%%HTML
<b>hi there</b>

# <codecell>

import urlparse
import urllib
from IPython.core.display import HTML

def add_census_key(url, api_key=settings.CENSUS_KEY):
    """Take an input example Census API call and a key parameter"""

    pr = urlparse.urlparse(url)
    
    # we're going to modify the query, which is the 5th element in the tuple (index 4)
    pr1 = list(pr)
    
    # convert pr.query from string to dict
    # see http://stackoverflow.com/a/10233141/7782 for meaning of doseq
    pr_query = urlparse.parse_qs(pr.query)
    pr_query["key"]= api_key

    pr1[4] = urllib.urlencode(pr_query, doseq=True)
    
    return urlparse.urlunparse(pr1)


def c_url (url, title=None, api_key=settings.CENSUS_KEY):
    url_with_key = add_census_key(url, api_key)
    if title is None:
        title = url
    return HTML("""<a href="{url}">{title}</a>""".format(url=url_with_key, title=title))

#add_census_key("http://api.census.gov/data/2010/sf1?get=P0010001&for=county:*")
c_url("http://api.census.gov/data/2010/sf1?get=NAME,P0010001&for=state:*")

# <headingcell level=1>

# Scraping the examples

# <codecell>

import requests
from lxml.html import parse, fromstring

url = "http://api.census.gov/data/2010/sf1/geo.html"
r = requests.get(url).content
doc = fromstring(r)

rows = doc.xpath("//table/tr")

# first row is the header

headers = [col.text for col in rows[0].findall('th')]
headers

# next rows are the census URL examples

# <codecell>

row = rows[1]
cols = row.findall('td')

# col[s0]:  Summmary Level

print cols[0].text

# cols[1]:  Description

print cols[1].text

# <codecell>

from itertools import islice
from lxml.html import parse

# let's actually now decorate the urls

def decorated_parse_examples(examples, api_key=settings.CENSUS_KEY):
    for row in examples:
        new_row = row.copy()
        # need to change URLs
        
        example_urls_col = new_row[headers[2]]
        #urls_with_key  = [add_census_key(url) for url in example_urls_col]
        
        new_row[headers[2]] = "<br/>".join(
            ["""<a href="{url_with_key}">{url}</a>""".format(
                url=url, 
                url_with_key=add_census_key(url)
                ) for url in example_urls_col
            ])
        
        yield new_row
        
def parse_urls_col(col):
    # http://stackoverflow.com/a/15074386/7782
    return [child for child in col.itertext()]

def parse_census_examples():

    url = "http://api.census.gov/data/2010/sf1/geo.html"
    doc = parse(url)

    rows = doc.xpath("//table/tr")

    # first row is the header

    headers = [col.text for col in rows[0].findall('th')]

    for row in rows[1:]:
        cols = row.findall('td')
        yield ({headers[0]:cols[0].text, 
                headers[1]:cols[1].text, 
                headers[2]:parse_urls_col(cols[2])})

#parsed_examples = list(islice(parse_census_examples(),None))
parsed_examples = parse_census_examples()

# <codecell>

# let's redisplay the table with 

from IPython.display import HTML
from jinja2 import Template

URLS_TEMPLATE= """
 <table>
   <tr>
   {% for header in headers %}
     <th>{{header}}</th>
   {% endfor %}
   </tr>
   {% for row in rows %}
   <tr>
    {% for header in headers %}
      <td>{{row[header]}}</td>
    {% endfor %}
   </tr>
   {% endfor %}
 </table>"""
    
template = Template(URLS_TEMPLATE)
HTML(template.render(headers=headers, rows=decorated_parse_examples(parsed_examples))) 

