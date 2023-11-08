import streamlit as st

from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    """
    --------------------
    Description
    --------------------
    -> display_overall_df (function): Function that will instantiate tab_df.logics.Dataset class, save it into Streamlit session state and call its tab_df.logics.Dataset.set_data() method in order to compute all information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    1. the results of tab_df.logics.Dataset.get_summary() as a Streamlit Table
    2. the results of tab_df.logics.Dataset.table using Streamlit.write()
    Finally it will display a second Streamlit Expander container with a slider to select the number of rows to be displayed and a radio button to select the method (head, tail, sample).
    According to the values selected on the slider and radio button, display the subset of the dataframe accordingly using Streamlit.dataframe
    
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file

    --------------------
    Returns
    --------------------
    -> None
    
    """
    dataset = Dataset(file_path)
    dataset.set_df()
    
    dataset.set_data()
    # Sumary display
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
