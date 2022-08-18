from html.entities import html5
import pandas as pd
import folium
import geopandas
from IPython.display import display
import numpy as np



latlong = pd.read_html('https://developers.google.com/public-data/docs/canonical/countries_csv')

tables = pd.read_csv('AllCountry.csv')

tables['Total'] = tables.groupby(['Country', 'Activity','Year'])['Quantity'].transform('sum')
tables = tables.drop_duplicates(subset=['Country', 'Activity','Year'])
del tables['Quantity']
#Change Own use
tables['Activity'] = tables['Activity'].replace(['Own use'],'Ownuse')

# Get rows, for rows with year not "2019": delete row
# Export map.py as function and call in app.py, take in user inoput (years) and display html file.
tables = tables.loc[tables["Year"] == 1991]
tables = tables.loc[tables["Activity"] == "Fuel"]
del tables['Year']
del tables['Activity']
del tables['Unit']
tables['Country'] = tables['Country'].replace(['United States'],'United States of America')
tables['Country'] = tables['Country'].replace(['Russian Federation'],'Russia')

tables = tables[tables['Country']=="Albania"]['Total'].iloc[0]

print(tables)