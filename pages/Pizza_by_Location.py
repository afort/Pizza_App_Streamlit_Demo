import streamlit as st
import pandas as pd
from streamlit_folium import folium_static, st_folium
import folium
import pydeck as pdk
import itertools
import numpy as np

# Load the data
df_datafiniti = pd.read_csv("./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv")
df_datafiniti = df_datafiniti.filter(items=['name', 'province', 'city', 'address', 'latitude', 'longitude', 'postalCode', 'menus.name'])
df_datafiniti = df_datafiniti.drop_duplicates()

st.set_page_config(page_title=None, page_icon=None, layout="wide")

st.markdown("### Pizza Locations")

# Drop Down
selections = st.multiselect("Choose State(s)", df_datafiniti.province.unique())
if len(selections) == 0:
    # Default new york
    selections = ['NY']
df_by_state = df_datafiniti[df_datafiniti['province'].isin(selections)]

col1, col2 = st.columns(2)

with col1:
    # Table
    st.dataframe(df_by_state)

with col2:
    # Marker Map
    m = folium.Map(location = [df_by_state.latitude.mean(), df_by_state.longitude.mean()], zoom_start = 3, control_scale = True)

    # Loop through each row in the dataframe
    for i, row in df_by_state.iterrows():
        # setup the content of the popup
        iframe = folium.IFrame('Item Name: ' + str(row["menus.name"]))

        # initialize the popup with the iframe
        popup = folium.Popup(iframe, min_width = 300, max_width = 300)

        # add each row to the map
        folium.Marker(location = [row["latitude"], row["longitude"]], popup = popup, c = row["menus.name"]).add_to(m)

    st_data = folium_static(m, width=1000)

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["longitude", "latitude"],
                    radius=1000,
                    elevation_scale=100,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# Map with barchart overlaid
midpoint = mpoint(df_by_state.latitude, df_by_state.longitude)
map(df_by_state, midpoint[0], midpoint[1], 6)