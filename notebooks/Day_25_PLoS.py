# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
from pandas import DataFrame, Series, Index
import numpy as np
import matplotlib.pyplot as plt

# <markdowncell>

# Hint from http://api.plos.org/search-examples/plos_search.py about how to get only articles in search:
# 
#     query['fq'] = quote('doc_type:full AND !article_type_facet:"Issue Image"') #search only for articles

# <markdowncell>

# We need to be mindful of the API rate limit -- but PLoS has 
# 
# http://api.plos.org/solr/faq/#solr_api_recommended_usage:
# 
# > Please limit your API requests to 7200 requests a day, 300 per hour, 10 per minute and allow 5 seconds for your search to return results. If you exceed this threshold, we will lock out your IP address. If you’re a high-volume user of the PLOS Search API and need more API requests a day, please contact us at api@plos.org to discuss your options. We currently limit API users to no more than five concurrent connections from a single IP address.
# 
# [...]
# 
# > PLOS Search API requests: Please do not send requests that return more than 100 rows. That’s a lot of data for our network to push all at once and it may take some time to return the result set. If you are getting back a result set that bigger than 100+ rows, then you likely need to change your query to return a smaller result set or set a limit on the records returned and page through the results.

# <codecell>

import settings
import requests
import urllib

# http://api.plos.org/search-examples/plos_search.py
#  query['fq'] = quote('doc_type:full AND !article_type_facet:"Issue Image"') 
#search only for articles

def plos_search(q,start=0,rows=100,fl=None, extras=None):

    BASE_URL = 'http://api.plos.org/search'
    DEFAULT_FL = ('abstract','article_type','author_display',
                  'eissn','id','journal','publication_date',
                  'score','title_display')
    
    # fl indicates fields to return
    # http://wiki.apache.org/solr/CommonQueryParameters#fl
    
    if fl is None:
        fl_ = ",".join(DEFAULT_FL)
    else:
        fl_ = ",".join(fl)
        
    query = {'q':q,
             'start':start,
             'rows':rows,
             'api_key':settings.PLOS_KEY,
             'wt':'json',
             'fl':fl_,
             'fq': 'doc_type:full AND !article_type_facet:"Issue Image"'}
    
    if extras is not None:
        query.update(extras)
        
    query_url = BASE_URL + "?" +urllib.urlencode(query)
    
    r = requests.get(query_url)
    return r

# <codecell>

r = plos_search(q='subject:"biotechnology"')

# <codecell>

r.json()['response']['numFound']

# <codecell>

docs = r.json()['response']['docs']

# <codecell>

df = DataFrame(docs)
df.head()

# <markdowncell>

# What type of parameters in search?
# 
# parameters: http://api.plos.org/solr/search-fields/
# 
# Can try out: http://www.plosone.org/search/advanced?noSearchFlag=true&query=&filterJournals=PLoSONE
# 
# How to ask for more metadata -- like subject areas?  
# http://www.plosone.org/search/advanced?unformattedQuery=subject%3A%22Body+mass+index%22 
# 
# https://groups.google.com/forum/#!searchin/plos-api-developers/subject/plos-api-developers/BqECTQkvRTI/r9v6oCAAOPoJ

# <codecell>

# get subjects of a given article
# http://api.plos.org/search?q=id:%2210.1371/journal.pbio.0050082%22&fl=id,subject,subject_level_1&api_key=[YOUR_API_KEY]

r = plos_search(q="10.1371/journal.pone.0039504",
            fl=('id','subject','subject_level'))

# <codecell>

r.json()

# <codecell>

# There is also a list of all the top-level subject areas and their article counts: 
# http://api.plos.org/search/?q=*:*&fq=doc_type:full&rows=0&facet.field=subject_facet&facet.mincount=1

# this doesn't seem to work for me:
# https://groups.google.com/forum/#!searchin/plos-api-developers/subject/plos-api-developers/BqECTQkvRTI/r9v6oCAAOPoJ

r = plos_search(q="*.*",
                extras={'fq':'doc_type:full',
                    'facet.field':'subject_facet',
                    'facet.mincount':1
                    })
r

# <codecell>

r.json()

# <markdowncell>

# for simplicity, try to limit to PLoS One to start with

# <codecell>

# compute links back to journal, XML document

# <markdowncell>

# Example article:
# 
# http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0039504
# 
# id: 10.1371/journal.pone.0039504
# XML: http://www.plosone.org/article/fetchObjectAttachment.action?uri=info%3Adoi%2F10.1371%2Fjournal.pone.0039504&representation=XML

# <codecell>

# get all articles

r = plos_search(q="*:*")
r

# <codecell>

r.json()['response']['numFound']

# <codecell>


