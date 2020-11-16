# Filtering process

The first thing to do is to unwind the companies.json database into the diffrent offices that are stored there. To do so we need to use the ´aggregate´ function from pymongo and `"$unwind":"$offices"` and store the unwinded informatio in a new MongoDB collection called `offices`. 

After that, from all the officces we need to select the companies that have design related categories on one hand, and on the other the ones related with tech activities. These filtering are conducted with the `isfashion` and `istech` function stored in `functions\filtering.py`. We need to filter the latter categories for the ones that made more than one millon US dollars. To do so, we need to define the `obtain_1m` fucntion to check this conditon. Some companies have different currencies, so this function also takes this into account and convert them into US dollars.

This allows to create a list of neighbours, so using the `$near` option in `pymongo` we retrieve those spots closer than 1km from one of these valid points. We also exclude the spots nearer than 50m to exclude the same office that we want to get its closer neighbours.

From all the possible locations, there are many of them that have the same coordinates, maybe because they are in the same building or very close. These repeated coordinates would increase the API request incecesarily and extend the computation time. If there is a spot that meet the requireremnts, the other in the same coordinates would as well, so we need to create a dataset wiht "unique coordinates". This is conducted by creating a column in the Pandas DataFrame wiht a set with the longitude and latitude, and after that applying the Panda's `drop_duplicates` on this column keeping the first record.

With this procedure, we have a candidate list with ~3000 potiential unique places. This forms a good enough dataset that can be handled and completed with API requests.

# Foursquere API querys

Having the list of candidate places, we need to check the conditions asked in the exercise. The Foursquare API is ideal to check the conditions, as the required places are labelled with "*Airport","Pet Service", "Daycare", "Nightlife Spot", "Vegetarian / Vegan Restaurant"* and *"Basketball Stadium"* categories. We need to request the places in these categories. 

**We need to define the search radii for each category**. The one for the Basketball Stadium is defined in the project that should be 10 km. For the Airport, we define a 30km radius to cover a city, for the vegan spots 500m , for the nighhtlife party places 2km and for the pet services and the child daycare we define a 1km search.

In additon, **for the vegan restaurants and the nightlife activity** we want to not only see if there is only one, **we want to check that near the office there is some variety of these kind of places**. We retrieve how many places are near the radius, but with a maximum of 10 places for the vegan restaurants and 20 for the nightlife spots, to not to overload the queries.

Now we have parameters that we can analyze what is the best office location. This is conducted in the [analysis.ipynb](https://github.com/nachordo/geospatial-data-project/blob/main/analysis.ipynb) notebook.

