import streamlit as st
import pandas as pd
import os

# Define the fluid lines and stages
fluid_lines = [
    "N2 line", "25, 35 OLM", "98 SA", "WSA", "SO3G", "POW", 
    "WT (S) air blowing", "WT (R) air blowing", "WT (S) flushing", "WT (R) flushing",
    "CAP", "VG (S)", 
]

steam_lines = [
    "MS", "HS", "Steam Trace line", "MC & SC", "SM2"
]

stages = [
    "Flushing Prep", "Leak Check 1", "Flushing/Blowing",
    "Pressure Test Prep", "Leak Check 2", "Pressure Test", "Sign-Off"
]

# Function to calculate overall progress for each fluid line
def calculate_overall_progress(row):
    stages_progress = row[:-1]  # Exclude 'Overall Progress' itself
    stages_progress = [float(value) for value in stages_progress]  # Convert to float
    return sum(stages_progress) / len(stages_progress)

# Function to calculate overall progress across all fluid lines
def calculate_total_progress(df):
    return df["Overall Progress"].mean()

# Load initial data from CSV if it exists
file_path = "progress_data.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    df = df.set_index('Fluid Line')
else:
    # Initialize the DataFrame with all zeros if CSV does not exist
    data = {stage: [0]*len(fluid_lines) for stage in stages}
    data["Fluid Line"] = fluid_lines
    df = pd.DataFrame(data).set_index("Fluid Line")

# Ensure 'Overall Progress' column exists
if 'Overall Progress' not in df.columns:
    df['Overall Progress'] = 0.0

# Calculate overall progress for each fluid line
df["Overall Progress"] = df.apply(calculate_overall_progress, axis=1)

# Streamlit UI
st.title("Flushing/Blowing Progress Tracker")

# Calculate total overall progress
total_progress = calculate_total_progress(df) / 100  # Normalize to 0-1 scale
st.header(f"Total Overall Progress: {total_progress * 100:.2f}%")
st.progress(total_progress)

# Display the DataFrame
st.dataframe(df)

# Select fluid line and stage to update
selected_line = st.selectbox("Select Fluid Line", fluid_lines)
selected_stage = st.selectbox("Select Stage", stages)

# Input for new percentage
new_percentage = st.number_input("Update Percentage", min_value=0, max_value=100)

# File handling functions
def save_progress(df, file_path):
    df.to_csv(file_path)

# Update button
if st.button("Update Progress"):
    df.loc[selected_line, selected_stage] = new_percentage
    df["Overall Progress"] = df.apply(calculate_overall_progress, axis=1)
    save_progress(df, file_path)  # Save the updated data
    st.experimental_rerun()  # Rerun the script to replace the table

def load_progress(file_path):
    df = pd.read_csv(file_path, index_col="Fluid Line")
    if 'Overall Progress' not in df.columns:
        df['Overall Progress'] = 0.0
    df["Overall Progress"] = df.apply(calculate_overall_progress, axis=1)
    return df

# Streamlit UI for saving and loading data
if st.button("Save Progress"):
    save_progress(df, file_path)
    st.success("Progress data saved successfully!")

if st.button("Load Progress"):
    df = load_progress(file_path)
    total_progress = calculate_total_progress(df) / 100  # Normalize to 0-1 scale
    st.header(f"Total Overall Progress: {total_progress * 100:.2f}%")
    st.progress(total_progress)
    st.success("Progress data loaded successfully!")
    st.experimental_rerun()  # Rerun the script to replace the table

# Display progress bars for each fluid line
st.subheader("Progress Overview")
for idx, row in df.iterrows():
    st.write(f"{idx}: {row['Overall Progress']:.2f}%")
    st.progress(row["Overall Progress"] / 100)  # Convert to 0-1 scale
