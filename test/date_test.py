import unittest
import pandas as pd
from tab_date.logics import DateColumn  

class TestDateColumn(unittest.TestCase):
    def setUp(self):
        
        data = {
            'date_column_1': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'date_column_2': ['01/01/2022', '01/02/2022', '01/03/2022'],
            'non_date_column': ['apple', 'banana', 'orange']
        }
        self.temp_csv_path = 'temp_test_csv.csv'
        pd.DataFrame(data).to_csv(self.temp_csv_path, index=False)

    def tearDown(self):
        
        import os
        os.remove(self.temp_csv_path)

    def test_find_date_cols(self):
        
        date_col_instance = DateColumn(file_path=self.temp_csv_path)

        # Call find_date_cols method
        date_col_instance.find_date_cols()

        # Assert that cols_list contains the expected date columns
        expected_date_cols = ['date_column_1', 'date_column_2']
        self.assertEqual(date_col_instance.cols_list, expected_date_cols)

    def test_set_data(self):
        # Initialize DateColumn instance with the temporary CSV file
        date_col_instance = DateColumn(file_path=self.temp_csv_path)

        # Call find_date_cols method
        date_col_instance.find_date_cols()

        # Test set_data method with a date column
        date_col_instance.set_data('date_column_1')

        # Assert that the serie attribute is not None after calling set_data
        self.assertIsNotNone(date_col_instance.serie)

        # Test set_data method with a non-existent column
        date_col_instance.set_data('non_existent_column')

        # Assert that a message is printed indicating the column does not exist
        # You can modify this part based on your actual print statements
        self.assertEqual(date_col_instance.get_summary().iloc[0]['Value'], 0)

if __name__ == '__main__':
    unittest.main()
