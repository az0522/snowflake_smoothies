# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
# st.write(
#     """Replace this example with your own code!
#     **And if you're new to Streamlit,** check
#     out our easy-to-follow guides at
#     [docs.streamlit.io](https://docs.streamlit.io).
#     """
# )

st.write("Choose the **fruits** you want in your custom Smoothie!")


# option = st.selectbox(
#     "What is your favorite fruit?",
#     ('Banana', 'Strawberries', 'Peaches'))

# st.write("You selected:", option)

name_on_order = st.text_input('Name on Smoothie:')
# st.write('name on you smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert the Snowpark DF to a Pandas DF, so we can use LOC function.
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient , 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', ingredient, ' is ', search_on, '.')
        
        st.subheader(ingredient + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + ingredient)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into orders (ingredients, name_on_order) 
                    values ('""" + ingredients_string + """','""" + name_on_order + """' )"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
