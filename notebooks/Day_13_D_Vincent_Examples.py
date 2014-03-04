# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

!which python

# <codecell>

!pip freeze | grep -i ipython

# <codecell>

!pip show vincent 

# <codecell>

%pylab --no-import-all inline

# <codecell>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas import Series, DataFrame
plt.plot(np.arange(10))

# <codecell>

import vincent
import pandas as pd
import random

#Iterable
list_data = [10, 20, 30, 20, 15, 30, 45]

#Dicts of iterables
cat_1 = ['y1', 'y2', 'y3', 'y4']
index_1 = range(0, 21, 1)
multi_iter1 = {'index': index_1}
for cat in cat_1:
    multi_iter1[cat] = [random.randint(10, 100) for x in index_1]

cat_2 = ['y' + str(x) for x in range(0, 10, 1)]
index_2 = range(1, 21, 1)
multi_iter2 = {'index': index_2}
for cat in cat_2:
    multi_iter2[cat] = [random.randint(10, 100) for x in index_2]

#Pandas
import pandas as pd

farm_1 = {'apples': 10, 'berries': 32, 'squash': 21, 'melons': 13, 'corn': 18}
farm_2 = {'apples': 15, 'berries': 43, 'squash': 17, 'melons': 10, 'corn': 22}
farm_3 = {'apples': 6, 'berries': 24, 'squash': 22, 'melons': 16, 'corn': 30}
farm_4 = {'apples': 12, 'berries': 30, 'squash': 15, 'melons': 9, 'corn': 15}

farm_data = [farm_1, farm_2, farm_3, farm_4]
farm_index = ['Farm 1', 'Farm 2', 'Farm 3', 'Farm 4']
df_farm = pd.DataFrame(farm_data, index=farm_index)

#As DataFrames
index_3 = multi_iter2.pop('index')
df_1 = pd.DataFrame(multi_iter2, index=index_3)
df_1 = df_1.reindex(columns=sorted(df_1.columns))

cat_4 = ['Metric_' + str(x) for x in range(0, 10, 1)]
index_4 = ['Data 1', 'Data 2', 'Data 3', 'Data 4']
data_3 = {}
for cat in cat_4:
    data_3[cat] = [random.randint(10, 100) for x in index_4]
df_2 = pd.DataFrame(data_3, index=index_4)

import pandas.io.data as web
all_data = {}
for ticker in ['AAPL', 'GOOG', 'IBM', 'YHOO', 'MSFT']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2010', '1/1/2013')
price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.items()})

