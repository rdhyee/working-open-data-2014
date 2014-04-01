# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# HackFSM
# 
# Relationship to other public APIs based on Solr?
# 
# * http://www.hathitrust.org/htrc/solr-api
# * http://api.plos.org/solr/search-fields/
# 

# <markdowncell>

# Documentation:
#     
# http://digitalhumanities.berkeley.edu/hackfsm/api/detail

# <codecell>

from settings import (HACKFSM_ID, HACKFSM_KEY, HACKFSM_BASEURL)
from itertools import islice

import logging
import requests
import json
import urllib
import urlparse

from pandas import DataFrame, Series
import pandas as pd
import numpy as np

logging.basicConfig(filename='Experiment_20140325_HackFSM.log',level=logging.WARNING)
logger=logging.getLogger()

# <codecell>

def query(q, fl="id"):
    url = "{base_url}?".format(base_url=HACKFSM_BASEURL) + \
            urllib.urlencode({'q':q,
                              'fl':fl,
                              'wt':'json',
                              'app_id':HACKFSM_ID,
                              'app_key':HACKFSM_KEY})
    r = requests.get(url)
    return r.json()
        

# <codecell>

result = query(q="fsmTitle:Savio")['response']
result

# <headingcell level=1>

# Paging through results

# <codecell>

# try again
# http://stackoverflow.com/a/5724453/7782
# http://excess.org/article/2013/02/itergen1/


class my_g(object):
    def __init__(self,max_count):
        self._remaining = range(max_count)
        self._len = max_count
    def __iter__(self):
        return self
    def __len__(self):
        return self._len
    def next(self):
        if not self._remaining:
            raise StopIteration
        return self._remaining.pop(0)

g=my_g(10)
print len(g)
list(g)

# <codecell>

class FSM(object):
    def __init__(self, q, fl="id", start=0, rows=30,
                 base_url=HACKFSM_BASEURL, app_id=HACKFSM_ID, app_key=HACKFSM_KEY):
        self.q = q
        self.fl = fl
        self.start = start
        self.rows = rows
        
        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key

        # get first page and numfound
        self.cursor = start 
        
        # get the first page
        result = self._get_page(q, fl, self.cursor, self.rows)
        self.numfound = result['response']['numFound']
    
    def _check_status(self,result):
        """throw exception if non-zero status"""
        if result['responseHeader']['status'] != 0:
            raise FSMException("status: " + str(result['responseHeader']['status']))

    def _get_page(self, q, fl, start, rows):
        result = self._call_api(q, fl, start, rows)
        
        # update current page
        self.page = result['response']['docs']
        self.page_len = len(self.page)
        
        return result
    
    def _call_api(self, q, fl, start, rows):
        url = "{base_url}?".format(base_url=self.base_url) + \
            urllib.urlencode({'q':q,
                              'fl':fl,
                              'wt':'json',
                              'start':start,
                              'row':rows,
                              'app_id':self.app_id,
                              'app_key':self.app_key})

        result = requests.get(url).json()
        self._check_status(result)
        
        # check whether we're getting fewer records than expected
        if len(result['response']['docs']) < rows:
            # are we at the end of the results
            if start + len(result['response']['docs']) != self.numfound:
                logger.warning("url:{url}, numfound:{numfound}, start+len{start_plus_len}".format(url=url,
                                                            numfound=self.numfound,
                                                            start_plus_len=start + len(result['response']['docs'])))
                
        
        return result

    def __iter__(self):
        return self
    def __len__(self):
        return self.numfound
    def next(self):
        if not self.page:
            # retrieve next page and check whether there's anything left
            self.cursor += self.page_len
            result = self._get_page(self.q, self.fl, self.cursor, self.rows)
    
            if self.page_len == 0:
                raise StopIteration
                
        return self.page.pop(0)
    

# <codecell>

fsm = FSM("-fsmTeiUrl:[* TO *]", fl="id,fsmTitle,fsmImageUrl,fsmDateCreated")

# <codecell>

len(fsm)

# <codecell>

results = list(islice(fsm,None))
results[:10]

# <codecell>

df = DataFrame(results)

# <codecell>

