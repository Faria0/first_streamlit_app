# imports:
import pandas
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Bluebery Oatmeal')
streamlit.text('🥗 Kale, Spinac & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



# Adding pandas data in
# Reading in data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# Show only some fruits:
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)



# New section for fruityvice api- requests
# Header
streamlit.header('Fruitvice Fruit Advice!')

# Create a function to pull data from fruityvice:
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
  # streamlit.text(fruityvice_response.json()) # Writes data on screen. Removed as not needed
  # Making the presentation nicer:
  # normalize the json into a pandas object
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  


# try and except for user input for fruityvice:
try:
  # Adding user input for fruit names:
  fruit_choice = streamlit.text_input('What fruit would you like information about?') # Second arguement is a string as a suggestion in the text input box
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # display the new pandas dataframe
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  strealit.error()
    
# Add this so nothing runs past this whilst troubleshooting:
#streamlit.stop()


# Snowflake connector
streamlit.header("The fruit load list contains:")

# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

# Adding a button to load the fruit:
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


# Allow the end user to add a fruit to the list:
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding"+new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)


# Fruit list into snowflake
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
