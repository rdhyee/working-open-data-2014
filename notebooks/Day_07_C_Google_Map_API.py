# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# https://developers.google.com/maps/ specifically [Google Maps JavaScript API v3 — Google Developers](https://developers.google.com/maps/documentation/javascript/)
# 
# Go to [Getting Started - Google Maps JavaScript API v3 — Google Developers](https://developers.google.com/maps/documentation/javascript/tutorial)
# 
# How to read in from a local file -- use script?

# <codecell>

from IPython.core.display import HTML, Javascript

# <codecell>

# load the Google Maps API library
# TO DO:  make it easy to add API key

def gmap_init():
    js = """
window.gmap_initialize = function() {};
$.getScript('https://maps.googleapis.com/maps/api/js?v=3&sensor=false&callback=gmap_initialize');
"""
    return Javascript(data=js)

gmap_init()

# <codecell>

%%html
<style type="text/css">
  .map-canvas { height: 300px; }
</style

# <codecell>

# generate a random id

import uuid
div_id = 'i' + str(uuid.uuid4())

html = """<div id="%s" class="map-canvas"/>""" % (div_id)

js = """
<script type="text/Javascript">
  (function(){
    var mapOptions = {
        zoom: 8,
        center: new google.maps.LatLng(-34.397, 150.644)
      };

    var map = new google.maps.Map(document.getElementById('%s'),
          mapOptions);
  })();  
</script>
""" % (div_id)

HTML(html+js)

# <codecell>

import uuid

def gmap(lat=37.8717,long=-122.2728,zoom=8):

    div_id = 'i' + str(uuid.uuid4())

    html = """<div id="%s" class="map-canvas"/>""" % (div_id)

    js = """
    <script type="text/Javascript">
      (function(){
        var mapOptions = {
            zoom: %s,
            center: new google.maps.LatLng(%s, %s)
          };

        var map = new google.maps.Map(document.getElementById('%s'),
              mapOptions);
      })();  
    </script>
    """ % (zoom, lat,long, div_id)

    return HTML(html+js)

# <codecell>

import jinja2

TEMPLATE = """{{greeting}}, {{name}}"""

my_template = jinja2.Template(TEMPLATE)
my_template.render(greeting="hello", name="RY")

# <markdowncell>

# Can we ask google for list of instantiated maps?

# <headingcell level=1>

# Plotting markers

# <markdowncell>

# https://developers.google.com/maps/documentation/javascript/markers
# 
#     var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
#     var mapOptions = {
#       zoom: 4,
#       center: myLatlng
#     }
#     var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
# 
#     // To add the marker to the map, use the 'map' property
#     var marker = new google.maps.Marker({
#         position: myLatlng,
#         map: map,
#         title:"Hello World!"
#     });

# <codecell>

%%html
<div id="markers" class="map-canvas"/>

# <codecell>

%%javascript

var myLatlng = new google.maps.LatLng(37.8717,-122.2728);

var mapOptions = {
  zoom: 8,
  center: myLatlng
};

var map = new google.maps.Map(document.getElementById('markers'),
  mapOptions);

// To add the marker to the map, use the 'map' property
var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title:"Berkeley"
});

# <headingcell level=2>

# Drawing Circles on Map

# <markdowncell>

# https://developers.google.com/maps/documentation/javascript/examples/circle-simple
# 
#     // This example creates circles on the map, representing
#     // populations in the United States.
# 
#     // First, create an object containing LatLng and population for each city.
#     var citymap = {};
#     citymap['chicago'] = {
#       center: new google.maps.LatLng(41.878113, -87.629798),
#       population: 2842518
#     };
#     citymap['newyork'] = {
#       center: new google.maps.LatLng(40.714352, -74.005973),
#       population: 8143197
#     };
#     citymap['losangeles'] = {
#       center: new google.maps.LatLng(34.052234, -118.243684),
#       population: 3844829
#     };
#     var cityCircle;
# 
#     function initialize() {
#       // Create the map.
#       var mapOptions = {
#         zoom: 4,
#         center: new google.maps.LatLng(37.09024, -95.712891),
#         mapTypeId: google.maps.MapTypeId.TERRAIN
#       };
# 
#       var map = new google.maps.Map(document.getElementById('map-canvas'),
#           mapOptions);
# 
#       // Construct the circle for each value in citymap.
#       // Note: We scale the population by a factor of 20.
#       for (var city in citymap) {
#         var populationOptions = {
#           strokeColor: '#FF0000',
#           strokeOpacity: 0.8,
#           strokeWeight: 2,
#           fillColor: '#FF0000',
#           fillOpacity: 0.35,
#           map: map,
#           center: citymap[city].center,
#           radius: citymap[city].population / 20
#         };
#         // Add the circle for this city to the map.
#         cityCircle = new google.maps.Circle(populationOptions);
#       }
#     }
# 
#     google.maps.event.addDomListener(window, 'load', initialize);

# <codecell>

%%html
<div id="circles" class="map-canvas"/>

# <codecell>

%%javascript

// This example creates circles on the map, representing
// populations in the United States.

// First, create an object containing LatLng and population for each city.
var citymap = {};
citymap['chicago'] = {
  center: new google.maps.LatLng(41.878113, -87.629798),
  population: 2842518
};
citymap['newyork'] = {
  center: new google.maps.LatLng(40.714352, -74.005973),
  population: 8143197
};
citymap['losangeles'] = {
  center: new google.maps.LatLng(34.052234, -118.243684),
  population: 3844829
};
var cityCircle;


var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(37.09024, -95.712891),
    mapTypeId: google.maps.MapTypeId.TERRAIN
};


  var map = new google.maps.Map(document.getElementById('circles'),
      mapOptions);

  // Construct the circle for each value in citymap.
  // Note: We scale the population by a factor of 20.
  for (var city in citymap) {
    var populationOptions = {
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      center: citymap[city].center,
      radius: citymap[city].population / 20
    };
    // Add the circle for this city to the map.
    cityCircle = new google.maps.Circle(populationOptions);
  }


# <markdowncell>

# [[IPython-User] using Google Charts in IPython](http://lists.ipython.scipy.org/pipermail/ipython-user/2013-May/012694.html):
# 
# > google.load blanks the page unless you give it a
# callback <http://stackoverflow.com/questions/9519673/why-does-google-load-cause-my-page-to-go-blank>
# .
# 
# Also: [javascript - Google Maps API v3 - TypeError: Result of expression 'google.maps.LatLng' undefined] is not a constructor - Stack Overflow](http://stackoverflow.com/questions/6577404/google-maps-api-v3-typeerror-result-of-expression-google-maps-latlng-undef/8361021#8361021)

# <codecell>


