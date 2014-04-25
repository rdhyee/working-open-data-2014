# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# I recommend using Folium (see [Day_23_B_folium-ipython.ipynb](Day_23_B_folium-ipython.ipynb)) instead of trying to get Google Maps working in the Notebook for the course.  Should be easier.
# 
# This notebook is a demonstration of plotting airport data we get from the project on airport data.

# <codecell>

# http://nbviewer.ipython.org/gist/bburky/7763555/folium-ipython.ipynb

from IPython.display import HTML
import folium

def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.
    
    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    map._build_map()
    return HTML('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 510px; border: none"></iframe>'.format(srcdoc=map.HTML.replace('"', '&quot;')))

def embed_map(map, path="map.html"):
    """
    Embeds a linked iframe to the map into the IPython notebook.
    
    Note: this method will not capture the source of the map into the notebook.
    This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))

# <codecell>

import json
from itertools import islice

airports = []
# skip first line, which is a header row
for rec in islice(open("../data/airport_data.json"), 1, None):
    airports.append(json.loads(rec))

airports[:2]

# <codecell>

airport_map = folium.Map(location=[40, -99], zoom_start=4)

for airport in islice(airports,None):
    lat =  float(airport['Origin_lat'])
    lon = float(airport['Origin_long'])
    label = str(airport['Origin_airport'])  # don't know why str necessary here
    airport_map.simple_marker([lat,lon],popup=label)

inline_map(airport_map)

# <codecell>


