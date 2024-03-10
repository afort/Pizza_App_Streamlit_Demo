import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Welcome", page_icon = ":heart:", layout = "wide")

st.markdown("# Happy Pi Day!")
st.image("./data/Pi-Day-Pie.jpg", width=300)

df_datafiniti = pd.read_csv("./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv")
st.dataframe(df_datafiniti)

