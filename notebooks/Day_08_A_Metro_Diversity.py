# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Exercise

# <markdowncell>

# In this exercise, reproduce some of the findings from [What Makes Houston the Next Great American City? | Travel | Smithsonian](http://www.smithsonianmag.com/travel/what-makes-houston-the-next-great-american-city-4870584/), specifically the calculation represented in
# 
# ![Alt text](http://thumbs.media.smithsonianmag.com//filer/Houston-diversity-3.jpg__600x0_q85_upscale.jpg "Optional title")
# 
# whose caption is
# 
# <blockquote>To assess the parity of the four major U.S. ethnic and racial groups, Rice University researchers used a scale called the Entropy Index. It ranges from 0 (a population has just one group) to 1 (all groups are equivalent). Edging New York for the most balanced diversity, Houston had an Entropy Index of 0.874 (orange bar).</blockquote>
# 
# The research report by *Smithsonian Magazine* is
# [Houston Region Grows More Racially/Ethnically Diverse, With Small Declines in Segregation: A Joint Report Analyzing Census Data from 1990, 2000, and 2010](http://kinder.rice.edu/uploadedFiles/Urban_Research_Center/Media/Houston%20Region%20Grows%20More%20Ethnically%20Diverse%202-13.pdf) by the Kinder Institute for Urban Research & the Hobby Center for the Study of Texas.  
# 
# In the report, you'll find the following quotes:
# 
# <blockquote>How does Houston’s racial/ethnic diversity compare to the racial/ethnic
# diversity of other large metropolitan areas? The Houston metropolitan
# area is the most racially/ethnically diverse.</blockquote>
# 
# ....
# 
# <blockquote>Houston is one of the most racially/ethnically diverse metropolitan
# areas in the nation as well. *It is the most diverse of the 10 largest
# U.S. metropolitan areas.* [emphasis mine] Unlike the other large metropolitan areas, all
# four major racial/ethnic groups have substantial representation in
# Houston with Latinos and Anglos occupying roughly equal shares of the
# population.</blockquote>
# 
# ....
# 
# <blockquote>Houston has the highest entropy score of the 10 largest metropolitan
# areas, 0.874. New York is a close second with a score of 0.872.</blockquote>
# 
# ....
# 
# Your task is:
# 
# 1. Tabulate all the metropolian/micropolitan statistical areas.  Remember that you have to group various entities that show up separately in the Census API but which belong to the same area.  You should find 942 metropolitan/micropolitan statistical areas in the 2010 Census.
# 
# 1. Calculate the normalized Shannon index (`entropy5`) using the categories of White, Black, Hispanic, Asian, and Other as outlined in the [Day_07_G_Calculating_Diversity notebook](http://nbviewer.ipython.org/github/rdhyee/working-open-data-2014/blob/master/notebooks/Day_07_G_Calculating_Diversity.ipynb#Converting-to-Racial-Dot-Map-Categories) 
# 
# 1. Calculate the normalized Shannon index (`entropy4`) by not considering the Other category.  In other words, assume that the the total population is the sum of White, Black, Hispanic, and Asian.
# 
# 1. Figure out how exactly the entropy score was calculated in the report from Rice University. Since you'll find that the entropy score reported matches neither `entropy5` nor `entropy4`, you'll need to play around with the entropy calculation to figure how to use 4 categories to get the score for Houston to come out to "0.874" and that for NYC to be "0.872".  [I **think** I've done so and get 0.873618 and 
# 0.872729 respectively.]
# 
# 1. Add a calculation of the [Gini-Simpson diversity index](https://en.wikipedia.org/wiki/Diversity_index#Gini.E2.80.93Simpson_index) using the five categories of White, Black, Hispanic, Asian, and Other.
# 
# 1. Note where the Bay Area stands in terms of the diversity index.
# 
# For bonus points:
# 
# * make a bar chart in the style used in the Smithsonian Magazine
# 
# Deliverable:
# 
# 1. You will need to upload your notebook to a gist and render the notebook in nbviewer and then enter the nbviewer URL (e.g., http://nbviewer.ipython.org/gist/rdhyee/60b6c0b0aad7fd531938)
# 2. On bCourses, upload the CSV version of your `msas_df`.
# 
# **HAVE FUN: ASK QUESTIONS AND WORK TOGETHER**

