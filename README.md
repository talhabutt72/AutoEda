# AutoEDA

A Streamlit app for quick exploratory data analysis and basic preprocessing. Upload a CSV or Excel file, inspect it, make a few plots, and clean it, without writing code.

## Demo

Live app: https://autoeda-by-talha.streamlit.app/

## What it does

**Inspect the data**
- Dataset preview, shape, and column data types
- Value counts and number of unique values for any column
- Missing values and their percentage in each column
- Summary statistics (`describe`)
- Outlier counts using the IQR method
- Duplicate row detection
- Correlation matrix for numerical columns

**Plots**
- Pairplot of the numeric columns (top 5 by variance, 500-row sample)
- Bar chart of the first numeric column by the first categorical column

**Preprocessing**
- Fill or drop missing values
- Encode categorical columns: one-hot, label, or target encoding

## How to run it locally

1. Clone the repo: `git clone https://github.com/talhabutt72/AutoEda.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `streamlit run app.py`

## Tech stack

Python, Streamlit, pandas, seaborn, matplotlib, scikit-learn, category_encoders

## Limitations

- Preprocessing steps cannot be undone. Re-upload the file to start over.
- Missing values: if there are fewer than 150 and at least 5,000 rows, the rows with nulls are dropped. Otherwise numeric columns are filled with the median and text columns with the mode.
- Outliers are detected and counted, but not removed.
- The bar chart only uses the first categorical and first numeric column.
- Not tested on very large files.

## Author

Talha, BS Data Science student
GitHub: https://github.com/talhabutt72
LinkedIn: https://www.linkedin.com/in/talhabutt7810/
