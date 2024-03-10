import streamlit as st
import pandas as pd
from streamlit_folium import folium_static, st_folium
import folium
import itertools

df_datafiniti = pd.read_csv("./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv")
#st.dataframe(df_datafiniti)

st.markdown("### Here, we look at the datafiniti dataset, where location is included.")

m = folium.Map(location = [df_datafiniti.latitude.mean(), df_datafiniti.longitude.mean()], zoom_start = 3, control_scale = True)

# Loop through each row in the dataframe
for i, row in df_datafiniti.iterrows():
    # setup the content of the popup
    iframe = folium.IFrame('Item Name: ' + str(row["menus.name"]))
    
    # initialize the popup with the iframe
    popup = folium.Popup(iframe, min_width = 300, max_width = 300)
    
    # add each row to the map
    folium.Marker(location = [row["latitude"], row["longitude"]], popup = popup, c = row["menus.name"]).add_to(m)
    
st_data = folium_static(m, width=1000)