# <headingcell level=1>

# Constraints

# <markdowncell>

# Below is testing code to help make sure you are on the right track.  A key assumption made here is that you will end up with a Pandas DataFrame called `msas_df`, indexed by the FIPS code of a metropolitan/micropolitan area (e.g., Houston's code is 26420) and with the the following columns:
# 
# * Total
# * White
# * Black
# * Hispanic
# * Asian
# * Other
# * p_White
# * p_Black
# * p_Hispanic
# * p_Asian
# * p_Other
# * entropy4
# * entropy5
# * entropy_rice
# * gini_simpson
# 
# You should have 942 rows, one for each MSA.  You can compare your results for `entropy5`, `entropy_rice` with mine.

# <codecell>

# FILL IN WITH YOUR CODE














# <codecell>

# Testing code

def to_unicode(vals):
    return [unicode(v) for v in vals]

def test_msas_df(msas_df):

    min_set_of_columns =  set(['Asian','Black','Hispanic', 'Other', 'Total', 'White',
     'entropy4', 'entropy5', 'entropy_rice', 'gini_simpson','p_Asian', 'p_Black',
     'p_Hispanic', 'p_Other','p_White'])  
    
    assert min_set_of_columns & set(msas_df.columns) == min_set_of_columns
    
    # https://www.census.gov/geo/maps-data/data/tallies/national_geo_tallies.html
    # 366 metro areas
    # 576 micropolitan areas
    
    assert len(msas_df) == 942  
    
    # total number of people in metro/micro areas
    
    assert msas_df.Total.sum() == 289261315
    assert msas_df['White'].sum() == 180912856
    assert msas_df['Other'].sum() == 8540181
    
    # list of msas in descendng order by entropy_rice 
    # calculate the top 10 metros by population
    top_10_metros = msas_df.sort_index(by='Total', ascending=False)[:10]
    
    msa_codes_in_top_10_pop_sorted_by_entropy_rice = list(top_10_metros.sort_index(by='entropy_rice', 
                                                ascending=False).index) 
    
    assert to_unicode(msa_codes_in_top_10_pop_sorted_by_entropy_rice)== [u'26420', u'35620', u'47900', u'31100', u'19100', 
        u'33100', u'16980', u'12060', u'37980', u'14460']


    top_10_metro = msas_df.sort_index(by='Total', ascending=False)[:10]
    
    list(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy5'])
    
    np.testing.assert_allclose(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy5'], 
    [0.79628076626851163, 0.80528601550164602, 0.80809418318973791, 0.7980698349711991,
     0.75945930510650161, 0.74913610558765376, 0.73683277781032397, 0.72964862063970914,
     0.64082509648457675, 0.55697288400004963])
    
    np.testing.assert_allclose(top_10_metro.sort_index(by='entropy_rice', ascending=False)['entropy_rice'],
    [0.87361766576115552,
     0.87272877244078051,
     0.85931803868749834,
     0.85508015237749468,
     0.82169723530719896,
     0.81953527301129059,
     0.80589423784325431,
     0.78602596561378812,
     0.68611350427640316,
     0.56978827050565117])

# <codecell>

# you are on the right track if test_msas_df doesn't complain
test_msas_df(msas_df)

# <codecell>

# code to save your dataframe to a CSV
# upload the CSV to bCourses
# uncomment to run
# msas_df.to_csv("msas_2010.csv", encoding="UTF-8")

# <codecell>

# load back the CSV and test again
# df = DataFrame.from_csv("msas_2010.csv", encoding="UTF-8")
# test_msas_df(df)

# <codecell>


