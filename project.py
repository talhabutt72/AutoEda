import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Auto Eda(Explotry data Analysis)")

file = st.file_uploader("Enter your CSV or Excel dataset", type=["csv", "xlsx"])

dataset = None 

if file is None:
    
    st.warning("The file is not uploded")
    st.stop()

elif file is not None:
    # st.session_state["uploaded_file"] = file
    st.success("File uploaded is successfully.")


# if "uploaded_file" in st.session_state:
#     file = st.session_state["uploaded_file"]
    
    file.seek(0)

    if file.name.endswith(".csv"):
        st.write("The Dataset is in the CSV Format.")
        dataset = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        st.write("The Dataset is in the Excel Format.")
        dataset = pd.read_excel(file)
            

if dataset is not None:
    st.write("### Dataset Preview:")
    st.dataframe(dataset.head(5))
else:
    st.warning("Dataset is not uploaded")
    

# SideBar

st.sidebar.header("Welcome to Auto Encode.")

st.sidebar.markdown("#### Graphs imp before EDA")
graph = st.sidebar.selectbox("Graphs", ["Select Please", "Pairplot (Numeric Data)", "Bar Chart for Categorical Columns"])

if graph == "Pairplot (Numeric Data)":
    
    numeric_cols = dataset.select_dtypes(include = ["number"]).columns
    
    if len(numeric_cols) > 5:
        top_numeric_cols = dataset[numeric_cols].var().nlargest(5).index
    
    else:
        
        top_numeric_cols = numeric_cols
    
    data_size = min(500, len(dataset))
    sample_data = dataset.sample(data_size, random_state = 42)
    
    fig = sns.pairplot(sample_data[top_numeric_cols], corner = True)
    st.pyplot(fig)

elif graph == "Bar Chart for Categorical Columns":


    # Select categorical and numeric columns
    cat_cols = dataset.select_dtypes(include=["category", "object"]).columns
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
action = st.sidebar.selectbox("Actions", ["Select Please","Size of the dataset", "Show data types of each column", "Display value counts and no of unique value counts","Highlight missing data and its percentage in each column", "Describe the Dataset", "Outliers Detection(IQR)", "Duplicates Detection", "Correlation Matrix (for numerical features)" ])

# Wrinting Acctions

if action == "Size of the dataset":
    st.write("Rows of dataset",dataset.shape[0], "|\n", "Columns or Feature of dataset",dataset.shape[1])
    # st.write("Columns or Feature of dataset",dataset.shape[1])

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
            st.error(f"The {col} is not exits in Your dataset, please cross check.")
    else:
        st.warning("Please anter the column name before proceding")

elif action == "Highlight missing data and its percentage in each column":
    
    for col in dataset.columns:
        st.write(f"The {col} have {dataset[col].isnull().sum()} Null values | {(dataset[col].isnull().sum() / len(dataset[col])) * 100} in (%)")
        
elif action == "Describe the Dataset":
    st.write(dataset.describe())

elif action == "Outliers Detection(IQR)":
    
    for col in dataset.columns:
        if dataset[col].dtype == "int64" or dataset[col].dtype == "float64":
            Q1 = dataset[col].quantile(0.25)
            Q3 = dataset[col].quantile(0.75)
            
            IQR =  Q3 - Q1
            
            Lower_Bound = Q1 - 1.5 * IQR
            Upper_Bound = Q3 + 1.5 * IQR

            # st.write(IQR)
            outliers = (dataset[col] < Lower_Bound) | (dataset[col] > Upper_Bound)


            # outlier_row = col[outliers]
            outlier_count = outliers.sum()
            
            st.write(f"Total Outliers in '{col}': {outlier_count}")
            # st.write(dataset[outliers])
            # st.write(f"Total number of outliers: {len(outliers)}")

elif action == "Duplicates Detection":
    length = dataset.duplicated().sum()
    # st.write(length)
    if length > 0:
        st.write(f"Total dublicated rows: {length}")
        st.write(dataset[dataset.duplicated()])

    else:
        st.success("No duplicate rows found in the dataset.")



# filling missing value or dropping, normalization, encoding, remove duplicates, removing Outliers.
st.sidebar.markdown("#### Perform Eda Steps.")
step = st.sidebar.selectbox("Steps", ["Select Please", "Filling Null values or dropping.","Encoding"])

# st.stop()

if step == "Filling Null values or dropping.":
    if dataset.isnull().sum().sum() > 0:
        if dataset.isnull().sum().sum() < 150 and dataset.shape[0] >= 5000:
            dataset = dataset.dropna(axis = 0)
        else:
            st.text("You have too much missing values, so, you have to fill this.")
            for col in dataset.columns:
                if dataset[col].dtype == "int64" or dataset[col].dtype == "float64":
                    Q1 = dataset[col].quantile(0.25)
                    Q3 = dataset[col].quantile(0.75)
                    
                    IQR =  Q3 - Q1
                    
                    Lower_Bound = Q1 - 1.5 * IQR
                    Upper_Bound = Q3 + 1.5 * IQR
                    # st.write(IQR)
                    outliers = (dataset[col] < Lower_Bound) | (dataset[col] > Upper_Bound)
                    
                    if outliers.any():
                        dataset[col].fillna(dataset[col].median(), inplace = True)
                            
    else:
        st.info("There is not any Null Value Represent in the Dataset.")

elif step == "Encoding":
    
    encoding_methods = ["Select Method for encoding","OneHotEncoding", "Label Encoding", "Target Encoding"]
    
    target = st.text_input("Enter your target column name (for Target Encoding only):")

    
    for col in dataset.columns:
        if dataset[col].dtype == "object" and col != target:
            # means = st.selectbox(f"{dataset[col]} have meaninng category?", ["Yes", "NO"], key=f"mean_{col}")
            
        
            
                encoding = st.selectbox("Methods", encoding_methods, key=f"encode_{col}")
                if encoding != "Select Method for encoding":
                    
                    if encoding == "OneHotEncoding":
                        dataset = pd.get_dummies(data = dataset, columns = [col])
                        
                        st.text(dataset[col].sample(2))
                        
                    elif encoding == "Label Encoding":
                        from sklearn.preprocessing import LabelEncoder                   
                        encorder = LabelEncoder()
                        dataset[col] = encorder.fit_transform(dataset[col])
                        st.text(dataset[col].sample(2))
                    
                    elif encoding == "Target Encoding":
                        
                        if target in dataset.columns:
                        
                            import category_encoders as ce
                            
                            encoder = ce.TargetEncoder()
                            
                            dataset[col] = encoder.fit_transform(dataset[col], dataset[target])
                            st.text(dataset[col].sample(2))
                        else:
                            st.error("Please enter a valid target column!")
                        
                    st.success(f"'{col}' encoded using {encoding}.")
                    st.text(dataset.sample(5))
                else:
                    st.warning(f"Please select an encoding method for {col}.")
                    
    st.text(dataset.sample(5))
                    