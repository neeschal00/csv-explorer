import streamlit as st

from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_text_content (function): Function that will instantiate tab_text.logics.TextColumn class, save it into Streamlit session state and call its tab_text.logics.TextColumn.find_text_cols() method in order to find all text columns.
    Then it will display a Streamlit select box with the list of text columns found.
    Once the user select a text column from the select box, it will call the tab_text.logics.TextColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_text.logics.TextColumn.get_summary() as a Streamlit Table
    - the graph from tab_text.logics.TextColumn.histogram using Streamlit.altair_chart()
    - the results of tab_text.logics.TextColumn.frequent using Streamlit.write
 
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
    # Instantiate TextColumn and call find_text_cols method
    text_column = TextColumn(file_path=file_path, df=df)
    text_column.find_text_cols()

    # Display select box for text columns
    selected_column = st.selectbox('Select Text Column', text_column.cols_list)

    if selected_column:
        # Call set_data method with selected column
        text_column.set_data(selected_column)


        # Display Expander container with results
        with st.expander('Text Column Summary'):
            # Display summary table
            st.table(text_column.get_summary())

            # Display histogram using altair_chart
            st.altair_chart(text_column.barchart, use_container_width=True)

            # Display frequent values
            st.write('Most frequent values:')
            st.write(text_column.frequent)