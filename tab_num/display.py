import streamlit as st
from tab_num.logics import NumericColumn


#display logic for tab_num
def display_tab_num_content(file_path=None, df=None):
    
    numeric_col = NumericColumn(file_path=file_path, df=df)
    try:
        numeric_col.find_num_cols()
    except Exception as e:
        st.error("Unable to parse CSV file are you sure you are using CSV format file")
        return

    selected_col = st.selectbox("Select a numeric column", numeric_col.cols_list)



    if selected_col:
        
        numeric_col.set_data(selected_col)
        

        with st.expander("Numeric Column Information"):
            
            st.table(numeric_col.get_summary())
            
            st.altair_chart(numeric_col.histogram, use_container_width=True)

            st.write("Frequent Values:")
            st.write(numeric_col.frequent)