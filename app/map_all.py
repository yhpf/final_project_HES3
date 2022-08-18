import pandas as pd
import folium
import geopandas


def create_map(Year, Activity):
    tables = pd.read_csv('AllCountry.csv')

    latlong = pd.read_html('https://developers.google.com/public-data/docs/canonical/countries_csv')

    #Sum duplicates then remove column
    tables['Total'] = tables.groupby(['Country', 'Activity','Year'])['Quantity'].transform('sum')
    tables = tables.drop_duplicates(subset=['Country', 'Activity','Year'])
    del tables['Quantity']
    #Change Own use
    tables['Activity'] = tables['Activity'].replace(['Own use'],'Ownuse')

    # Get rows, for rows with year not "2019": delete row
    # Export map.py as function and call in app.py, take in user inoput (years) and display html file.
    tables = tables.loc[tables["Year"] == Year ]
    tables = tables.loc[tables["Activity"] == Activity]
    del tables['Year']
    del tables['Activity']
    del tables['Unit']
    tables['Country'] = tables['Country'].replace(['United States'],'United States of America')
    tables['Country'] = tables['Country'].replace(['Russian Federation'],'Russia')

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    table = world.merge(tables, how="left", left_on=['name'], right_on=['Country'])
    table = table.dropna(subset="Total")

    my_map = folium.Map(min_zoom = 3, zoom_start= 4, max_bounds=True, position="absolute", top = "6%")
    folium.Choropleth(
        geo_data=table,
        name='choropleth',
        data=table,
        columns=['Country','Total'],
        key_on='feature.properties.name',
        fill_color='OrRd',
        fill_opacity=0.1,
        line_opacity=0.2,
        legend_name='Energy(Terajoules)'
    ).add_to(my_map)

    html="""<iframe src= "/graph"  width="300" height="250"  frameborder="0">"""


    tables['Country'] = tables['Country'].replace(['United States of America'],'United States')

    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html Remove key

    for i in range(len(latlong[0])):
        for j in tables['Country']:
            if latlong[0]['name'][i] == j:
                folium.Marker(location = [latlong[0]['latitude'][i], latlong[0]['longitude'][i]], popup = folium.Popup((j + ": " + str(int(tables[tables['Country']==j]['Total'].iloc[0])) + " Tj"), max_width=500)).add_to(my_map)
            else:
                continue

    #popup = folium.Popup(folium.Html(html, script=True))

    mapping = my_map.get_root().render()

    #https://github.com/python-visualization/folium/issues/781 outputting map

    return mapping