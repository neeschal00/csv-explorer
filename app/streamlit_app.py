# Import packages
import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Set Python path
current_dir = os.path.dirname(__file__)
parent_dir = str(Path(current_dir).resolve().parents[0])
sys.path.append(parent_dir)

# Import custom functions
from tab_df.display import display_tab_df_content
from tab_num.display import display_tab_num_content
from tab_text.display import display_tab_text_content
from tab_date.display import display_tab_date_content

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="CSV Explorer",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Set objects in Streamlit session state
st.session_state["file_path"] = None
st.session_state["df"] = None
st.session_state["dataset"] = None
st.session_state["selected_num_col"] = None
st.session_state["num_column"] = None
st.session_state["selected_text_col"] = None
st.session_state["text_column"] = None
st.session_state["selected_date_col"] = None
st.session_state["date_column"] = None

# Display Title
st.title("CSV Explorer")

# Add Window to upload CSV file
with st.expander("ℹ️ - Streamlit application for performing data exploration on a CSV", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file")
    # st.session_state.file_path = st.file_uploader("Choose a CSV file")
    # print(st.session_state.file_path)


# If a CSV file is uploaded, display the different tabs
if uploaded_file is not None:
    filename = uploaded_file.name
    # Construct the file path in the "csv" directory
    file_path = os.path.join("csv", filename)

    # Save the uploaded file to the "csv" directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    tab_df, tab_num, tab_text, tab_date = st.tabs(["DataFrame", "Numeric Serie", "Text Serie", "Datetime Serie"])
    st.session_state.file_path = file_path
    try:
        st.session_state["df"] = pd.read_csv(file_path)
    except UnicodeDecodeError:
        st.session_state["df"] = pd.read_csv(file_path,encoding = "ISO-8859-1")
    with tab_df:
        display_tab_df_content(file_path=st.session_state.file_path)
    with tab_num:
        
        display_tab_num_content(file_path=st.session_state.file_path,df=st.session_state["df"])
    with tab_text:
        
        display_tab_text_content(st.session_state.file_path,df=st.session_state["df"])
    with tab_date:
        
        display_tab_date_content(st.session_state.file_path,df=st.session_state["df"])