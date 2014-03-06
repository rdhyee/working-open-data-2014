% Day 13:  Baby Names II and mpld3
% Raymond Yee 
% March 4, 2014 (<http://is.gd/wwod1413>)

# Goals Today

* Focus on working with baby names and learning `mpld3`

# Preparing for midterm

The focus for the next two weeks is on preparing for the midterm.  I'm working on developing some quizzes to help you in that regard.

# Baby Names

* Before you use [Day_13_C_Baby_Names_MF_Completed.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_C_Baby_Names_MF_Completed.ipynb),
try the approach in [Day_13_B_Baby_Names_MF_Starter.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb)

# mpld3

* [Day_13_A_mpl3d.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_A_mpl3d.ipynb)
* [MPLD3: Bringing Matplotlib to the Browser](http://mpld3.github.io/index.html) and 
[jakevdp/mpld3](https://github.com/jakevdp/mpld3)

background:

[A D3 Viewer for Matplotlib Visualizations](http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/) and [Matplotlib Tutorial ? mpl-tutorial 0.1 documentation](http://jakevdp.github.io/mpl_tutorial/)
[D3 Plugins: Truly Interactive Matplotlib In Your Browser](http://jakevdp.github.io/blog/2014/01/10/d3-plugins-truly-interactive/)

Jake VandePlas' tutorials are great:

* [Matplotlib Tutorial - Jake VanderPlas on Vimeo](https://vimeo.com/53057312) (SciPy 2012),
companion website: [Matplotlib Tutorial - mpl-tutorial 0.1 documentation](http://jakevdp.github.io/mpl_tutorial/),
and github repo: [jakevdp/mpl_tutorial](https://github.com/jakevdp/mpl_tutorial)

* [Creating Interactive Applications in Matplotlib on Vimeo](https://vimeo.com/63260224) (PyData 2013) and [jakevdp/matplotlib_pydata2013](https://github.com/jakevdp/matplotlib_pydata2013)

# use matplotlib magic

I've been using

    %pylab inline
    
or

    %pylab --no-import-all inline
    
We should instead use:

    %matplotlib inline
    
to get matplotlib plots to show up inline in the IPython notebook .  See [nbviewer.ipython.org/github/ipython/ipython/blob/master/examples/notebooks/Part 3 - Plotting with Matplotlib.ipynb](http://nbviewer.ipython.org/github/ipython/ipython/blob/master/examples/notebooks/Part%203%20-%20Plotting%20with%20Matplotlib.ipynb)

  
# Assignments / Homework

Assignment in [nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_13_B_Baby_Names_MF_Starter.ipynb):

> Submit a notebook that describes what you've learned about the nature of
ambigendered names in the baby names database. (Due date: <s>Monday, March 10</s> Wed, March 12 at
11:5pm --> bCourses assignment) I'm interested in seeing what you do
with the data set in this regard. At the minimum, show that you are able to run
Day_13_C_Baby_Names_MF_Completed. Be creative and have fun.

