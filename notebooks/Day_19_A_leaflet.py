# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [Leaflet - a JavaScript library for mobile-friendly maps](http://leafletjs.com/)

# <markdowncell>

# I have a question:  can you use requirejs to deal with non-AMD JavaScript files?  According to http://stackoverflow.com/a/14603398/7782: maybe.  Seems to be affirmed by [Requirement #9:  Load any script](http://requirejs.org/docs/requirements.html#9).

# <codecell>

from IPython.display import HTML, display, clear_output
import uuid

import jinja2
from jinja2 import Template

from settings import LEAFLET_KEY

CSS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css"
LEAFLET_JS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet"

div_id = 'i' + str(uuid.uuid4())

JS = u"""
<script type="text/javascript">


    // load css if it's not already there: http://stackoverflow.com/a/4724676/7782
    function loadcss(url) {
        if (!$("link[href='" + url + "']").length)
            $('<link href="' + url + '" rel="stylesheet">').appendTo("head");
    }
    
    function add_map(id, map) {


        if ('_my_maps' in window && window._my_maps !== undefined) {
            window._my_maps[id] = map;
        } else {
            window._my_maps = {};
            window._my_maps[id] = map;
        }
    }


    require.config({
      paths: {
        leaflet: "{{leaflet_js_url}}"
      }
    });

    
    loadcss("{{css_url}}");

    require(["leaflet"], function(leaflet) {

        var map = L.map('{{div_id}}').setView([{{lat}}, {{long}}], {{zoom}});

        L.tileLayer('http://{s}.tile.cloudmade.com/{{leaflet_api_key}}/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        }).addTo(map);

    });

</script>
"""

# demonstrates interference from .rendered_html CSS

CSS = """
<style type="text/css">
    #{{div_id}} { height: {{height}}px; }
</style>
"""

HTML_ = """
<div id="{{div_id}}"></div>
"""

template = Template(CSS + JS + HTML_)
HTML(template.render(leaflet_js_url=LEAFLET_JS_URL,
                      css_url = CSS_URL,
                      leaflet_api_key = LEAFLET_KEY,
                      lat=37.8717,
                      long=-122.2728,
                      zoom=12,
                      div_id=div_id,
                      height=200
                      ))


# <codecell>

# will normalize.css fix this problem?

from IPython.display import HTML, display, clear_output
import uuid

import jinja2
from jinja2 import Template

from settings import LEAFLET_KEY

CSS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css"
LEAFLET_JS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet"

div_id = 'i' + str(uuid.uuid4())

JS = u"""
<script type="text/javascript">


    // load css if it's not already there: http://stackoverflow.com/a/4724676/7782
    function loadcss(url) {
        if (!$("link[href='" + url + "']").length)
            $('<link href="' + url + '" rel="stylesheet">').appendTo("head");
    }

    function add_map(id, map) {

        if ('_my_maps' in window && window._my_maps !== undefined) {
            window._my_maps[id] = map;
        } else {
            window._my_maps = {};
            window._my_maps[id] = map;
        }
    }

    require.config({
      paths: {
        leaflet: "{{leaflet_js_url}}"
      }
    });

    
    loadcss("{{css_url}}");
    loadcss("http://yui.yahooapis.com/3.15.0/build/cssnormalize-context/cssnormalize-context-min.css");
 

    require(["leaflet"], function(leaflet) {

        console.log(L.version);
        var map = L.map('{{div_id}}').setView([{{lat}}, {{long}}], {{zoom}});
        map.invalidateSize();

        L.tileLayer('http://{s}.tile.cloudmade.com/{{leaflet_api_key}}/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        }).addTo(map);

    });

</script>
"""

# demonstrates interference from .rendered_html CSS

CSS = """
<style type="text/css">
    #{{div_id}} { height: {{height}}px; }
</style>
"""

HTML_ = """
<div id="{{div_id}}" class="yui3-normalized"></div>
"""