len(df)

# <codecell>

df.fsmImageUrl

# <codecell>

from IPython.display import HTML
from jinja2 import Template

CSS = """
<style>
  .wrap img {
    margin-left: 0px;
    margin-right: 0px;
    display: inline-block;
    width: 150px;
  }
  
.wrap {
   /* Prevent vertical gaps */
   line-height: 0;
   
   -webkit-column-count: 5;
   -webkit-column-gap:   0px;
   -moz-column-count:    5;
   -moz-column-gap:      0px;
   column-count:         5;
   column-gap:           0px;
   
}
.wrap img {
  /* Just in case there are inline attributes */
  width: 100% !important;
  height: auto !important;
}

</style>
"""

IMAGES_TEMPLATE = CSS + """
<div class="wrap">
 {% for item in items %}<img title="{{item.fsmTitle.0}}" src="{{item.fsmImageUrl.0}}"/>{% endfor %}
</div>
"""
    
template = Template(IMAGES_TEMPLATE)
HTML(template.render(items=results[:10])) 

# <markdowncell>

# # DISTINGUISHING IMAGES FROM DOCUMENTS
# 
# To programmatically differentiate records that describe images from records that describe TEI-encoded XML documents, the API permits queries that exclude records with NULL values in the "unwanted" Url field.
#  
# That is, to retrieve TEI documents only, one would query for null values in the `fsmImageUrl` field. To retrieve images only, one would query for null values in the `fsmTeiUrl` field.
#  
# NOTE: Please observe the hyphen prepended to the field names in the examples below. The hyphen (minus sign) functions here as a NOT operator.
#  
# Example that selects for TEI encoded XML documents by excluding null values of `fsmImageUrl`:
#  
#      https://<BASE URL>/solr/fsm/select?q=-fsmImageUrl:[* TO *]&wt=json&indent=true&app_id=abcdefgh&app_key=12345678901234567890123456789012
#  
# Example that selects for images by excluding null values of fsmTeiUrl:
#  
#      https://<BASE URL>/solr/fsm/select?q=-fsmTeiUrl:[* TO *]&wt=json&indent=true&app_id=abcdefgh&app_key=12345678901234567890123456789012

# <codecell>

# TEI-encoded docs

len(FSM("-fsmImageUrl:[* TO *]"))

# <codecell>

# images

len(FSM("-fsmTeiUrl:[* TO *]", fl="id,fsmImageUrl"))

# <headingcell level=1>

# Studying the API parameters

# <codecell>

from lxml.html import parse, fromstring
from collections import OrderedDict

api_docs_url = "http://digitalhumanities.berkeley.edu/hackfsm/api/detail"
r = requests.get(api_docs_url).content
doc = fromstring(r)

# <codecell>

rows = doc.xpath('//div[@id="content"]/article/div/div/div/table[1]//tr')
headers = [col.text_content().strip() for col in rows[0].findall('td')]
headers

# <codecell>

fields = []

for row in rows[1:]:
    field = [col.text_content().strip() for col in row.findall('td')]
    fields.append(field)
    
fsmfields = OrderedDict(fields)
fsmfields.keys()

# <headingcell level=1>

# Study all the records

# <codecell>

fsm = FSM(q="*",fl=",".join(fsmfields.keys()))

# <codecell>

len(fsm)

# <codecell>

df = DataFrame(list(fsm))

# <codecell>

len(df)

# <codecell>

df.head()

# <codecell>

# TEI URIs

len(list(df[~df.fsmTeiUrl.isnull()].fsmTeiUrl.apply(lambda a: a[0])))

# <codecell>

# null dates

len(df[df.fsmDateCreated.isnull()])

# <codecell>

# non-null image URLs
len(df[~df.fsmImageUrl.isnull()])

# <codecell>

df[~df.fsmImageUrl.isnull()].id

# <codecell>

# distribution of number of image URLs

df[~df.fsmImageUrl.isnull()].fsmImageUrl.apply(len).value_counts()

# <codecell>

# let's crawl for images

results_images = list(FSM("-fsmTeiUrl:[* TO *]", fl=",".join(fsmfields.keys())))

