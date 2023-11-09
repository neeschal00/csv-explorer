import pandas as pd
import altair as alt
import datetime
class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column from a dataframe of datetime data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are text type (default set to empty list)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a serie (optional)
    -> n_missing (int): Number of missing values of a serie (optional)
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> n_weekend (int): Number of times a serie has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a serie has dates not falling during weekend (optional)
    -> n_future (int): Number of times a serie has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a serie has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a serie has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Dataframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    
    def find_date_cols(self):
        """
        --------------------
        Description
        --------------------
        -> find_date_cols (method): Class method that will load the uploaded CSV file as Pandas DataFrame and store it as attribute (self.df) if it hasn't been provided before.
        Then it will find all columns of datetime data type. If it can't find any datetime then it will look for all columns of text time. Then it will store the results in the relevant attribute (self.cols_list).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.df is None and self.file_path:
            # Load the CSV file as a Pandas DataFrame
            try:
                self.df = pd.read_csv(self.file_path)
            except UnicodeDecodeError:
                self.df = pd.read_csv(self.file_path,encoding = "ISO-8859-1")

        if self.df is not None:
            # Find columns with datetime data type
            datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()

            if datetime_cols:
                # If datetime columns are found, store them in cols_list
                self.cols_list = datetime_cols
            else:
                # If no datetime columns are found, look for columns with text data that might represent dates
                text_cols = self.df.select_dtypes(include=['object']).columns.tolist()
                potential_date_cols = []

                # Add your logic to identify text columns that represent dates
                for col in text_cols:
                    try:
                        pd.to_datetime(self.df[col], errors='raise')
                        potential_date_cols.append(col)
                    except (ValueError, TypeError):
                        pass  # Ignore columns that cannot be converted to datetime

                self.cols_list = potential_date_cols
        

    def set_data(self, col_name):
        """
        --------------------
        Description
        --------------------
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that sets the self.serie attribute with the relevant column from the dataframe and then computes all requested information from self.serie to be displayed in the Date section of Streamlit app 

        --------------------
        Parameters
        --------------------
        -> col_name (str): Name of the text column to be analysed

        --------------------
        Returns
        --------------------
        -> None
        """

        if self.df is not None:
            if col_name in self.df.columns:
                # Extract the specified column and assign it to self.serie
                self.serie = self.df[col_name]
                
                # Check if the series contains datetime data; if not, convert it
                if self.serie.dtype != 'datetime64':
                    self.convert_serie_to_date()

                # Now you can call the various methods to compute the required information
                self.set_unique()
                self.set_missing()
                self.set_min()
                self.set_max()
                self.set_weekend()
                self.set_weekday()
                self.set_future()
                self.set_empty_1900()
                self.set_empty_1970()
                self.set_barchart()
                self.set_frequent()
            else:
                # Handle the case where col_name does not exist in the DataFrame
                print(f"Column '{col_name}' does not exist in the DataFrame.")
        else:
            # Handle the case where the DataFrame is not loaded
            print("DataFrame is not loaded. Use 'find_date_cols' to load the DataFrame.")





        

    def convert_serie_to_date(self):
        """
        --------------------
        Description
        --------------------
        -> convert_serie_to_date (method): Class method that convert a Pandas Series to datetime data type and store the results in the relevant attribute (self.serie).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
            try:
                # Attempt to convert the series to datetime using the 'infer_datetime_format' option
                self.serie = pd.to_datetime(self.serie, errors='coerce', infer_datetime_format=True)
            except (ValueError, TypeError):
                # Handle the case where conversion fails
                print("Error converting the series to datetime.")
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for conversion.")
        

    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none 

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (bool): Flag stating if the serie is empty or not

        """
        if self.serie is None or len(self.serie) == 0:
            return True
        else:
            return False

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie and store the results in the relevant attribute(self.n_unique).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
            # Calculate the number of unique values in the series
            self.n_unique = self.serie.nunique()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie and store the results in the relevant attribute(self.n_missing).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
        # Calculate the number of missing (NaN) values in the series
            self.n_missing = self.serie.isna().sum()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_min).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
            # Calculate the minimum value in the series
            self.col_min = self.serie.min()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_max).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
        # Calculate the maximum value in the series
            self.col_max = self.serie.max()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a serie has dates falling during weekend and store the results in the relevant attribute(self.n_weekend).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
        # Calculate the number of times dates fall during the weekend (Saturday or Sunday)
            weekend_count = self.serie.dt.dayofweek.isin([5, 6]).sum()
            self.n_weekend = weekend_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend and store the results in the relevant attribute(self.n_weekday).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Calculate the number of times dates do not fall during the weekend (Monday to Friday)
            weekday_count = (~self.serie.dt.dayofweek.isin([5, 6])).sum()
            self.n_weekday = weekday_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a serie has dates falling in the future and store the results in the relevant attribute(self.n_future).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Get the current date
            current_date = datetime.datetime.now()

            # Calculate the number of times dates fall in the future
            future_count = (self.serie > current_date).sum()
            self.n_future = future_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        
    
    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' and store the results in the relevant attribute(self.n_empty_1900).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Calculate the number of times dates are equal to '1900-01-01'
            empty_1900_count = (self.serie == '1900-01-01').sum()
            self.n_empty_1900 = empty_1900_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a serie has only digit characters and store the results in the relevant attribute(self.n_empty_1970).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Convert the datetime series to a string in 'YYYY-MM-DD' format
            date_string = self.serie.dt.strftime('%Y-%m-%d')

            # Calculate the number of times dates are equal to '1970-01-01'
            empty_1970_count = (date_string == '1970-01-01').sum()
            self.n_empty_1970 = empty_1970_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie and store the results in the relevant attribute(self.barchart).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
            # Create a Pandas DataFrame with the counts for each unique value
            value_counts_df = self.serie.value_counts().reset_index()
            value_counts_df.columns = ['value', 'count']

            # Create an Altair bar chart
            chart = alt.Chart(value_counts_df).mark_bar().encode(
                x='value',
                y='count',
                tooltip=['value', 'count']
            ).properties(
                title='Bar Chart: Count of Unique Values'
            )

            # Store the Altair bar chart in the self.barchart attribute
            self.barchart = chart
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie and store the results in the relevant attribute(self.frequent).

        --------------------
        Parameters
        --------------------
        -> end (int):
            Parameter indicating the maximum number of values to be displayed

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.serie is not None:
            # Calculate the value counts for each unique value in the series
            value_counts = self.serie.value_counts()

            # Select the top 'end' most frequent values
            frequent_values_df = value_counts.head(end).reset_index()
            frequent_values_df.columns = ['value', 'occurrence']

            # Calculate the percentage of occurrence
            frequent_values_df['percentage'] = (frequent_values_df['occurrence'] / len(self.serie)) * 100

            # Store the DataFrame in the self.frequent attribute
            self.frequent = frequent_values_df
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def get_summary(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (pd.DataFrame): Formatted dataframe to be displayed on the Streamlit app

        """
        if self.serie is not None:
            # Create a DataFrame with the summary information
            summary_df = pd.DataFrame({
                'Description': ['Number of Unique Values', 'Number of Missing Values', 'Minimum Value', 'Maximum Value',
                                'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Future Dates',
                                'Number of Dates equal to 1900-01-01', 'Number of Dates equal to 1970-01-01'],
                'Value': [self.n_unique, self.n_missing, self.col_min, self.col_max,
                        self.n_weekend, self.n_weekday, self.n_future, self.n_empty_1900, self.n_empty_1970]
            })

            # Add a row for each frequent value
            # if not self.frequent.empty:
            #     frequent_rows = self.frequent[['occurrence', 'value']].apply(
            #         lambda x: f"{x['value']} ({x['occurrence']} occurrences)", axis=1
            #     )
            #     summary_df = pd.concat([summary_df, pd.Series(frequent_rows, name='Value')], ignore_index=True)

            summary_df = summary_df.astype(str)
            return summary_df
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
            return pd.DataFrame(columns=['Description', 'Value'])