import collections
text = 'The sun did not shine It was too wet to play So we sat in the house All that cold cold wet day sat there with Sally we sat there we two And I said How I wish we had something to do Too wet to go out and too cold to play ball So we sat in the house We did nothing at all So all we could do was to Sit Sit Sit Sit And we did not like it Not one little bit And then something went BUMP How that bump made us jump We looked Then we saw him step in on the mat We looked And we saw him The Cat in the Hat And he said to us Why do you sit there like that I know it is wet And the sun is not sunny But we can have lots of good fun that is funny I know some good games we could play Said the cat I know some new tricks Said the Cat in the Hat A lot of good tricks I will show them to you Your mother Will not mind at all if I do Then Sally and I Did not know what to say Our mother was out of the house For the day But the fish said No No Make that cat go away Tell that Cat in the Hat you do NOT want to play He should not be here He should not be about He should not be here When your mother is out Now Now Have no fear Have no fear said the cat My tricks are not bad Said the Cat in the Hat Why we can have lots of good fun if you wish With a game that I call UP UP UP with a fish Put me down said the fish This is no fun at all Put me down said the fish I do NOT wish to fall Have no fear said the cat I will not let you fall I will hold you up high as I stand on a ball With a book on one hand And a cup on my hat But that is not ALL I can do said the cat Look at me Look at me now said the cat With a cup and a cake on the top of my hat I can hold up TWO books I can hold up the fish And a little toy ship And some milk on a dish And look I can hop up and down on the ball But that is not all Oh no That is not all Look at me Look at me Look at me NOW It is fun to have fun But you have to know how I can hold up the cup And the milk and the cake I can hold up these books And the fish on a rake I can hold the toy ship And a little toy man And look With my tail I can hold a red fan I can fan with the fan As I hop on the ball But that is not all Oh no That is not all That is what the cat said Then he fell on his head He came down with a bump from up there on the ball And Sally and I We saw ALL the things fall And our fish came down too He fell into a pot He said Do I like this Oh no I do not This is not a good game Said our fish as he lit No I do not like it Not one little bit Now look what you did Said the fish to the cat Now look at this house Look at this Look at that You sank our toy ship Sank it deep in the cake You shook up our house And you bent our new rake You SHOULD NOT be here when our mother is not You get out of this house Said the fish in the pot But I like it here Oh I like it a lot Said the Cat in the Hat To the fish in the pot I will NOT go away I do NOT wish to go And so said the Cat in the Hat So so so I will show you Another good game that I know And then he ran out And then fast as a fox The Cat in the Hat Came back in with a box A big red wood box It was shut with a hook Now look at this trick Said the cat Take a look Then he got up on top With a tip of his hat I call this game FUN IN A BOX Said the cat In this box are two things I will show to you now You will like these two things Said the cat with a bow I will pick up the hook You will see something new Two things And I call them Thing One and Thing Two These things will not bite you They want to have fun Then out of the box Came Thing Two and Thing One And they ran to us fast They said How do you do Would you like to shake hands With Thing One and Thing Two And Sally and I Did now know what to do So we had to shake hands With Thing One and Thing Two We shook their two hands But our fish said No No Those Things should not be In this house Make them go They should not be here When your mother is not Put them out Put them out Said the fish in the pot Have no fear little fish Said the Cat in the Hat These things are good Things And he gave them a pat They are tame Oh so tame They have come here to play They will give you some fun On this wet wet day Now here is a game that they like Said the cat They like to fly kites Said the Cat in the Hat No Not in the house Said the fish in the pot They should not fly kites In a house They should not Oh the things they will bump Oh the things they will hit Oh I do not like it Not one little bit Then Sally and I Saw them run down the hall We saw those two Things Bump their kites on the wall Bump Thump Thump Bump Down the wall in the hall Thing Two and Thing One They ran up They ran down On the string of one kit We saw Mothers new gown Her gown with the dots That are pink white and red Then we saw one kite bump On the head of her bed Then those Things ran about With big bumps jumps and kicks And with hops and big thumps And all kinds of bad tricks And I said I do NOT like the way that they play If Mother could see this Oh what would she say Then our fish said Look Look And our fish shook with fear Your mother is on her way home Do you hear Oh what will she do to us What will she say Oh she will not like it To find us this way So DO something Fast said the fish Do you hear I saw her Your mother Your mother is near So as fast as you can Think of something to do You will have to get rid of Thing One and Thing Two So as fast as I could I went after my net And I said With my net I can get them I bet I bet with my net I can get those Things yet Then I let down my net It came down the a PLOP And I had them At last Those two Things had to stop Then I said to the cat Now you do as I say You pack up those Things And you take them away Oh dear said the cat You did not like our game Oh dear What shame What a shame What a shame Then he shut up the Things In the box with the hook And the cat went away With a sad kind of look That is good said the fishHe has gone away Yes But your mother will come She will find this big mess And this mess is so big And so deep and so tall we can not pick it up There is no way at all And THEN Who was back in the house Why the cat Have no fear of this mess Said the Cat in the Hat I always pick up all my playthings And so I will show you another good trick that I know Then we saw him pick up all the things that were down He picked up the cake And the rake And the gown And the milk and the strings And the books and the dish And the fan and the cup And the ship and the fish And he put them away Then he said That is that And then he was gone with the tip of his hat Then our mother came in And said said to us two Did you have any fun Tell me What did you do And Sally and I did not know What to say Should we tell her The things that went on there that day She we tell her about it Now what SHOULD we do Well what would YOU do If you mother asked YOU'
counter = collections.Counter()
for w in text.split():
    counter[w] += 1
normalize = lambda x: int(x / (max(counter.values()) - min(counter.values())) * 90 + 10)
word_list = {k: normalize(v) for k, v in counter.items()}

# <codecell>

import vincent
vincent.core.initialize_notebook()
bar = vincent.Bar(multi_iter1['y1'])
bar.axis_titles(x='Index', y='Value')
bar.display()

# <codecell>

bar.to_json('bar.json', html_out=True, html_path='vincent_bar.html')

# <codecell>

line = vincent.Line(multi_iter1, iter_idx='index')
line.axis_titles(x='Index', y='Value')
line.legend(title='Categories')
line.display()

# <codecell>

line = vincent.Line(price[['GOOG', 'AAPL']])
line.axis_titles(x='Date', y='Price')
line.legend(title='GOOG vs AAPL')
line.display()

# <codecell>

scatter = vincent.Scatter(df_1)
scatter.axis_titles(x='Index', y='Data Value')
scatter.legend(title='Categories')
scatter.colors(brew='Set3')
scatter.display()

# <codecell>

stacked = vincent.StackedArea(df_1)
stacked.axis_titles(x='Index', y='Value')
stacked.legend(title='Categories')
stacked.colors(brew='Spectral')
stacked.display()

# <codecell>

stacked = vincent.StackedArea(price)
stacked.axis_titles(x='Date', y='Price')
stacked.legend(title='Tech Stocks')
stacked.display()

# <codecell>

stack = vincent.StackedBar(df_2)
stack.legend(title='Categories')
stack.scales['x'].padding = 0.1
stack.display()

