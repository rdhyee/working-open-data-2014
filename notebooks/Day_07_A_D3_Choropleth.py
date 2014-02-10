# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# The goal I set out to do: rewrite the [Choropleth](http://bl.ocks.org/mbostock/4060606) d3.js example to work in the IPython notebook.  For future work: once we are able to reproduce the Choropleth example, then work to feed the map arbitrary county-level data.  
# 
# The first thing I did was to make sure I could get 
# 
#  <http://bl.ocks.org/mbostock/raw/4060606/>
# 
# to work by copying the source to
# 
#  <http://mashupguide.net/wwod14/mbostock_4060606.html>
# 
# and serving `us.json` and `unemployment.tsv` from my server with [CORS enabled](http://enable-cors.org/) for these two files:
# 
#  * <http://mashupguide.net/wwod14/us.json>
#  * <http://mashupguide.net/wwod14/unemployment.tsv>
#  
# With the map working on standalone HTML page, then I turned to embedding the map inside an IPython notebook. That's where it got really interesting!

# <codecell>

# print out the version of IPython used
import IPython
IPython.version_info

# <headingcell level=1>

# Initial unsuccessful attempt at rendering choropleth map in notebook

# <markdowncell>

# It turned out that the hard part of doing the translation to IPython Notebook was figuring out how to load the required JavaScript libraries.  Being an off-and-on JavaScript programmer who is ramping up on the way to writing JavaScript properly in 2014, I was still living in the world of adding a `<script>` to load libraries. The problem of such an approach is the possibility of a lot of name collisions.   I knew that the IPython developers had moved to using [RequireJS](http://requirejs.org/), but I really couldn't figure out how to use it by reading the documentation for RequireJS.  
# 
# It was only when I read [Something wrong with the d3js.org/d3.v3.min.js package - Issue #1693 - mbostock/d3](https://github.com/mbostock/d3/issues/1693), which I found via [d3.js - how to integrate d3 with require.js - Stack Overflow](http://stackoverflow.com/questions/13157704/how-to-integrate-d3-with-require-js#comment32647365_13171592) that I knew what to do.  Here's the very helpful incantion I was looking for:

# <codecell>

%%javascript
// https://github.com/mbostock/d3/issues/1693

// loads d3 using require 

require.config({
  paths: {
    d3: "http://d3js.org/d3.v3.min"
  }
});

// example function on using d3 in callback

require(["d3"], function(d3) {
  console.log(d3.version);
});

# <markdowncell>

# Even though I now know the basics of using `RequireJS` to load an external module in the IPython Notebook, I think it could still be helpful to document what I did while wandering in the wilderness. I spent a lot of studying the [IPython in Depth: d3.js JavaScript example ](http://nbviewer.ipython.org/github/ipython/ipython-in-depth/blob/master/notebooks/03%20-%20Rich%20Display%20System.ipynb#JavaScript) and got parts of it working.  Specifically, I copied and used
# 
#     # fetch d3 from cloudflare
#     Javascript("""$.getScript('//cdnjs.cloudflare.com/ajax/libs/d3/3.2.2/d3.v3.min.js')""")
#     
# to successfully load the `d3` JavaScript object.  I ran into problems, when I tried  
# 
#     $.getScript("//d3js.org/queue.v1.min.js");
#     
# but found to my surprise that I couldn't access the `queue` object.  Indeed, 
# 
#     $.getScript("//d3js.org/d3.v3.js"); 
#     
# didn't seem to load the `d3` object either.
# 
# For a few days, I found what seemed to be a successful work-around:  load what seemed to be the equivalent libraries from the [cdnjs](http://cdnjs.com/).  So I was replacing 
# 
#   * `d3`: <http://d3js.org/d3.v3.min.js>
#   * `queue`: <http://d3js.org/queue.v1.min.js>
#   * `topojson`: <http://d3js.org/topojson.v1.min.js>
#     
# with 
# 
#   * `d3`: <http://cdnjs.cloudflare.com/ajax/libs/d3/3.2.2/d3.v3.min.js>
#   * `queue`: <http://cdnjs.cloudflare.com/ajax/libs/queue-async/1.0.4/queue.min.js>
#   * `topojson`: <http://cdnjs.cloudflare.com/ajax/libs/topojson/1.1.0/topojson.min.js>
# 
# The [result](http://mashupguide.net/wwod14/mbostock_4060606_2.html) was something that half-worked.  SVG was produced but nothing was visible, unless you delete the styling.  *As of this moment (2014.02.10), I've not tracked down the reasons for the discrepancy*.
# 
# At any rate, I now know why the libraries from the d3js.org domain was not loading by doing only a `$.getScript` call. For example, the d3.js library was making use of [AMD · amdjs/amdjs-api Wiki](https://github.com/amdjs/amdjs-api/wiki/AMD) (something I'm just learning now), ostensibly implemented by `RequireJS`, to get itself [loaded in a controlled, modular way](https://github.com/mbostock/d3/blob/657effbeea1d1dd1260893f545361c9599019782/d3.js#L9267).  In contrast, using `$.getScript` on [v 3.2.2 of d3.js](https://github.com/mbostock/d3/blob/v3.2.2/d3.js#L1) results in a `d3` defined a global (window) object, thus one that is available to all cells in the Notebook without any other action.

