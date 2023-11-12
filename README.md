# <project title>

## Description


## How to Setup

**Requirements:** 
Python Version: 3.9


**Setup:**
- Clone the repository.

- CD to the project directory:

```
cd "At3_group_26-csv-explorer"
```

- Create a Python Virtual Environment:

```
python -m venv venv
```

- Activate the virtual Environment:

```
venv\Scripts\activate
```

or if **linux** or **mac**

```
source venv/bin/activate
```

- Install Packages

```
pip install -r requirements.txt
```
- Is ready to Run

## How to Run the Program
- The **streamlit_app.py** module consists of the streamlit main app configuration and the streamlit app is run from this code.
```
streamlit run app\streamlit_app.py
```
- Upload a CSV file using the file uploader.
- Explore the different tabs for DataFrame, numeric series, text series, and datetime series.
- Choose which column to select from to visulaize each column in different tabs.
- Expand the components as per the need.


## Project Structure
- `csv/`: Directory to store uploaded CSV files.
- `main.py`: Main application file.
- `tab_df/`: Folder containing the logic and display functions for the DataFrame tab.
- `tab_num/`: Folder containing the logic and display functions for the numeric series tab.
- `tab_text/`: Folder containing the logic and display functions for the text series tab.
- `tab_date/`: Folder containing the logic and display functions for the datetime series tab.
