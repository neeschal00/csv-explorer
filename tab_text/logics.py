import pandas as pd
import altair as alt

class TextColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty  = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    
    def find_text_cols(self):
        if self.df is None and self.file_path is not None:
            try:
                self.df = pd.read_csv(self.file_path)
            except UnicodeDecodeError:
                self.df = pd.read_csv(self.file_path,encoding = "ISO-8859-1")
        if self.df is not None:
            self.cols_list = [col for col in self.df.columns if self.df[col].dtype == 'object']
        

    def set_data(self, col_name):
        if col_name in self.cols_list:
            self.serie = self.df[col_name]
            
            self.convert_serie_to_text()
            self.set_unique()
            self.set_missing()
            self.set_empty()
            self.set_mode()
            self.set_whitespace()
            self.set_lowercase()
            self.set_uppercase()
            self.set_alphabet()
            self.set_digit()
            self.set_barchart()
            self.set_frequent()


    def convert_serie_to_text(self):
        if not self.is_serie_none():
            self.serie = self.serie.astype(str)
        

    def is_serie_none(self):
        return self.serie is None or self.serie.empty

    def set_unique(self):
        if not self.is_serie_none():
            self.n_unique = len(self.serie.unique())
        

    def set_missing(self):
        if not self.is_serie_none():
            self.n_missing = self.serie.isnull().sum()
        

    def set_empty(self):
        if not self.is_serie_none():
            self.n_empty = (self.serie == '').sum()
        

    def set_mode(self):
        if not self.is_serie_none():
            self.n_mode = self.serie.mode().iloc[0] if not self.serie.mode().empty else None
        

    def set_whitespace(self):
        if not self.is_serie_none():
            self.n_space = self.serie.str.isspace().sum()
        

    def set_lowercase(self):
        if not self.is_serie_none():
            self.n_lower = self.serie.str.islower().sum()

    def set_uppercase(self):
        if not self.is_serie_none():
            self.n_upper = self.serie.str.isupper().sum()
        
    
    def set_alphabet(self):
        if not self.is_serie_none():
            self.n_alpha = self.serie.str.isalpha().sum()
        

    def set_digit(self):
        if not self.is_serie_none():
            self.n_digit = self.serie.str.isdigit().sum()
        

    def set_barchart(self):  
        value_counts_df = self.serie.value_counts().reset_index()
        value_counts_df.columns = ['value', 'count']
        if not self.is_serie_none():
            chart = alt.Chart(value_counts_df).mark_bar().encode(
                alt.X("value" + ':N', title="value"),
                alt.Y('count():Q', title='Count'),
                tooltip=['value', 'count']

            )
            
            self.barchart = chart

        
      
    def set_frequent(self, end=20):
        if not self.is_serie_none():
            value_counts = self.serie.value_counts().head(end).reset_index()
            value_counts.columns = ['value', 'occurrence']
            value_counts['percentage'] = (value_counts['occurrence'] / len(self.serie)) * 100
            self.frequent = value_counts
        

    def get_summary(self):
        if not self.is_serie_none():
            summary_data = {
                'Description': ['Number of Unique Values', 'Number of Missing Values', 'Number of Empty Values',
                                'Mode', 'Number of Whitespace Values', 'Number of Lowercase Values',
                                'Number of Uppercase Values', 'Number of Alphabetical Values',
                                'Number of Digit Values'],
                'Value': [self.n_unique, self.n_missing, self.n_empty, self.n_mode, self.n_space, self.n_lower,
                        self.n_upper, self.n_alpha, self.n_digit]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df = summary_df.astype(str)
            return summary_df
        else:
            print("Series is empty or None. Use 'set_data' to specify the column for analysis.")
            return pd.DataFrame(columns=['Description', 'Value'])
