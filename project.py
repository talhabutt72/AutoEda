import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Auto EDA (Exploratory Data Analysis)")

file = st.file_uploader("Enter your CSV or Excel dataset", type=["csv", "xlsx"])

dataset = None

if file is None:

    st.warning("The file is not uploaded")
    st.stop()

elif file is not None:
    st.success("File uploaded successfully.")

    # load the file only once, then keep working on the saved copy
    # (streamlit reruns the whole script on every click)
    if st.session_state.get("file_name") != file.name:
        file.seek(0)

        if file.name.endswith(".csv"):
            st.write("The Dataset is in the CSV Format.")
            st.session_state.df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            st.write("The Dataset is in the Excel Format.")
            st.session_state.df = pd.read_excel(file)

        st.session_state.file_name = file.name

    dataset = st.session_state.df


if dataset is not None:
    st.write("### Dataset Preview:")
    st.dataframe(dataset.head(5))
else:
    st.warning("Dataset is not uploaded")
    st.stop()


# SideBar

st.sidebar.header("Welcome to Auto EDA.")

st.sidebar.markdown("#### Graphs imp before EDA")
graph = st.sidebar.selectbox("Graphs", ["Select Please", "Pairplot (Numeric Data)", "Bar Chart for Categorical Columns"])

if graph == "Pairplot (Numeric Data)":

    numeric_cols = dataset.select_dtypes(include=["number"]).columns

    if len(numeric_cols) > 5:
        top_numeric_cols = dataset[numeric_cols].var().nlargest(5).index

    else:

        top_numeric_cols = numeric_cols

    data_size = min(500, len(dataset))
    sample_data = dataset.sample(data_size, random_state=42)

    fig = sns.pairplot(sample_data[top_numeric_cols], corner=True)
    st.pyplot(fig.figure)

elif graph == "Bar Chart for Categorical Columns":

    # Select categorical and numeric columns
    cat_cols = dataset.select_dtypes(include=["category", "object", "string"]).columns
    num_cols = dataset.select_dtypes(include=["number"]).columns

    if len(cat_cols) == 0 or len(num_cols) == 0:
        st.warning("No categorical or numerical columns found in the dataset.")
    else:
        x_col = cat_cols[0]  # Select first categorical column
        y_col = num_cols[0]  # Select first numeric column

        # Create a figure
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=x_col, y=y_col, data=dataset, ax=ax, palette="coolwarm")

        # Customize labels
        ax.set_title(f"Bar Chart of {y_col} by {x_col}", fontsize=14)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        plt.xticks(rotation=45)

        # Show the plot in Streamlit
        st.pyplot(fig)


st.sidebar.markdown("#### What you want to check.")
action = st.sidebar.selectbox("Actions", ["Select Please", "Size of the dataset", "Show data types of each column", "Display value counts and no of unique value counts", "Highlight missing data and its percentage in each column", "Describe the Dataset", "Outliers Detection(IQR)", "Duplicates Detection", "Correlation Matrix (for numerical features)"])

# Writing Actions

if action == "Size of the dataset":
    st.write("Rows of dataset", dataset.shape[0], "|\n", "Columns or Feature of dataset", dataset.shape[1])

elif action == "Show data types of each column":
    dtype_dict = {}

    for i in dataset.columns:
        col_dtype = str(dataset[i].dtype)

        if col_dtype in dtype_dict:
            dtype_dict[col_dtype].append(i)
        else:
            dtype_dict[col_dtype] = [i]

    # Display the result
    st.write("### Data Types of Columns:")
    st.write(dtype_dict)

elif action == "Display value counts and no of unique value counts":

    col = st.text_input("Enter the name of the Column")
    if col:
        if col in dataset.columns:
            st.text(dataset[col].value_counts())
            st.write(f"There are {dataset[col].nunique()} unique values in {col}")
        else:
            st.error(f"The {col} does not exist in your dataset, please cross check.")
    else:
        st.warning("Please enter the column name before proceeding")

