import pandas as pd


class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None

    def set_data(self):
        
        if not self.is_df_none():
            
            self.set_columns()
            self.set_dimensions()
            self.set_duplicates()
            self.set_missing()
            self.set_numeric()
            self.set_text()
            self.set_table()

    
    def set_df(self):
        
        if self.df is None:
            
            try:
                self.df = pd.read_csv(self.file_path)
            except UnicodeDecodeError:
                self.df = pd.read_csv(self.file_path,encoding = "ISO-8859-1")


    def is_df_none(self):
        
        if self.df.empty:
            return True
        if self.df is None:
            return True
        return False
        

    def set_columns(self):
        
        if not self.is_df_none():
            self.cols_list = self.df.columns.tolist() 
        

    def set_dimensions(self):
        
        if not self.is_df_none():
            self.n_rows, self.n_cols = self.df.shape

    def set_duplicates(self):
        
        if not self.is_df_none():
            self.n_duplicates = self.df.duplicated().sum()
        

    def set_missing(self):
        
        if not self.is_df_none():
            self.n_missing = self.df.isnull().sum().sum() 


    def set_numeric(self):
        
        if not self.is_df_none():
            numeric_columns = self.df.select_dtypes(include=['number'])
            self.n_num_cols = numeric_columns.shape[1]

    def set_text(self):
        
        if not self.is_df_none():
            text_columns = self.df.select_dtypes(include=['object', 'string'])
            self.n_text_cols = text_columns.shape[1]
        

    def get_head(self, n=5):
        
        if not self.is_df_none():
            return self.df.head(n)
        else:
            return pd.DataFrame()
        

    def get_tail(self, n=5):
        
        if not self.is_df_none():
            return self.df.tail(n)
        else:
            return pd.DataFrame()
        

    def get_sample(self, n=5):
        
        if not self.is_df_none():
            return self.df.sample(n)
        else:
            return pd.DataFrame()
        

    def set_table(self):
        
        if not self.is_df_none():
            
            data_types = self.df.dtypes
            
            mem_usage = self.df.memory_usage(deep=True)
            mem_usage = mem_usage[mem_usage.index.isin(data_types.index)]
            
            self.table = pd.DataFrame({
                'Column Name': data_types.index,
                'Data Type': data_types.values,
                'Memory Usage': mem_usage.values
            })


    def get_summary(self):
        
        summary_data = {
            'Description': [
                'Number of Rows',
                'Number of Columns',
                'Number of Duplicates',
                'Number of Missing Values',
                'Number of Numeric Columns',
                'Number of Text Columns',
            ],
            'Value': [
                self.n_rows,
                self.n_cols,
                self.n_duplicates,
                self.n_missing,
                self.n_num_cols,
                self.n_text_cols,
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        
        return summary_df