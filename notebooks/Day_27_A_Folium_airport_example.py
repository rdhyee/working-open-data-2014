# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# I recommend using Folium (see [Day_23_B_folium-ipython.ipynb](Day_23_B_folium-ipython.ipynb)) instead of trying to get Google Maps working in the Notebook for the course.  Should be easier.
# 
# This notebook is a demonstration of plotting airport data we get from the project on airport data.
# 
# **Note**:  As of 2014.04.26, to get the lines working, you need to be running the master branch of folium.  To install it, you might need to uninstall folium first:
# 
#     pip uninstall folium
#     
# and then install the master branch:
# 
#     pip install git+git://github.com/wrobstory/folium.git

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

# <headingcell level=1>

# Lines

# <codecell>

# https://github.com/wrobstory/folium/blob/master/examples/line_example.py

coordinates = [
    [  42.3581    ,  -71.0636    ],
    [  42.82995815,  -74.78991444],
    [  43.17929819,  -78.56603306],
    [  43.40320216,  -82.37774519],
    [  43.49975489,  -86.20965845],
    [  43.46811941,  -90.04569087],
    [  43.30857071,  -93.86961818],
    [  43.02248456,  -97.66563267],
    [  42.61228259, -101.41886832],
    [  42.08133868, -105.11585198],
    [  41.4338549 , -108.74485069],
    [  40.67471747, -112.29609954],
    [  39.8093434 , -115.76190821],
    [  38.84352776, -119.13665678],
    [  37.7833    , -122.4167    ]]


# Create the map and add the line
m = folium.Map(location=[41.9, -97.3], zoom_start=4)
m.line(coordinates, line_color='#FF0000', line_weight=5)
inline_map(m)

# <codecell>


