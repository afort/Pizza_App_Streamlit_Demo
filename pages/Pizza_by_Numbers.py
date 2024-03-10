import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from itertools import chain

def update_selection(selection):
    top_n = df2_ingredients.nlargest(n = int(selection), columns = ["count_of"])
    return top_n

datafiniti_path = "./data/Datafiniti_Pizza_Restaurants_and_the_Pizza_They_Sell_May19.csv" # includes latitude and longitude information
ingredient_path = "./data/Data_Model_Pizza_Sales.xlsx" # the sales of a specific restaurant, including ingredients

df_ingredients = pd.read_excel(ingredient_path)
df_ingredients['pizza_ingredients'] = [x.split(',') for x in df_ingredients['pizza_ingredients'].values.tolist()] # converting string contents to list
df_ingredients['order_id'] = df_ingredients['order_id'].astype(int) # setting order_id as dtype int
df_ingredients['datetime'] = pd.to_datetime(df_ingredients['order_date'].astype(str) + ' ' + df_ingredients['order_time'].astype(str))
max_order = df_ingredients['order_id'].max() # haven't verified true number of order_id(s), but am relying on 1 - n value setting

# performing a count function of the list, returning a new df (df2)
df2_ingredients = pd.Series(Counter(chain(*df_ingredients.pizza_ingredients))).sort_index().rename_axis('pizza_ingredients').reset_index(name='count_of')

# explicitly stating variable type because of issues with streamlit and pyarrow
# serialization of dataframe
df2_ingredients["pizza_ingredients"] = df2_ingredients["pizza_ingredients"].astype(str)
df2_ingredients["count_of"] = df2_ingredients["count_of"].astype(int)
df3_ingredients = df2_ingredients.sort_values(by = ["count_of"], ascending = False)

num_ingred = len(df2_ingredients['pizza_ingredients'].unique()) # number of ingredients


#-----------------Actual streamlit page coding begins here----------------------
st.set_page_config(page_title = "About The Data", layout = "wide")
col1, col2 = st.columns(2)


with col1:
    st.markdown('# Table of Ingredients')
    st.markdown("### This is what the **original data** looks like, as a simple table")
    df_ingredients_items = df_ingredients.filter(items=['pizza_name', 'pizza_ingredients', 'pizza_category', 'unit_price', 'total_price'])
    st.dataframe(df_ingredients_items)
    st.divider()
    st.markdown("### What are the top ingredients?")
    num_list = [item for item in range(1, (num_ingred+1))] # create a list from 1 to n of ingredients, this is done for a 'Top __' selection
    selection = st.slider("# Slide to select Top X Ingredients:", min_value=1, value=15,  max_value=num_ingred)
    if selection is not False:
        top_n = update_selection(selection)
        st.subheader(" Pizza 'Pie' Chart")
        st.markdown(f"### Out of *{max_order}* orders and *{num_ingred}* ingredients, this is what the *Top __ Topping* selections looked like.".format(max_order, num_ingred))
        plt.pie(top_n['count_of'], labels = top_n['pizza_ingredients'])
        st.pyplot(plt)
with col2:
    st.markdown("# Orders placed")

    st.markdown("### What are the peak order dates?")
    df_ingredients['date_count'] = df_ingredients.order_date.map(df_ingredients.groupby('order_date').size())
    st.bar_chart(df_ingredients, x='order_date', y='date_count', color='pizza_category')


    st.markdown("### What is the most profitable pizza?")
    profit_pizza = df_ingredients.groupby(by=['pizza_name'])['total_price'].sum().reset_index()
    profit_pizza = profit_pizza.sort_values(by=['total_price'], ascending=False)
    st.bar_chart(profit_pizza, x='pizza_name', y='total_price', color='pizza_name')

    # style
    th_props = [
        ('font-size', '25px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7ffff')
    ]

    td_props = [
        ('font-size', '25px')
    ]

    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]


    profit_style_df = profit_pizza.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(profit_style_df)


