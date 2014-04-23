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
<script>
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
        .defer(d3.json, "files/data/us.json")
        .defer(d3.tsv, "files/temp/unemployment.tsv", function(d) { rateById.set(d.id, +d.rate); })
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
</script>

# <codecell>

from census_api_utils import (counties, census_labels, diversity, FINAL_LABELS)
r = list(counties(census_labels()))

# <codecell>

from pandas import DataFrame

counties_df = DataFrame(r)
counties_df = diversity(counties_df)
counties_df[FINAL_LABELS].head()

# <codecell>

counties_df['fips_for_map'] = counties_df.apply(lambda s: str(int(s['state']))+s['county'], axis=1)

# <codecell>

df = DataFrame()
df[['id','diversity']] = counties_df[['fips_for_map', 'entropy5']]

# <codecell>

df.to_csv('temp/entropy5.tsv', sep="\t", index=False)

# <codecell>

!head temp/entropy5.tsv

# <codecell>

%%html
<div id="diversity_map" style="height:600px; width:100%"></div>
<script>
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
        .domain([0, 1.0])
        .range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

    var path = d3.geo.path();

    var svg = d3.select('#diversity_map').append("svg")
        .attr("width", width)
        .attr("height", height);

    queue()
        .defer(d3.json, "files/data/us.json")
        .defer(d3.tsv, "files/temp/entropy5.tsv", function(d) { rateById.set(d.id, +d.diversity); })
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
</script>

# <codecell>


