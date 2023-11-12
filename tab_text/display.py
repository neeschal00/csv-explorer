import streamlit as st

from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    
    text_column = TextColumn(file_path=file_path, df=df)
    
    try:
        text_column.find_text_cols()
    except Exception as e:
        st.error("Unable to parse CSV file are you sure you are using CSV format")
        return
    
    selected_column = st.selectbox('Select Text Column', text_column.cols_list)

    if selected_column:
        text_column.set_data(selected_column)
        

        with st.expander('Text Column Summary'):
            
            st.table(text_column.get_summary())

            
            st.altair_chart(text_column.barchart, use_container_width=True)

            st.write('Most frequent values:')
            st.write(text_column.frequent)