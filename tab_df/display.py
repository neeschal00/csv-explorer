import streamlit as st

from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    
    dataset = Dataset(file_path)
    try:
        dataset.set_df()
    except Exception as e:
        st.error("Unable to parse dataframe are you sure you are using CSV format")
        return
    
    dataset.set_data()
    with st.expander("Dataset Summary"):
        summary_df = dataset.get_summary()

        
        st.table(summary_df)
        dataset.table = dataset.table.astype(str)
        st.write("Columns")
        st.table(dataset.table)
    
    
    with st.expander("Display Subset of Data"):
        
        num_rows = st.slider("Select the number of rows to display", 1, dataset.n_rows, 5)
        method = st.radio("Select the method to display data", ("Head", "Tail", "Sample"))
        
        if method == "Head":
            st.dataframe(dataset.get_head(num_rows))
        elif method == "Tail":
            st.dataframe(dataset.get_tail(num_rows))
        else:  
            st.dataframe(dataset.get_sample(num_rows))
