# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Let's try out [MPLD3: Bringing Matplotlib to the Browser](http://mpld3.github.io/index.html), which shows tons of promise for extending the reach of `matplotlib` into the browser:
# 
# <blockquote>
# The mpld3 project brings together Matplotlib, the popular Python-based graphing library, and D3js, the popular Javascript library for creating data-driven web pages. The result is a simple API for exporting your matplotlib graphics to HTML code which can be used within the browser, within standard web pages, blogs, or tools such as the IPython notebook.
# </blockquote>
# 
#  
# To install `mpld3`, you can do a 
# 
#     pip install mpld3
#     
# or follow the instructions at [jakevdp/mpld3](https://github.com/jakevdp/mpld3) (essentially, clone the repository and run `make install`)

# <codecell>

%matplotlib inline

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

# <codecell>

from mpld3 import enable_notebook
from mpld3 import plugins
enable_notebook()

# <codecell>

# try to import seaborn

try:
    import seaborn as sns
except Exception as e:
    print "Could not import seaborn", e

# <codecell>

# Scatter points
fig, ax = plt.subplots()
np.random.seed(0)
x, y = np.random.normal(0, 1, (2, 200))
color = np.random.random(200)
size = 500 * np.random.random(200)

ax.scatter(x, y, c=color, s=size, alpha=0.3)

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_title('Matplotlib Plot Rendered in D3!', size=14)

ax.grid(color='lightgray', alpha=0.7)

# <codecell>

fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
N = 100

scatter = ax.scatter(np.random.normal(size=N),
                     np.random.normal(size=N),
                     c=np.random.random(size=N),
                     s = 1000 * np.random.random(size=N),
                     alpha=0.3,
                     cmap=plt.cm.jet)
ax.grid(color='white', linestyle='solid')

ax.set_title("Scatter Plot (with tooltips!)", size=20)

labels = ['point {0}'.format(i + 1) for i in range(N)]
tooltip = plugins.PointLabelTooltip(scatter, labels=labels)
plugins.connect(fig, tooltip)

# <codecell>