template = Template(CSS + JS + HTML_)
HTML(template.render(leaflet_js_url=LEAFLET_JS_URL,
                      css_url = CSS_URL,
                      leaflet_api_key = LEAFLET_KEY,
                      lat=37.8717,
                      long=-122.2728,
                      zoom=12,
                      div_id=div_id,
                      height=200
                      ))


# <codecell>

import uuid
from functools import partial

from IPython.display import HTML, display, clear_output

import jinja2
from jinja2 import Template

from settings import LEAFLET_KEY

CSS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css"
LEAFLET_JS_URL = "http://cdn.leafletjs.com/leaflet-0.7.2/leaflet"


JS = u"""
<script type="text/javascript">

    // load css if it's not already there: http://stackoverflow.com/a/4724676/7782
    function loadcss(url) {
        if (!$("link[href='" + url + "']").length)
            $('<link href="' + url + '" rel="stylesheet">').appendTo("head");
            
    }
    
    function add_map(id, map) {

        if ('_my_maps' in window && window._my_maps !== undefined) {
            window._my_maps[id] = map;
        } else {
            window._my_maps = {};
            window._my_maps[id] = map;
        }
    }

    
    require.config({
      paths: {
        leaflet: "{{leaflet_js_url}}"
      }
    });
           
    loadcss("{{css_url}}");
    loadcss("http://yui.yahooapis.com/3.15.0/build/cssnormalize-context/cssnormalize-context-min.css");

    require(["leaflet"], function(leaflet) {

        var map = L.map('{{div_id}}').setView([{{lat}}, {{long}}], {{zoom}});
        
        add_map("{{div_id}}", map);

        L.tileLayer('http://{s}.tile.cloudmade.com/{{leaflet_api_key}}/997/256/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
            maxZoom: 18
        }).addTo(map);
        
        console.log(map instanceof L.Map);

    });

</script>
"""


CSS = """
<style type="text/css">
    #{{div_id}} { height: {{height}}px; }
    #{{div_id}} *+img{margin-top:0em}
</style>
"""

HTML_ = """
<div id="{{div_id}}"  class="yui3-normalized"></div>
"""

template = Template(CSS + JS + HTML_)


def leaflet(leaflet_api_key, lat, long, zoom, height):
    
    div_id = 'i' + str(uuid.uuid4())
    
    display(HTML(template.render(leaflet_js_url=LEAFLET_JS_URL,
                      css_url = CSS_URL,
                      leaflet_api_key = leaflet_api_key,
                      lat=lat,
                      long=long,
                      zoom=zoom,
                      div_id=div_id,
                      height=height
                      )))


# <codecell>

leaflet(leaflet_api_key=LEAFLET_KEY, lat=37.8717, long=-122.2728, zoom=9, height=300)

# <codecell>

%%javascript
require(["leaflet"], function(leaflet) {

var map = window._my_maps['i3c9fe247-096f-4df2-b6d7-291bb6d3b0e1']
console.log(map.getCenter());
    
});

# <codecell>

from IPython.html import widgets
from IPython.html.widgets import interact, fixed

zoom_widget = widgets.IntSliderWidget(min=1, max=18, step=1)
zoom_widget.value = 12

interact (leaflet, leaflet_api_key=fixed(LEAFLET_KEY), lat=fixed(37.8717), 
                  long=fixed(-122.2728),height=fixed(500), zoom=zoom_widget)

# <headingcell level=1>

# Doing more with a map

# <codecell>

%%javascript
console.log(IPython.notebook.get_cells());

# <codecell>

%%javascript
require(["leaflet"], function(leaflet) {

    console.log(L.version);

    // attempt to find maps in the window object -- not successful.
    var mapObjects = [];
    for(var key in window) {
      var value = window[key];
      if (value instanceof L.Map) {
        // foo instance found in the global scope, named by key
        mapObjects.push(value)
      }
    }

    console.log(mapObjects);
    
});

# <codecell>


