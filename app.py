import streamlit as st
import pandas as pd

# Define the fluid lines and stages
fluid_lines = [
    "N2 line", "25, 35 OLM", "98 SA", "WSA", "SO3G", "MS", "HS", "POW", "Steam Trace line",
    "MC & SC", "WT (S) air blowing", "WT (R) air blowing", "WT (S) flushing", "WT (R) flushing",
    "VG (S)", "SM2"
]

stages = [
    "Line Preparation", "MPCI Line Check (Pre-Flushing/Blowing)", "Leak Check",
    "Flushing/Blowing Execution", "Pressure Test Preparation", "MPCI Line Check (Post-Preparation)",
    "Pressure Test Execution", "DSM Sign-Off", "Overall Progress"
]

# Initialize the DataFrame with all zeros
data = {stage: [0]*len(fluid_lines) for stage in stages}
data["Fluid Line"] = fluid_lines
df = pd.DataFrame(data)

# Function to calculate overall progress
def calculate_overall_progress(row):
    stages_progress = row[:-1]  # Exclude 'Overall Progress'
    return sum(stages_progress) / len(stages_progress)

# Calculate overall progress for each fluid line
df["Overall Progress"] = df.apply(calculate_overall_progress, axis=1)

# Streamlit UI
st.title("Fluid Lines Progress Tracker")

# Display the DataFrame
st.dataframe(df)

# Select fluid line and stage to update
selected_line = st.selectbox("Select Fluid Line", fluid_lines)
selected_stage = st.selectbox("Select Stage", stages[:-1])  # Exclude 'Overall Progress'

# Input for new percentage
new_percentage = st.number_input("Update Percentage", min_value=0, max_value=100)

# Update button
if st.button("Update Progress"):
    df.loc[df["Fluid Line"] == selected_line, selected_stage] = new_percentage
    df["Overall Progress"] = df.apply(calculate_overall_progress, axis=1)
    st.dataframe(df)

# File handling functions
def save_progress(df, file_path):
    df.to_csv(file_path, index=False)

def load_progress(file_path):
    return pd.read_csv(file_path)

# Streamlit UI for saving and loading data
if st.button("Save Progress"):
    save_progress(df, "progress_data.csv")
    st.success("Progress data saved successfully!")

if st.button("Load Progress"):
    df = load_progress("progress_data.csv")
    st.dataframe(df)
    st.success("Progress data loaded successfully!")

# Display progress bars for each fluid line
st.subheader("Progress Overview")
for idx, row in df.iterrows():
    st.write(f"{row['Fluid Line']}: {row['Overall Progress']}%")
    st.progress(row["Overall Progress"])
