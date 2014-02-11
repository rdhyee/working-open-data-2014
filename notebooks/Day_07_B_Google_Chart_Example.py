# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Goal:  get a simple Google Chart w/ world map into the Notebook.
# 
# This might not prove to be the best way to do things, but the goal is to get a start.

# <codecell>

%%javascript
$.getScript('//www.google.com/jsapi');

# <codecell>

%%html
<div id="chart_div"></div>

# <markdowncell>

# [[IPython-User] using Google Charts in IPython](http://lists.ipython.scipy.org/pipermail/ipython-user/2013-May/012694.html):
# 
# > google.load blanks the page unless you give it a
# callback<http://stackoverflow.com/questions/9519673/why-does-google-load-cause-my-page-to-go-blank>
# .

# <codecell>

%%javascript

var drawRegionsMap = function() {
    var data = google.visualization.arrayToDataTable([
      ['Country', 'Popularity'],
      ['Germany', 200],
      ['United States', 300],
      ['Brazil', 400],
      ['Canada', 500],
      ['France', 600],
      ['RU', 700]
    ]);
    var options = {};

    var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

// google.setOnLoadCallback(drawRegionsMap);
google.load('visualization', '1', {'packages': ['geochart'],
                                   'callback': drawRegionsMap});


