import streamlit, requests, pandas as pd, snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

 # The below line is the link to the text file in the S3 bucket
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
 # take the json version of the resonse and normalize it
 fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

# New section to display fruityvice api response
streamlit.header('Fruitvice Fruit Advice!')
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
 else:
  back_from_function = get_fruitvice_data(fruit_choice)
  streamlit.dataframe(back_from_function) # output it to the screen as a table
except URLError as e:
 streamlit.error()

streamlit.header("The fruit load list contains:")
# Snowflake related functions
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from fruit_load_list")
  return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
 # my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)

# Don't run anything past here while we troubleshoot
streamlit.stop()

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("insert into fruit_load_list values ('from streamlit')")
  return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
 streamlit.text(back_from_function)

