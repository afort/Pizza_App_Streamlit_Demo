import streamlit as st
import pandas as pd
from streamlit_folium import folium_static, st_folium
import folium
import itertools

df_datafiniti = pd.read_csv("./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv")
df_datafiniti = df_datafiniti.filter(items=['name', 'province', 'city', 'address', 'latitude', 'longitude', 'postalCode', 'menus.name'])
df_datafiniti = df_datafiniti.drop_duplicates()

st.markdown("### Pizza Locations")

selections = st.multiselect("Choose State(s)", df_datafiniti.province.unique())
if len(selections) == 0:
    selections = ['AL']

df_by_state = df_datafiniti[df_datafiniti['province'].isin(selections)]

st.dataframe(df_by_state)


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

