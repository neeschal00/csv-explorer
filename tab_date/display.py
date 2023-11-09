import streamlit as st

from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_date_content (function): Function that will instantiate tab_date.logics.DateColumn class, save it into Streamlit session state and call its tab_date.logics.DateColumn.find_date_cols() method in order to find all datetime columns.
    Then it will display a Streamlit select box with the list of datetime columns found.
    Once the user select a datetime column from the select box, it will call the tab_date.logics.DateColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_date.logics.DateColumn.get_summary() as a Streamlit Table
    - the graph from tab_date.logics.DateColumn.histogram using Streamlit.altair_chart()
    - the results of tab_date.logics.DateColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """
    # Instantiate DateColumn class and save it into Streamlit session state
    date_column_instance = DateColumn(file_path=file_path, df=df)
    st.session_state.date_column_instance = date_column_instance

    # Find datetime columns
    date_column_instance.find_date_cols()

    # Display select box with datetime columns
    selected_column = st.selectbox("Select a datetime column:", date_column_instance.cols_list)

    if selected_column:
        # Set data for the selected datetime column
        date_column_instance.set_data(selected_column)

        # Display Expander container
        with st.expander("Date Column Summary"):
            # Display results of get_summary as a Streamlit Table
            st.table(date_column_instance.get_summary())

            # Display histogram using Streamlit.altair_chart()
            st.altair_chart(date_column_instance.barchart, use_container_width=True)

            # Display results of frequent using Streamlit.write
            st.write("Most frequent values:")
            st.write(date_column_instance.frequent)

