# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [Open Context: Data Publication for Cultural Heritage and Field
# Research](http://opencontext.org/): "Open Context reviews, edits, and
# publishes archaeological research data and archives data with
# university-backed repositories, including the California Digital
# Library."
# 
# I often think of OpenContext as an examplar – a model from the future:
# academic data archiving done right. Some cool features ([About Open
# Context: Technologies](http://opencontext.org/about/technology)):
# 
# -   use of Atom feeds
# -   JSON
# -   KML
# -   use of [timemap - Javascript library to help use a SIMILE timeline
#     with online maps](https://code.google.com/p/timemap/) to map
#     events/objects in time and space (though I wonder whether this
#     technology has been superceded).
# -   contextualization by making ties to other data services
#     -   putting things on maps
#     -   ties to controlled vocabulary around biologica taxa and
#         archaelogical terminology.
#     -   use of linked open data: Examples?
#     -   would be great to tie in any technology we develop for the
#         visualization of large image collections into OpenContext.
# 
# We want to provide for the long-term citability and availability of this
# data.
# 
# Also contextualization.
# 
# What was the excellent presentation/paper he made to us in WwOD13?
# 
# -   Questions
#     -   What costs of archiving data on OpenContext (How are the costs
#         shared among depositor, OpenContext, CDL, and funding agencies?)
#         I think [About Open Context: Estimate Data Management +
#         Publication Costs](http://opencontext.org/about/estimate) gives
#         some clues.
#     -   What guarantees are made about the data once it's archived at
#         OpenContext and CDL? [About Open
#         Context](http://opencontext.org/about/): "Data safeguarded and
#         preserved though archiving with the University of California's
#         California Digital Library"
#     -   How do you cite data in OpenContext?
#     -   Who is reusing this data? Examples?
#     -   IP rights of images (and other data)? Can we tie to Wikipedia
#         and to Wikimedia Commons? (Some insights in [About Open Context:
#         Intellectual
#         Property](http://opencontext.org/about/intellectual-property)
#         but all the whole range of issues are complex. It seems like
#         there will be varying levels of openness and restriction in
#         OpenContext. I will want to dive in to look at specific
#         examples.)
#         -   For example, I don't see any explicit copyright statement at
#             [Open Context Image Lightbox: (1021 Images
#             Showing)](http://opencontext.org/lightbox/?proj=Asian+Stoneware+Jars)
#             or
#             [http://opencontext.org/sets/.json?proj=Asian+Stoneware+Jars](http://opencontext.org/sets/.json?proj=Asian+Stoneware+Jars)
#     -   Can we bulk download data from OpenContext?
# -   open data in science, specifically archaeology
#     -   OpenContext has an API: [About Open Context: Web Services and
#         APIs](http://opencontext.org/about/services)
# -   [Open Context: Data Publication for Cultural Heritage and Field
#     Research](http://opencontext.org/)
# -   Eric Kansa ([@ekansa](https://twitter.com/ekansa)) is a former I
#     School Adjunct Prof, and we've done work together on open goverment,
#     particularly on the Recovery Act. Eric was recently honored (in
#     2013) by the White House [Open Science Champion of
#     Change](http://www.neh.gov/files/divisions/odh/images/wh_neh_champions.jpg).
# -   possible project ideas
#     -   visualizing the image collections in OpenContext.
#     -   making ties to Encyclopedia of Life
#     -   thinking about challenges of archiving data, reconciling data,
#         aligning metadata to standards.
#     -   I see a "suggested citation" in pages like [Open Context view of
#         Item: Trench
#         6](http://opencontext.org/subjects/E5B52F10-333F-4CB8-C397-7DFAD00A3719).
#         Good idea to embed metadata into page to make Zotero know how to
#         grab citation metadata?
# 
# There are so many possibilities here; we can work iteratively with Eric Kansa to
# develop a good project without having it all figured out upfront.
# 
# Eric has mentioned to me the idea of time span facets.

# <headingcell level=1>

# Studying the UI

# <markdowncell>

# How to reproduce data represented by the map on [Open Context](http://opencontext.org/)?
# 
# How to use the API to get a list of projects?
# 
# http://opencontext.org/sets/.json returns json representation of items, but
# http://opencontext.org/projects/.json doesn't work for getting list of all projects. Answer: 

# <markdowncell>

# # A quick jump into the API of opencontext.org
# 
# Let's use a specific project to focus on:
# 
# * <http://opencontext.org/sets/?proj=Asian+Stoneware+Jars>
# * <http://opencontext.org/lightbox/?proj=Asian+Stoneware+Jars>
# 
# 
# The API documentation: <http://opencontext.org/about/services>

# <markdowncell>

# [Open Context: Data Publication for Cultural Heritage and Field Research](http://opencontext.org/)

# <codecell>

# using an example in the API documentation to confirm that we can get json representation from API

import requests
json_url = "http://opencontext.org/sets/Palestinian+Authority/Tell+en-Nasbeh/.json?proj=Bade+Museum"

r = requests.get(json_url)

# what are the top level keys of response?
r.json().keys()

# <codecell>

# Now let's apply same logic to the Asian Stoneware Jars project

json_url = "http://opencontext.org/sets/.json?proj=Asian+Stoneware+Jars"

request = requests.get(json_url)
request_json = request.json()

results= request_json['results']

# <codecell>

request_json.keys()

# <codecell>

# number of results matches what is on human UI
request_json['numFound']

# <codecell>

# we get back the first page of 10
len(results)

# <codecell>

results[0]

# <codecell>

# list the URLs for the thumbnails
[result.get('thumbIcon') for result in results]

# <codecell>

# do a quick display

from IPython.display import HTML
from jinja2 import Template

CSS = """
<style>
  .wrap img {
    margin-left: 0px;
    margin-right: 0px;
    display: inline-block;
  }
</style>
"""

IMAGES_TEMPLATE = CSS + """
<div class="wrap">
 {% for item in items %}<img title="{{item.label}}" src="{{item.thumbIcon}}"/>{% endfor %}
</div>
"""
    
template = Template(IMAGES_TEMPLATE)
HTML(template.render(items=results)) 

# <headingcell level=1>

# Parsing http://opencontext.org/sets/.json

# <codecell>

import requests
url = "http://opencontext.org/sets/.json"

r = requests.get(url)
r.json().keys()

# <codecell>

r.json()['numFound']

# <codecell>

r.json()['paging']['prev']

# <codecell>

# write a generator for all items in http://opencontext.org/sets/.json

import requests

def opencontext_items():
    
    url = "http://opencontext.org/sets/.json"
    more_items = True
    
    while more_items:
        r = requests.get(url)
        for item in r.json()['results']:
            yield item
    
        url = r.json()['paging']['next']
        if not url:
            more_items = False
                       

# <codecell>

from itertools import islice
results = list(islice(opencontext_items(), 25))
HTML(template.render(items=results)) 

# <headingcell level=1>

# Parsing http://opencontext.org/projects/.atom

# <codecell>

import requests
import lxml
from lxml import etree

url = "http://opencontext.org/projects/.atom"
r = requests.get(url)

# <codecell>

doc = etree.fromstring(r.content)
doc

# <codecell>

# get list of titles

project_titles = [e.find('{http://www.w3.org/2005/Atom}title').text for e in doc.findall('{http://www.w3.org/2005/Atom}entry')]
for (i, title) in enumerate(project_titles):
    print i+1, title

