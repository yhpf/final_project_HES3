import pandas as pd
import folium
import geopandas

tables = pd.read_csv("../predictions.csv")

Activity = "Ownuse"

tables = tables.loc[tables["Activity"] == Activity]
print(tables)

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
table = world.merge(tables, how="left", left_on=['name'], right_on=['Country'])
table = table.dropna(subset="Quantity")
my_map = folium.Map(min_zoom = 3, zoom_start= 4, max_bounds=True)
folium.Choropleth(
    geo_data=table,
    name='choropleth',
    data=table,
    columns=['Country','Quantity'],
    key_on='feature.properties.name',
    fill_color='OrRd',
    fill_opacity=0.1,
    line_opacity=0.2,
    legend_name='Predicted Energy'
).add_to(my_map)

#html="""<iframe src= "graph"  width="300" height="250"  frameborder="0">"""
#popup = folium.Popup(folium.Html(html, script=True))
#USA
folium.Marker(location=[38.00, -97.00], popup=folium.Popup(("United States of America " + str(tables[tables['Country']=="United States"]['Quantity'].iloc[0]) + " Terajoules"), max_width=500)).add_to(my_map)
#Japan
folium.Marker(location=[36.20, 138.25], popup = folium.Popup(("Japan " + str(tables[tables['Country']=="Japan"]['Quantity'].iloc[0]) + " Terajoules"), max_width=500)).add_to(my_map)
#Belgium
folium.Marker(location=[50.50, 4.28], popup= folium.Popup(("Belgium " + str(tables[tables['Country']=="Belgium"]['Quantity'].iloc[0]) + " Terajoules"), max_width=500)).add_to(my_map)
#Russia
folium.Marker(location=[61.52, 105.32], popup= folium.Popup(("Russia " + str(tables[tables['Country']=="Russia"]['Quantity'].iloc[0]) + " Terajoules"), max_width=500)).add_to(my_map)

#Go plot data, export as html file and add into marker.

my_map.save('templates/prediction_maps/map_ownuse.html') 
