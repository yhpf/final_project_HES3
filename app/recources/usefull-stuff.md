# Here we can put links to usefull stuff 

This file is probably temporary and we can remove it later and move what we actually used into the References & Citations section in the README.md file. 

## IMPORTANT! - Pushing to GitHub Repo
The branch we use on the group repo is "master", please use **git push -u origin master** when you push! The "main" just not working on Lu's end somehow,...

## World or Country Heatmap

### Londitude and Latitude
If we do not have long/lat we can use  https://developers.google.com/public-data/docs/canonical/countries_csv or similar to add long/lat to our data. It seems most of the heat maps requires longitude and latitude.

### Possible Heatmap options:
1. Folium (Python library for maps). You can just pip install and then import into jupyter notebook. Google "Folium heatmaps examples" and you will get a lot of examples and different explanations on how to use it.
2. Geoplot and GeoPandas. Also seems pretty straight forward https://geopandas.org/en/stable/gallery/plotting_with_geoplot.html https://www.relataly.com/visualize-covid-19-data-on-a-geographic-heat-maps/291/
3. Good old Matplotlib also seems to be able to make heatmaps https://stackoverflow.com/questions/22684730/heat-world-map-with-matplotlib
4. Plotly can also make heatmaps https://plotly.com/python/maps/
5. Gmaps https://jupyter-gmaps.readthedocs.io/en/latest/# You can get heatmaps via google maps in jupyter notebook, but it requires an API key.
6. I worked with a person a couple of years ago that was really good at heatmaps in ArcGIS. Also Mode seem to have heapmap features. But after a first quick look, I think that probably option 1-5 might be better for us.
7. Tablueu (Unlikely because of free tial for a limited period and eventual paying)
8. Seaborn (more of a heatmap table rather than an actual map visuallisation, based on matplotlib)
9. Mymaps (Google earth API? https://www.google.com/maps/d/u/0/)
10. MS Excel Geoflow (Seems outdated in terms of visuals though https://www.microsoft.com/en-us/research/blog/geoflow-takes-data-3-d-drive/)

