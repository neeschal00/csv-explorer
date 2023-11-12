import pandas as pd
import altair as alt


class NumericColumn:
   
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_num_cols(self):
        
        if self.df is None and self.file_path is not None:
            
            try:
                self.df = pd.read_csv(self.file_path)
            except UnicodeDecodeError:
                self.df = pd.read_csv(self.file_path,encoding = "ISO-8859-1")

        if self.df is not None:
            
            self.cols_list = self.df.select_dtypes(include=['number']).columns.tolist()
        

    def set_data(self, col_name):
        

        if col_name in self.cols_list:
            
            self.serie = self.df[col_name]

            
            if not self.is_serie_none():
                
                self.set_unique()
                self.set_missing()
                self.set_mean()
                self.set_std()
                self.set_min()
                self.set_max()
                self.set_median()
                self.set_zeros()
                self.set_negatives()
                self.set_histogram()
                self.set_frequent()
        else:
            raise ValueError(f"Column '{col_name}' is not numeric or doesn't exist in the DataFrame.")







    def convert_serie_to_num(self):
        
        if not self.is_serie_none():
            try:
                # Convert the Pandas Series to a numeric data type
                self.serie = pd.to_numeric(self.serie, errors='coerce')
            except ValueError:
                # Handle any conversion errors
                # You can add error handling logic here, e.g., logging
                pass
        

    def is_serie_none(self):
        
        if self.serie is None or self.serie.empty:
            self.serie_empty = True
        else:
            self.serie_empty = False
        return self.serie_empty
        

    def set_unique(self):
        
        if not self.is_serie_none():
            #count unique values 
            self.n_unique = len(self.serie.unique())
        

    def set_missing(self):
        
        if not self.is_serie_none():
            self.n_missing = self.serie.isna().sum()
        

    def set_zeros(self):
        
        if not self.is_serie_none():
            self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        
        if not self.is_serie_none():
            self.n_negatives = (self.serie < 0).sum()
        

    def set_mean(self):
        
        if not self.is_serie_none():
            self.col_mean = self.serie.mean()
        

    def set_std(self):
        
        if not self.is_serie_none():
            self.col_std = self.serie.std()
        
    
    def set_min(self):
        
        if not self.is_serie_none():
            self.col_min = self.serie.min()
        

    def set_max(self):
        
        if not self.is_serie_none():
            self.col_max = self.serie.max()

    def set_median(self):
        if not self.is_serie_none():
            self.col_median = self.serie.median()

    def set_histogram(self):
        if not self.is_serie_none():
            
            chart = alt.Chart(self.df)
            chart = chart.mark_bar().encode(
                alt.X(f'{self.serie.name}:O', bin=alt.Bin(maxbins=20), title=self.serie.name),
                alt.Y('count()', title='Count')
            )
            
            self.histogram = chart
        

    def set_frequent(self, end=20):
        
        if not self.is_serie_none():
            
            frequent_values = self.serie.value_counts().head(end).reset_index()
            frequent_values.columns = ['value', 'occurrence']
            
            total_occurrences = self.serie.count()
            frequent_values['percentage'] = (frequent_values['occurrence'] / total_occurrences) * 100
            
            self.frequent = frequent_values
        
    def get_summary(self,):
        
        summary_data = {
            "Description": [
                "Number of Unique Values",
                "Number of Missing Values",
                "Average (Mean)",
                "Standard Deviation",
                "Minimum Value",
                "Maximum Value",
                "Median Value",
                "Number of Zeros",
                "Number of Negatives",
            ],
            "Value": [
                self.n_unique if not self.is_serie_none() else "N/A",
                self.n_missing if not self.is_serie_none() else "N/A",
                self.col_mean if not self.is_serie_none() else "N/A",
                self.col_std if not self.is_serie_none() else "N/A",
                self.col_min if not self.is_serie_none() else "N/A",
                self.col_max if not self.is_serie_none() else "N/A",
                self.col_median if not self.is_serie_none() else "N/A",
                self.n_zeros if not self.is_serie_none() else "N/A",
                self.n_negatives if not self.is_serie_none() else "N/A",
            ],
        }

        summary_df = pd.DataFrame(summary_data)
        
        return summary_df
