import pandas as pd

# === Step 1: Load the original metadata CSV ===
input_csv_path = "all_dicom_metadata.csv"  # Change path if needed
df = pd.read_csv(input_csv_path)

# === Step 2: Define relevant columns based on your thesis ===
relevant_columns = [
    'FilePath',
    "Patient_ID", "Patient's_Age", "Patient's_Sex",
    'Study_Description', 'Series_Description', 'Body_Part_Examined',
    'Reason_for_Study', 'Requested_Procedure_Description',

    'Modality', "Manufacturer", "Manufacturer's_Model_Name",
    'Magnetic_Field_Strength', 'Echo_Time', 'Repetition_Time', 'Flip_Angle',
    'Pixel_Spacing', 'Slice_Thickness', 'Spacing_Between_Slices',
    'Rows', 'Columns',

    'Study_Date', 'Series_Date', 'Acquisition_Date',
    'Instance_Number', 'Series_Number',
    'Image_Position_(Patient)', 'Image_Orientation_(Patient)', 'Slice_Location',

    'Contrast/Bolus_Agent', 'Window_Center', 'Window_Width',
    'Image_Comments', 'Patient_Comments', 'Pixel_Bandwidth',
    'Study_Comments', 'Requested_Procedure_Priority'
]

# === Step 3: Keep only existing columns ===
existing_columns = [col for col in relevant_columns if col in df.columns]
filtered_df = df[existing_columns]

# === Step 4: Save the filtered DataFrame ===
output_csv_path = "filtered_dicom_metadata.csv"
filtered_df.to_csv(output_csv_path, index=False)

print(f"Filtered metadata saved to: {output_csv_path}")