# <codecell>

%%javascript
// https://github.com/mbostock/d3/issues/1693
require.config({
  paths: {
    d3: "http://d3js.org/d3.v3.min",
    queue: "http://d3js.org/queue.v1.min",
    topojson: "http://d3js.org/topojson.v1.min"
  }
});

require(["d3", "queue", "topojson"], function(d3, queue, topojson) {
  console.log(d3.version);
  console.log(queue.version);
  console.log(topojson.version);
});

# <codecell>

%%html
<style type="text/css">

.counties {
  fill: none;
}

.states {
  fill: none;
  stroke: #fff;
  stroke-linejoin: round;
}

.q0-9 { fill:rgb(247,251,255); }
.q1-9 { fill:rgb(222,235,247); }
.q2-9 { fill:rgb(198,219,239); }
.q3-9 { fill:rgb(158,202,225); }
.q4-9 { fill:rgb(107,174,214); }
.q5-9 { fill:rgb(66,146,198); }
.q6-9 { fill:rgb(33,113,181); }
.q7-9 { fill:rgb(8,81,156); }
.q8-9 { fill:rgb(8,48,107); }

</style>

# <codecell>

%%html
<div id="county_map" style="height:600px; width:100%"></div>

# <codecell>

%%javascript

// https://github.com/mbostock/d3/issues/1693
require.config({
  paths: {
    d3: "http://d3js.org/d3.v3.min",
    queue: "http://d3js.org/queue.v1.min",
    topojson: "http://d3js.org/topojson.v1.min"
  }
});

require(["d3", "queue", "topojson"], function(d3, queue, topojson) {
  console.log(d3.version);
  console.log(queue.version);
  console.log(topojson.version);


    var width = 960,
        height = 500;

    var rateById = d3.map();

    var quantize = d3.scale.quantize()
        .domain([0, .15])
        .range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

    var path = d3.geo.path();

    var svg = d3.select('#county_map').append("svg")
        .attr("width", width)
        .attr("height", height);

    queue()
        .defer(d3.json, "http://mashupguide.net/wwod14/us.json")
        .defer(d3.tsv, "http://mashupguide.net/wwod14/unemployment.tsv", function(d) { rateById.set(d.id, +d.rate); })
        .await(ready);

    function ready(error, us) {
      svg.append("g")
          .attr("class", "counties")
        .selectAll("path")
          .data(topojson.feature(us, us.objects.counties).features)
        .enter().append("path")
          .attr("class", function(d) { return quantize(rateById.get(d.id)); })
          .attr("d", path);

      svg.append("path")
          .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
          .attr("class", "states")
          .attr("d", path);
    }
    
})

# <codecell>


