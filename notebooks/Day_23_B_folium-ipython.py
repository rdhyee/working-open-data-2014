# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# A promising route for using leaflet.js maps in the IPython notebook -- use [Folium: Python Data. Leaflet.js Maps. — Folium 0.1.2 documentation](https://folium.readthedocs.org/en/latest/).  Easiest way to install Folium:
# 
#     pip install folium
# 
# This notebook is a tiny modification of http://nbviewer.ipython.org/gist/bburky/7763555/folium-ipython.ipynb.  (See https://gist.github.com/bburky/7763555) Specifically, I host the us_counties_20m_topo.json file on my server.  I confirm that this notebook works in IPython 2.0 

# <codecell>

from IPython.display import HTML
import folium

# <codecell>

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

map = folium.Map(location=[40, -99], zoom_start=4)
map.simple_marker([40.67, -73.94], popup='Add <b>popup</b> text here.')
inline_map(map)

# <codecell>

import pandas as pd

#Grab the geojson from github
#county_geo = r'us_counties_20m_topo.json'
# https://gist.githubusercontent.com/wrobstory/5609959/raw/17e222ecd9e26348f50a04fa484485a0e0f54a58/us_counties_20m_topo.json
county_geo = 'http://mashupguide.net/wwod14/us_counties_20m_topo.json'
county_data = 'https://raw.github.com/wrobstory/folium/master/examples/data/us_county_data.csv'

df = pd.read_csv(county_data, na_values=[' '])
df['FIPS_Code'] = df['FIPS_Code'].astype(str)

def set_id(fips):
    '''Modify FIPS code to match GeoJSON property'''
    if fips == '0':
        return None
    elif len(fips) <= 4:
        return ''.join(['0500000US0', fips])
    else:
        return ''.join(['0500000US', fips])

#Apply set_id, drop NaN
df['GEO_ID'] = df['FIPS_Code'].apply(set_id)
df = df.dropna()

map = folium.Map(location=[40, -99], zoom_start=4)
map.geo_json(geo_path=county_geo, data_out='data2.json', data=df,
               columns=['GEO_ID', 'Unemployment_rate_2011'],
               key_on='feature.id',
               threshold_scale=[0, 5, 7, 9, 11, 13],
               fill_color='YlGnBu', line_opacity=0.3,
               legend_name='Unemployment Rate 2011 (%)',
               topojson='objects.us_counties_20m')

embed_map(map)

# <headingcell level=1>

# Blending folium with interact

# <codecell>

from IPython.html import widgets
from IPython.display import display, Image, HTML, clear_output

# <codecell>

# not the most interesting demo --> but a proof of concept on how we can control map using interact

def plot_map(lat, long, zoom):
    map = folium.Map(location=[lat, long], zoom_start=zoom)
    map.simple_marker([lat, long], popup='lat:{lat} long:{long}'.format(lat=lat,long=long))
    display(inline_map(map))
    
widgets.interact(plot_map, 
                 lat=widgets.FloatSliderWidget(min=-90,max=90,step=0.1,value=0),
                 long=widgets.FloatSliderWidget(min=-180,max=180,step=0.1,value=0),
                 zoom=widgets.IntSliderWidget(min=0,max=20,step=1,value=2))

# <codecell>


