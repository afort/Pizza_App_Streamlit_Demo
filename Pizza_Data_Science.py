import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Welcome", page_icon = ":heart:", layout = "wide")
st.markdown("# Happy Pi Day!")

col1, col2, col3 = st.columns(3, gap='small')

with col1:
    st.image("./data/Pi-Day-Pie.jpg", width=300)
    st.markdown("**Pi Day** was founded in 1988 by Larry Shaw, an employee of the San Francisco science museum. In 2009, the United States House of Representatives supported the designation of Pi Day. UNESCO's 40th General Conference designated Pi Day as the International Day of Mathematics in November 2019.")
with col2:
    st.markdown("***Dataset 1*** includes sales from all over the United States, including location information.")
    df_datafiniti = pd.read_csv("./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv")
    df_datafiniti = df_datafiniti.filter(items=['name', 'province', 'city', 'menus.name', 'menus.amountMax'])
    st.dataframe(df_datafiniti)
with col3:
    st.markdown("***Dataset 2*** includes detailed data from the sales of a single restaurant in 2015.")
    ingredient_path = "./data/Data_Model_Pizza_Sales.xlsx"  # the sales of a specific restaurant, including ingredients
    df_ingredients = pd.read_excel(ingredient_path)
    df_ingredients['pizza_ingredients'] = [x.split(',') for x in df_ingredients['pizza_ingredients'].values.tolist()]
    df_ingredients = df_ingredients.filter(items=['pizza_name', 'pizza_category', 'pizza_ingredients'])
    st.dataframe(df_ingredients)
