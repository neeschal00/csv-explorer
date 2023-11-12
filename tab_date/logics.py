import pandas as pd
import altair as alt
import datetime
class DateColumn:
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
        
        if self.df is None and self.file_path:
            
            try:
                self.df = pd.read_csv(self.file_path)
            except UnicodeDecodeError:
                self.df = pd.read_csv(self.file_path,encoding = "ISO-8859-1")

        if self.df is not None:
            
            datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()

            if datetime_cols:
                self.cols_list = datetime_cols
            else:
                
                text_cols = self.df.select_dtypes(include=['object']).columns.tolist()
                potential_date_cols = []

                
                for col in text_cols:
                    try:
                        pd.to_datetime(self.df[col], errors='raise')
                        potential_date_cols.append(col)
                    except (ValueError, TypeError):
                        pass  

                self.cols_list = potential_date_cols
        

    def set_data(self, col_name):

        if self.df is not None:
            if col_name in self.df.columns:
                
                self.serie = self.df[col_name]
                
                
                if self.serie.dtype != 'datetime64':
                    self.convert_serie_to_date()

                
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
                
                print(f"Column '{col_name}' does not exist in the DataFrame.")
        else:
            
            print("DataFrame is not loaded. Use 'find_date_cols' to load the DataFrame.")





        

    def convert_serie_to_date(self):
        
        if self.serie is not None:
            try:
                self.serie = pd.to_datetime(self.serie, errors='coerce', infer_datetime_format=True)
            except (ValueError, TypeError):
                
                print("Error converting the series to datetime.")
        else:
            
            print("Series is empty or None. Use 'set_data' to specify the column for conversion.")
        

    def is_serie_none(self):
        
        if self.serie is None or len(self.serie) == 0:
            return True
        else:
            return False

    def set_unique(self):
        
        if self.serie is not None:
            # Calculate the number of unique values in the series
            self.n_unique = self.serie.nunique()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_missing(self):
        
        if self.serie is not None:
        # Calculate the number of missing (NaN) values in the series
            self.n_missing = self.serie.isna().sum()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_min(self):
        
        if self.serie is not None:
            # Calculate the minimum value in the series
            self.col_min = self.serie.min()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_max(self):
        
        if self.serie is not None:
        # Calculate the maximum value in the series
            self.col_max = self.serie.max()
        else:
            # Handle the case where the series is empty or None
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
        

    def set_weekend(self):
        
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
        # Calculate the number of times dates fall during the weekend (Saturday or Sunday)
            weekend_count = self.serie.dt.dayofweek.isin([5, 6]).sum()
            self.n_weekend = weekend_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_weekday(self):
        
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Calculate the number of times dates do not fall during the weekend (Monday to Friday)
            weekday_count = (~self.serie.dt.dayofweek.isin([5, 6])).sum()
            self.n_weekday = weekday_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_future(self):
        
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
        
        if self.serie is not None and self.serie.dtype == 'datetime64[ns]':
            # Calculate the number of times dates are equal to '1900-01-01'
            empty_1900_count = (self.serie == '1900-01-01').sum()
            self.n_empty_1900 = empty_1900_count
        else:
            # Handle the case where the series is empty, None, or not a datetime series
            print("Series is empty, None, or not a datetime series. Use 'set_data' to specify a valid datetime column.")
        

    def set_empty_1970(self):
        
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
        
        if self.serie is not None:
            
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
        
        if self.serie is not None:
            
            summary_df = pd.DataFrame({
                'Description': ['Number of Unique Values', 'Number of Missing Values', 'Minimum Value', 'Maximum Value',
                                'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Future Dates',
                                'Number of Dates equal to 1900-01-01', 'Number of Dates equal to 1970-01-01'],
                'Value': [self.n_unique, self.n_missing, self.col_min, self.col_max,
                        self.n_weekend, self.n_weekday, self.n_future, self.n_empty_1900, self.n_empty_1970]
            })

            
            summary_df = summary_df.astype(str)
            return summary_df
        else:
            
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
            return pd.DataFrame(columns=['Description', 'Value'])





