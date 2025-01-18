import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
import streamlit as st

# Set options for Pandas and Seaborn
pd.set_option('display.max_columns', 100)
sns.set()

# Load the dataset
df = pd.read_csv("dataset.csv")
df.columns = map(str.upper, df.columns)

# Define the mappings
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

# Apply mappings to the dataframe
for column, mapping in mappings.items():
    if column in df.columns:
        df[column] = df[column].map(mapping).fillna("UNKNOWN")

# Bin the AGE column into defined age groups
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=False)

# Filter for positive outcomes and group by AGE_GROUP
positive_age_groups = df[df['OUTCOME'] == 'POSITIVE'].groupby('AGE_GROUP').size().reset_index(name='Positive')

# Create custom CSS for the dashboard
custom_css = """
<style>
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .metric-box h1 {
        margin: 0;
        font-size: 2rem;
        color: #4caf50; /* Adjust color for the numbers */
    }
    .metric-box h2 {
        margin: 0;
        font-size: 1rem;
        color: #333; /* Adjust color for the labels */
    }
</style>
"""

# Inject CSS into Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Add a filter for SEX at the side
sex_filter = st.sidebar.selectbox(
    "Select Sex",
    options=["All", "Female", "Male"],
    index=0,  # Default to "All"
    help="Filter the metrics by sex."
)

# Filter the dataset based on the selected sex
if sex_filter == "All":
    filtered_df = df
else:
    filtered_df = df[df["SEX"] == sex_filter.upper()]
#Title
st.markdown("### Latest COVID Situation")

# Metrics data based on filtered dataset
positive_count = (filtered_df['OUTCOME'] == "POSITIVE").sum()
hospitalized_count = (filtered_df['HOSPITALIZED'] == "YES").sum()
icu_count = (filtered_df['ICU'] == "YES").sum()

# Create custom HTML for metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-box">
            <h1>{positive_count}</h1>
            <h2>Positive Cases</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box">
            <h1>{hospitalized_count}</h1>
            <h2>Hospitalized</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-box">
            <h1>{icu_count}</h1>
            <h2>ICU</h2>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""---""")
st.markdown("")

# Sample data for Tab 1 (Heatmap)
df_heatmap = pd.DataFrame({
    "DIABETES": [1, 2, 1, 2, 2],
    "COPD": [1, 2, 2, 2, 1],
    "ASTHMA": [2, 1, 2, 1, 2],
    "INMUSUPR": [2, 2, 1, 1, 2],
    "HYPERTENSION": [1, 2, 1, 2, 1],
    "CARDIOVASCULAR": [1, 2, 1, 2, 2],
    "OBESITY": [2, 1, 2, 1, 2],
    "CHRONIC_KIDNEY": [2, 1, 2, 1, 2],
    "TOBACCO": [1, 2, 1, 1, 2],
    "ICU": [1, 2, 1, 2, 1]  # 1: ICU, 2: Not ICU
})

# Sample data for Tab 2 (Bar Chart)
df_bar = pd.DataFrame({
    "DIABETES": [1, 2, 1, 2, 2],
    "COPD": [1, 2, 2, 2, 1],
    "ASTHMA": [2, 1, 2, 1, 2],
    "INMUSUPR": [2, 2, 1, 1, 2],
    "HYPERTENSION": [1, 2, 1, 2, 1],
    "CARDIOVASCULAR": [1, 2, 1, 2, 2],
    "OBESITY": [2, 1, 2, 1, 2],
    "CHRONIC_KIDNEY": [2, 1, 2, 1, 2],
    "TOBACCO": [1, 2, 1, 1, 2],
    "OUTCOME": ['DECEASED', 'RECOVERED', 'DECEASED', 'RECOVERED', 'DECEASED']
})

# Tabs
tab1, tab2 = st.tabs(["Heatmap", "Bar Chart"])

# Tab 1: Heatmap
with tab1:
    st.markdown("### Correlation Heatmap")
    correlation_matrix = df_heatmap.corr()
    sns.set_theme(style="white", palette="muted")
    sns.set_context("talk")

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap='coolwarm',
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=1,
        annot_kws={"fontsize": 12, "fontweight": "bold"},
        fmt=".2f",
        cbar_kws={'label': 'Correlation Coefficient'},
    )

    plt.title("Correlation Between Diseases and ICU Admission", fontsize=18, fontweight='bold')
    plt.xlabel("Conditions", fontsize=14, fontweight='bold')
    plt.ylabel("Conditions", fontsize=14, fontweight='bold')
    st.pyplot(plt)

# Tab 2: Bar Chart
with tab2:
    st.markdown("### Common Diseases Among Deceased Patients")
    
    # Filter deceased patients
    deceased_df = df_bar[df_bar["OUTCOME"] == "DECEASED"]

    # Count diseases for deceased patients
    disease_columns = ["DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION", "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY", "TOBACCO"]
    disease_counts = deceased_df[disease_columns].sum()

    sns.set_theme(style="whitegrid", palette="copper")

    # Plot bar chart
    plt.figure(figsize=(10, 6))
    disease_counts.sort_values(ascending=True).plot(kind='barh', color=sns.color_palette("copper", len(disease_counts)))

    plt.title('Common Diseases Among Deceased Patients', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Deceased Patients', fontsize=12, fontweight='bold')
    plt.ylabel('Diseases', fontsize=12, fontweight='bold')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    st.pyplot(plt)
