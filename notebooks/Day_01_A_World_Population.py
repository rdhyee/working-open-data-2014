# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Goals

# <markdowncell>

# Some goals for this exercise:
# 
# * to reacquaint ourselves with Python
# * to start learning how to use a particular IPython notebook environment, one which is easy to jump right into, namely [Wakari](https://www.wakari.io/)
# * to learn a bit about the international context before diving into the US Census.
# * to get ourselves into looking at the Wikipedia as a data source.
# 
# Thinking about populations of various geographic entities is a good place to start with open data.  We can to work with numbers without necessarily involving complicated mathematics.  Just addition if we're lucky. We can also think about geographical locations.  We can build out from our initial explorations in a systematica manner.

# <headingcell level=1>

# Things to Think About

# <markdowncell>

# Off the top of your head:
#     
#     * What do you think is the current world population?
#     * How many countries are there?
#     * How many people are there in the USA?  Canada?  Mexico?  Your favorite country?
#     * What is the minimum number of countries to add up to 50% of the world's population?  How about 90%?
#     
# Now go answer these questions looking on the web.  Find some a source or two or three.

# <headingcell level=1>

# Data Source for Populations

# <markdowncell>

# Two open sources we'll consider:
# 
# * [CIA World Factbook: Country Comparison Population](https://www.cia.gov/library/publications/the-world-factbook/rankorder/2119rank.html) (see also [The World Factbook: ABOUT :: COPYRIGHT AND CONTRIBUTORS](https://www.cia.gov/library/publications/the-world-factbook/docs/contributor_copyright.html))
# * [List of countries by population (United Nations) - Wikipedia, the free encyclopedia](https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)) (see also [Wikipedia:Reusing Wikipedia content - Wikipedia, the free encyclopedia](https://en.wikipedia.org/wiki/Wikipedia:Reusing_Wikipedia_content)) -- btw, not the same as [List of countries by population - Wikipedia, the free encyclopedia](https://en.wikipedia.org/wiki/List_of_countries_by_population).
# 
# We will study how to parse these data sources in a later exercise, but for this exercise, the data sets have been parsed into [JSON format](https://en.wikipedia.org/wiki/JSON), which is easily loadable in many languages, including Python using the [json Python standard library](http://docs.python.org/2/library/json.html).  We'll also use [requests](http://docs.python-requests.org/en/latest/).
# 
# Let's look first at the Wikipedia source.

# <codecell>

# https://gist.github.com/rdhyee/8511607/raw/f16257434352916574473e63612fcea55a0c1b1c/population_of_countries.json
# scraping of https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=590438477

# read population in
import json
import requests

pop_json_url = "https://gist.github.com/rdhyee/8511607/raw/f16257434352916574473e63612fcea55a0c1b1c/population_of_countries.json"
pop_list= requests.get(pop_json_url).json()
pop_list

# <headingcell level=1>

# EXERCISES

# <markdowncell>

# Show how to calculate the total population according to the list in the Wikipedia. (Answer: 7,162,119,434)

# <codecell>


# <markdowncell>

# Calculate the total population of 196 entities that have a numeric rank. (Answer: 7,145,999,288) BTW, are those entities actually countries?

# <codecell>


# <markdowncell>

# Calculate the total population according to [The World Factbook: Country Comparison Population](https://www.cia.gov/library/publications/the-world-factbook/rankorder/2119rank.html) (See https://gist.github.com/rdhyee/8530164).

# <codecell>


# <headingcell level=1>

# CHALLENGE EXERCISE

# <markdowncell>

# Now for something more interesting. I'd like for us to get a feel of what it'd be like to pick a person completely at random from the world's population.  Say, if you were picking 5 people -- where might these people be from?  Of course, you won't be surprised to pick someone from China or India since those countries are so populous.  But how likely will it be for someone from the USA to show up?
# 
# To the end of answering this question, start thinking about writing a Python generator that will return the name of a country in which the probability of that country being returned is the proportion of the world's population represented by that country.   
# 
# Work with your neighbors -- we'll come back to this problem in detail in class on Thursday.

# <markdowncell>

#                                                                                                                                                                                                                                                                   