# <codecell>

len(results_images)

# <codecell>

df_images=DataFrame(results_images)

# <codecell>

df_images[df_images.fsmImageUrl.isnull()]

# <codecell>

# would be interesting to see sizes of images and whether we can get at thumbnails
df_images.fsmImageUrl

# <markdowncell>

# http://content.cdlib.org/ark:/13030/tf1z09n5r1/thumbnail ->
# http://digitalassets.lib.berkeley.edu/fsm/ucb/images/brk00040569b_a.gif
# 
# ![Mario Savio addressing the crowd (thumbnail)](http://content.cdlib.org/ark:/13030/tf1z09n5r1/thumbnail "Mario Savio addressing the crowd.")
# 
# http://content.cdlib.org/ark:/13030/tf1z09n5r1/hi-res.jpg ->
# http://digitalassets.lib.berkeley.edu/fsm/ucb/images/brk00040569b_c.jpg

# <codecell>

urlparse.urlparse("http://digitalassets.lib.berkeley.edu/fsm/ucb/images/brk00040569b_c.jpg").netloc

# <codecell>

df_images.fsmImageUrl

# <codecell>

# calculate hostnames for all image urls

# might be possible to do this all with pandas
netlocs = list(df_images.fsmImageUrl.dropna().apply(lambda urls: set([urlparse.urlparse(url).netloc for url in urls])))
reduce(lambda x,y: x | y, netlocs, set())

# <codecell>

def len2(x):
    try:
        return len(x)
    except:
        return np.nan
    
df_images.fsmImageUrl.apply(len2) == 3

# <codecell>

df_images[df_images.fsmImageUrl.apply(len2) == 3].head()

# <markdowncell>

# ![a](http://sunsite.berkeley.edu/FindingAids/dynaweb/calher/fsm/figures/brk00038887a_a.gif "a")
# ![b](http://sunsite.berkeley.edu/FindingAids/dynaweb/calher/fsm/figures/brk00038887a_b.jpg "b")
# ![a](http://sunsite.berkeley.edu/FindingAids/dynaweb/calher/fsm/figures/brk00038887a_c.jpg "c")

# <codecell>

df_images[df_images.fsmImageUrl.apply(len2) == 4].ix[100].fsmImageUrl

# <codecell>

IMAGES_TEMPLATE = """
<div class="nowrap">
 {% for item in items %}<img title="{{item}}" src="{{item}}"/>{% endfor %}
</div>
"""
    
template = Template(IMAGES_TEMPLATE)
HTML(template.render(items=df_images[df_images.fsmImageUrl.apply(len2) == 4].ix[100].fsmImageUrl )) 

# <headingcell level=1>

# Dates

# <codecell>

len(df[~df.fsmDateCreated.isnull()])

# <codecell>

s = df[~df.fsmDateCreated.isnull()].fsmDateCreated.apply(len)==2 #.astype('datetime64[ns]')

# <codecell>

def first(x):
    try:
        return x[0]
    except:
        return np.nan


df['calc_date'] = pd.to_datetime(df.fsmDateCreated.apply(first), coerce=True)

# <codecell>

df[~df.calc_date.isnull()].sort_index(by='calc_date').calc_date

# <codecell>

pd.to_datetime(df.fsmDateCreated.dropna().apply(lambda s:s[0]).astype('str'), coerce=True).dropna()

# <codecell>

# http://stackoverflow.com/questions/17690738/in-pandas-how-do-i-convert-a-string-of-date-strings-to-datetime-objects-and-put
date_stngs = ('2008-12-20','2008-12-21','2008-12-22','2008-12-23','Nov. 9, 1964', 'junk')
pd.to_datetime(pd.Series(date_stngs),coerce=True)

# <headingcell level=1>

# Types of Resources

# <codecell>

def f(x):
    try:
        return set(x)
    except:
        return set()
    
reduce(lambda x,y: x | y, df.fsmTypeOfResource.apply(f), set())


# <codecell>

#related id

len(df.fsmRelatedIdentifier.dropna())

# <headingcell level=1>

# TEI documents

# <codecell>

df.fsmTeiUrl.dropna()