# <codecell>

stack = vincent.StackedBar(df_farm.T)
stack.axis_titles(x='Total Produce', y='Farms')
stack.legend(title='Produce Types')
stack.colors(brew='Pastel1')
stack.display()

# <codecell>

group = vincent.GroupedBar(df_2)
group.legend(title='Categories')
group.colors(brew='Spectral')
group.width=750
group.display()

# <codecell>

group = vincent.GroupedBar(df_farm)
group.axis_titles(x='Total Produce', y='Farms')
group.legend(title='Produce Types')
group.colors(brew='Set2')
group.display()

# <codecell>

pie = vincent.Pie(farm_1)
pie.legend('Farm 1 Fruit')
pie.display()

# <codecell>

donut = vincent.Pie(farm_1, inner_radius=200)
donut.colors(brew="Set2")
donut.legend('Farm 1 Fruit')
donut.display()

# <codecell>

word = vincent.Word(word_list)
word.display()

# <headingcell level=1>

# World Map

# <codecell>

!curl -v -X HEAD http://mashupguide.net/wwod14/world-countries.json 

# <codecell>

# https://vincent.readthedocs.org/en/latest/quickstart.html

#world_topo = r'https://raw.github.com/trifacta/vega/gh-pages/data/world-countries.json'
# CORS enabled
#world_topo = r'http://mashupguide.net/wwod14/world-countries.topo.json'
world_topo = "files/vincent_map_data/world-countries.topo.json"
geo_data = [{'name': 'countries',
             'url': world_topo,
             'feature': 'world-countries'}]

vis = vincent.Map(geo_data=geo_data, scale=200)
vis

# <codecell>

vis.display()

# <codecell>

vis.to_json('world_map.json', html_out=True, html_path='vincent_world_map.html')

# <markdowncell>

# When I load vincent_world_map.html -- I don't see a map.  I see in JS console: "Uncaught TypeError: Cannot read property 'world-countries' of undefined "

# <codecell>

geo_data = [{'name': 'counties',
             'url': 'files/vincent_map_data/us_counties.topo.json',
             'feature': 'us_counties.geo'},
            {'name': 'states',
             'url': 'files/vincent_map_data/us_states.topo.json',
             'feature': 'us_states.geo'}]

vis = vincent.Map(geo_data=geo_data, scale=1000, projection='albersUsa')
del vis.marks[1].properties.update
vis.marks[0].properties.update.fill.value = '#084081'
vis.marks[1].properties.enter.stroke.value = '#fff'
vis.marks[0].properties.enter.stroke.value = '#7bccc4'
vis.display()

# <codecell>

# https://vincent.readthedocs.org/en/latest/quickstart.html#data
#Map Data Binding
import json
import pandas as pd
#Map the county codes we have in our geometry to those in the
#county_data file, which contains additional rows we don't need
with open('vincent_map_data/us_counties.topo.json', 'r') as f:
    get_id = json.load(f)


#A little FIPS code munging
new_geoms = []
for geom in get_id['objects']['us_counties.geo']['geometries']:
    geom['properties']['FIPS'] = int(geom['properties']['FIPS'])
    new_geoms.append(geom)

get_id['objects']['us_counties.geo']['geometries'] = new_geoms

with open('vincent_map_data/us_counties_intfips.topo.json', 'w') as f:
    json.dump(get_id, f)

#Grab the FIPS codes and load them into a dataframe
geometries = get_id['objects']['us_counties.geo']['geometries']
county_codes = [x['properties']['FIPS'] for x in geometries]
county_df = pd.DataFrame({'FIPS': county_codes}, dtype=str)
county_df = county_df.astype(int)

#Read into Dataframe, cast to string for consistency
df = pd.read_csv('data/us_county_data_vincent.csv', na_values=[' '])
df['FIPS_Code'] = df['FIPS'].astype(str)

#Perform an inner join, pad NA's with data from nearest county
merged = pd.merge(df, county_df, on='FIPS', how='inner')
merged = merged.fillna(method='pad')

# <codecell>

geo_data = [{'name': 'counties',
             'url': 'files/vincent_map_data/us_counties_intfips.topo.json',
             'feature': 'us_counties.geo'}]


vis = vincent.Map(data=merged, geo_data=geo_data, scale=1100,
                  projection='albersUsa', data_bind='Employed_2011',
                  data_key='FIPS', map_key={'counties': 'properties.FIPS'})
vis.marks[0].properties.enter.stroke_opacity = vincent.ValueRef(value=0.5)
#Change our domain for an even inteager
vis.scales['color'].domain = [0, 189000]
vis.legend(title='Number Employed 2011')
vis.to_json('unemployed.json', html_out=True, html_path='unemployed_map.html')

# <codecell>

vis.display()

# <codecell>


