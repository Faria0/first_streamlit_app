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

# try and except for user input for fruityvice:
try:
  # Adding user input for fruit names:
  fruit_choice = streamlit.text_input('What fruit would you like information about?') # Second arguement is a string as a suggestion in the text input box
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    # Request response
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice) # User fruit selection is requested
    # streamlit.text(fruityvice_response.json()) # Writes data on screen. Removed as not needed
    # Making the presentation nicer:
    # normalize the json into a pandas object
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display the new pandas dataframe
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  strealit.error()
    
# Add this so nothing runs past this whilst troubleshooting:
streamlit.stop()

# Snowflake connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Add a fruit box:
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding', add_my_fruit)


# Fruit list into snowflake
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
