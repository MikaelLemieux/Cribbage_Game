import streamlit as st
import base64
#import streamlit_analytics
from streamlit_chat import message
import openai
from Welcome import *
from Rules import *
from Main import *
from Crib_Game import *
from Computer_Crib import *

# Set page config
#st.set_page_config(
 #   page_title="Cribbage Quest",
  #  page_icon=":f44a:",
  #  layout="wide",
  #  initial_sidebar_state="expanded"
#)

# Define user credentials (username: password)
user_credentials = {
    "DanOuellet": "Lemieux24#",
    "MikLemieux": "Lemieux24#",
    # Add more users as needed
}

# Check if the user is logged in
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Authentication check
if st.session_state['authentication_status']:
    # User is authenticated, proceed with app

    # App content starts here
    png_file = './Crib.png'

    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_png_as_page_bg(png_file, width, height):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = f'''
            <div>
            <div style="text-align: center;">
            <img src="data:image/png;base64,{bin_str}" style="width:{width}px; height:{height}px;">
            </div>
            '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

    set_png_as_page_bg(png_file, 250, 125)

    # Create a dictionary to categorize your apps
    app_categories = {
        "Welcome": ["Welcome"],
        "Daily Challenge": ["Daily Challenge"],
        "Crib Game": ["P2P", "Computer Game"],
        "Rules": ['Rules'],
    }

    # Dropdown for selecting a category
    selected_category = st.sidebar.selectbox("Select Category:", list(app_categories.keys()))
    selected_apps = app_categories[selected_category]
    app_selection = st.sidebar.radio("Select App:", selected_apps)
    
    # App Functionality
    if app_selection == "Welcome":
        WC()
    elif app_selection == "Daily Challenge":
        main_page()
    elif app_selection == "P2P":
        Game()
    elif app_selection == "Computer Game":
        Comp_Game()
    elif app_selection == "Rules":
        Rules()


    # User Feedback Section
    feedback_list = []
    if "feedback_submitted_faces" not in st.session_state:
        st.session_state["feedback_submitted_faces"] = False
    from streamlit_feedback import streamlit_feedback
    feedback = streamlit_feedback(
        feedback_type="faces",
        optional_text_label="[Optional] Please provide an explanation",
    )
    
    # OpenAI Integration
  #  openai.api_key = st.secrets["openai"]["api_key"]
   # if "openai_model" not in st.session_state:
    #    st.session_state["openai_model"] = "gpt-3.5-turbo"
    #with st.sidebar.expander("🤖 Hello, I am Crib Bot. Can I be of assistance?"):
     #   prompt = st.text_area("Enter Question", key="prompt_key", max_chars=150)
      #  if prompt:
       #     with st.spinner("🤖 Thinking..."):
        #        response = openai.ChatCompletion.create(
         #           model=st.session_state["openai_model"],
          #          messages=[{"role": "user", "content": prompt}],
           #     )
            #    truncated_response = response.choices[0].message["content"][:150]
             #   st.write(truncated_response)

    # Logout button (moved to the bottom of the sidebar)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line
    if st.sidebar.button('Logout'):
        st.session_state['authentication_status'] = None
        st.experimental_rerun()

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')

elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in user_credentials and user_credentials[username] == password:
            st.session_state['authentication_status'] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

