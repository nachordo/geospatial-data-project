# GeoSpatial Data Project

In this project I had to plan the location of a company in the `GAMING industry` based on a series of conditions. The location of the office has to be one of the offices listed in the `companies.json` database from other IRONHACK exercises. The goal is to prioritize among the conditions to choose the best location according to them. The requirements are the following:

1- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.

2- 30% of the company has at least 1 child.

3- Developers like to be near successful tech startups that have raised at least 1 Million dollars.

4- Executives like Starbucks A LOT. Ensure there's a Starbucks not too far.

5- Account managers need to travel a lot

6- All people in the company have between 25 and 40 years, give them some place to go to party.

7- The CEO is Vegan.

8- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.

9- The office dog "Pepe" needs a hairdresser every month. Ensure there's one not too far away.

As it is impossible to cover all of them, the goal is to choose the one that is the most appropiate.

The project is structured in different parts. First, I filtered the list of office candidates. Later, through API I will query the coordinates within certain distance treshold certains spots that fullfils the conditions asked. Lasly, I analize the results and choose the best office location.

The filtering and API querying proccess are executed through `main.py`, and it is explained in detail in the [filtering_process.md](https://github.com/nachordo/geospatial-data-project/blob/main/filtering_process.md). The decision process analysis is performed in the [analysis.ipynb](https://github.com/nachordo/geospatial-data-project/blob/main/analysis.ipynb) notebook by loading the csv file with the desition parameters previously computed. I used a python notebook as it is better to explain the it step by step and to show the results in the map.


![Gaming company](https://officesnapshots.com/wp-content/uploads/2016/06/avant-chicago-office-design-21.jpg)

## Strategy to filter first

In order to choose the best location, I needed to list all the different offices in a single MongoDB collection, so companies with various offices needed to be “unwinded”. I chose the first and third conditions to filter among all the possible candidates, so I can save API queries to retrieve the information from other conditions, and to finish the project before the deadline. This first filter has more sense to be applied, as other conditions are easier to meet in locations active and crowded. So I will examine the conditions for other variables based on the proximity to a design company or a succesful tech company.

## Using the Foursquare API to retrieve information about other conditions

In the Foursquare database, places are grouped among categories that are easy to adapt to analyze our conditions. This is because there are categories for airports, basketball stadiums, daycare for children, vegan restaurants, nightlife spots and pet care services. With queries within different distance radii, we can examine for each location candidate, how many of these conditions meet.

## Quantifying how conditions are met to provide the best location

There are conditions that are either met or not met, but others are based on whether there are some determinated spots nearby. To do something different, I introduced sigmoid functions to not to assign just 0 or 1, so I put intermediate values in distances that might be in the limit. Also, for other ones I introuduced that to get the complete point there should be variety of laces, as in the the vegan restaurants or nightlife party places.

![Sigmoid](https://www.researchgate.net/profile/Tali_Leibovich-Raveh/publication/325868989/figure/fig2/AS:639475206074368@1529474178211/A-Basic-sigmoid-function-with-two-parameters-c1-and-c2-as-commonly-used-for-subitizing.png)

This allows to create a score to quantify the better option, and to store possible alternatives based on the mentioned score if the first one is rejected for some hypotetical reason.

Lastly, with the folium library, I represented the best location according to this metric and represented it in a map, along with the required places as well.

![The map](images/map_nearby.png)


## Final thoughts




