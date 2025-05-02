import os
import pydicom
import pandas as pd

# Root folder of your DICOM hierarchy
root_folder = r"C:\Users\Saad\Desktop\Thesis\Sagittal_Selected"

all_records = []
all_keys = set()

for dirpath, _, filenames in os.walk(root_folder):
    for file in filenames:
        if file.lower().endswith(".dcm"):
            try:
                filepath = os.path.join(dirpath, file)
                dcm = pydicom.dcmread(filepath, stop_before_pixels=True)

                record = {"FilePath": filepath}
                # Fix: Replace iterall() with standard iteration or walk()
                for elem in dcm:  # Or use dcm.walk() to include nested sequences
                    tag_name = elem.name.replace(" ", "_")
                    value = str(elem.value)
                    record[tag_name] = value
                    all_keys.add(tag_name)
                    
                all_records.append(record)

            except Exception as e:
                print(f"Error reading {file}: {e}")

# Fill missing keys with NaN for uniform DataFrame
df = pd.DataFrame(all_records)
# Save to current folder instead of root folder
csv_output = os.path.join(os.getcwd(), "all_dicom_metadata.csv")
# Or simply use: csv_output = "all_dicom_metadata.csv"
df.to_csv(csv_output, index=False)

print(f"All metadata fields extracted. Saved to:\n{csv_output}")
