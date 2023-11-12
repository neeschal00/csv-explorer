import streamlit as st

from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
    
    date_column_instance = DateColumn(file_path=file_path, df=df)
    st.session_state.date_column_instance = date_column_instance

    try:    
        date_column_instance.find_date_cols()
    except Exception as e:
        st.error("Unable to set date data are you sure you are using CSV format file?")
        return
    
    selected_column = st.selectbox("Select a datetime column:", date_column_instance.cols_list)

    if selected_column:
        
        date_column_instance.set_data(selected_column)
        
        
        with st.expander("Date Column Summary"):
            st.table(date_column_instance.get_summary())
            st.altair_chart(date_column_instance.barchart, use_container_width=True)
            st.write("Most frequent values:")
            st.write(date_column_instance.frequent)