elif action == "Highlight missing data and its percentage in each column":

    for col in dataset.columns:
        st.write(f"The {col} have {dataset[col].isnull().sum()} Null values | {round((dataset[col].isnull().sum() / len(dataset[col])) * 100, 2)} in (%)")

elif action == "Describe the Dataset":
    st.write(dataset.describe())

elif action == "Outliers Detection(IQR)":

    for col in dataset.select_dtypes(include=["number"]).columns:
        Q1 = dataset[col].quantile(0.25)
        Q3 = dataset[col].quantile(0.75)

        IQR = Q3 - Q1

        Lower_Bound = Q1 - 1.5 * IQR
        Upper_Bound = Q3 + 1.5 * IQR

        outliers = (dataset[col] < Lower_Bound) | (dataset[col] > Upper_Bound)
        outlier_count = outliers.sum()

        st.write(f"Total Outliers in '{col}': {outlier_count}")

elif action == "Duplicates Detection":
    length = dataset.duplicated().sum()
    if length > 0:
        st.write(f"Total duplicated rows: {length}")
        st.write(dataset[dataset.duplicated()])

    else:
        st.success("No duplicate rows found in the dataset.")

elif action == "Correlation Matrix (for numerical features)":
    num_data = dataset.select_dtypes(include=["number"])

    if num_data.shape[1] < 2:
        st.warning("Need at least 2 numerical columns for a correlation matrix.")
    else:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(num_data.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)


# filling missing value or dropping, normalization, encoding, remove duplicates, removing Outliers.
st.sidebar.markdown("#### Perform Eda Steps.")
step = st.sidebar.selectbox("Steps", ["Select Please", "Filling Null values or dropping.", "Encoding"])

if step == "Filling Null values or dropping.":
    if dataset.isnull().sum().sum() > 0:
        if dataset.isnull().sum().sum() < 150 and dataset.shape[0] >= 5000:
            dataset = dataset.dropna(axis=0)
            st.success("Few missing values, so the rows with nulls were dropped.")
        else:
            st.text("You have too much missing values, so, they are filled.")
            for col in dataset.columns:
                if dataset[col].isnull().sum() > 0:
                    if pd.api.types.is_numeric_dtype(dataset[col]):
                        dataset[col] = dataset[col].fillna(dataset[col].median())
                    else:
                        dataset[col] = dataset[col].fillna(dataset[col].mode()[0])
            st.success("Missing values filled (median for numbers, mode for text).")

        st.session_state.df = dataset

    else:
        st.info("There is not any Null Value Represent in the Dataset.")

elif step == "Encoding":

    encoding_methods = ["Select Method for encoding", "OneHotEncoding", "Label Encoding", "Target Encoding"]

    target = st.text_input("Enter your target column name (for Target Encoding only):")

    for col in dataset.select_dtypes(include=["object", "string", "category"]).columns:
        if col != target:

            encoding = st.selectbox(f"Method for '{col}'", encoding_methods, key=f"encode_{col}")
            if encoding != "Select Method for encoding":

                if encoding == "OneHotEncoding":
                    dataset = pd.get_dummies(data=dataset, columns=[col])

                elif encoding == "Label Encoding":
                    from sklearn.preprocessing import LabelEncoder
                    encorder = LabelEncoder()
                    dataset[col] = encorder.fit_transform(dataset[col])
                    st.text(dataset[col].sample(2))

                elif encoding == "Target Encoding":

                    if target in dataset.columns:

                        import category_encoders as ce

                        encoder = ce.TargetEncoder()

                        dataset[col] = encoder.fit_transform(dataset[col], dataset[target])[col]
                        st.text(dataset[col].sample(2))
                    else:
                        st.error("Please enter a valid target column!")
                        continue

                st.session_state.df = dataset
                st.success(f"'{col}' encoded using {encoding}.")
            else:
                st.warning(f"Please select an encoding method for {col}.")

    st.text(dataset.sample(5))
