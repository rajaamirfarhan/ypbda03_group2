import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset.csv")
df.columns = map(str.upper, df.columns) 

st.set_page_config(page_title="🚑 GROUP 1", layout="wide")
st.sidebar.write('Main Dashboard')

st.title("""🚑 GROUP 1: Covid-19 Statistics Summary\n
         MEMBERS: Raja Amir | Azrul Azree | Aliff Hiqmal | Khairul Amir
         """)
st.markdown("""---""")

df = pd.read_csv('dataset.csv')
mappings = {
    "SEX": {1: "FEMALE", 2: "MALE", 99: "UNKNOWN"},
    "HOSPITALIZED": {1: "NO", 2: "YES", 99: "UNKNOWN"},
    "INTUBATED": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "PNEUMONIA": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "PREGNANCY": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "SPEAKS_NATIVE_LANGUAGE": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "DIABETES": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "COPD": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "ASTHMA": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "INMUSUPR": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "HYPERTENSION": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "OTHER_DISEASE": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "CARDIOVASCULAR": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "OBESITY": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "CHRONIC_KIDNEY": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "TOBACCO": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "ANOTHER_CASE": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "MIGRANT": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "ICU": {1: "YES", 2: "NO", 97: "DOES NOT APPLY", 98: "IGNORED", 99: "UNKNOWN"},
    "OUTCOME": {1: "POSITIVE", 2: "NEGATIVE", 3: "PENDING"},
    "NATIONALITY": {1: "MEXICAN", 2: "FOREIGN", 99: "UNKNOWN"},
    "COUNTRY_OF_ORIGIN": {1: "MEXICO", 2: "ABROAD", 99: "UNKNOWN"},
    "SECTOR": {1: "PUBLIC", 2: "PRIVATE", 99: "UNKNOWN"},
    "TREATMENT_LOCATION": {1: "URBAN", 2: "RURAL", 99: "UNKNOWN"},
    "BIRTHPLACE_LOCATION": {1: "RURAL", 2: "URBAN", 99: "UNKNOWN"},
    "PATIENT_LOCATION": {1: "INDOOR", 2: "OUTDOOR", 99: "UNKNOWN"},
    "MUNICIPALITY": {1: "MEXICAN", 2: "ABROAD", 99: "UNKNOWN"}
}

for column, mapping in mappings.items():
    if column in df.columns:
        df[column] = df[column].map(mapping).fillna("UNKNOWN")

analysis = df.copy()


# Bin the AGE column into the defined age groups
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=False)


# Filter for positive outcomes and group by AGE_GROUP
positive_age_groups = df[df['OUTCOME'] == 'POSITIVE'].groupby('AGE_GROUP').size().reset_index(name='Positive')

# Display the result with age group and positive count
max_positive_row = positive_age_groups.loc[positive_age_groups['Positive'].idxmax()]

# Extract the age group and the maximum positive value
max_positive_age_group = max_positive_row['AGE_GROUP']
max_positive_value = max_positive_row['Positive']

# Display the result in Streamlit
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Age group with the maximum positives cases: {max_positive_age_group} y'old")

with col2:
    st.subheader(f"Maximum positive cases: {max_positive_value} cases")

st.markdown("""---""")

# Gender Filter in Sidebar
gender_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=["FEMALE", "MALE"],
    default=["FEMALE", "MALE"]
)

# Filter Data Based on Gender
filtered_data = analysis[analysis['SEX'].isin(gender_filter)]

# Bin the AGE column into the defined age groups for filtered data
filtered_data['AGE_GROUP'] = pd.cut(filtered_data['AGE'], bins=bins, labels=labels, right=False)

# Grouping by AGE_GROUP and SEX for the filtered data
gender_age_group_counts = filtered_data.groupby(["AGE_GROUP", "SEX"], observed=False).size().unstack(fill_value=0)

tab2, tab3 = st.tabs(["COMPARISON BY AGE", "COMPARISON BY GENDER"])


with tab2:
    st.header("AGE")
    st.bar_chart(positive_age_groups, x="AGE_GROUP", y="Positive")

with tab3:
    st.header("GENDER")
    st.bar_chart(gender_age_group_counts)

