import os
import shutil
import pydicom
import numpy as np

def is_sagittal(image_orientation):
    if image_orientation and len(image_orientation) == 6:
        row_cosines = np.array(image_orientation[:3])
        return np.allclose(row_cosines, [0, 1, 0], atol=0.1)
    return False

def find_target_folders(base_path):
    sagittal_folders = []
    t2_tse_cor_folders = []

    for root, dirs, files in os.walk(base_path):
        root_lower = root.lower()
        if "localizer" in root_lower or "tumor" in root_lower:
            continue
        for file in files:
            if file.endswith(".dcm"):
                try:
                    filepath = os.path.join(root, file)
                    dcm = pydicom.dcmread(filepath, stop_before_pixels=True)
                    orientation = dcm.get("ImageOrientationPatient", None)
                    series_desc = dcm.get("SeriesDescription", "").lower()

                    if "tumor" in series_desc:
                        break  # skip this folder
                    if is_sagittal(orientation):
                        sagittal_folders.append(root)
                        break
                    elif "t2_tse_cor" in series_desc:
                        t2_tse_cor_folders.append(root)
                        break

                except Exception as e:
                    print(f"Error reading {file} in {root}: {e}")

    return list(set(sagittal_folders)), list(set(t2_tse_cor_folders))

def copy_folders(folder_list, destination_root):
    os.makedirs(destination_root, exist_ok=True)
    successful_copies = 0
    failed_copies = 0

    print(f"\nFiles will be copied to: {os.path.abspath(destination_root)}\n")

    for source_folder in folder_list:
        relative_path = os.path.join(*source_folder.split(os.sep)[-3:])
        destination_folder = os.path.join(destination_root, relative_path)

        print(f"Copying: {source_folder} → {destination_folder}")
        try:
            shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
            successful_copies += 1
        except Exception as e:
            print(f"  Error copying: {str(e)}")
            failed_copies += 1

    print("\n✅ Copy operation completed!")
    print(f"Successfully copied: {successful_copies} folders")
    print(f"Failed copies: {failed_copies} folders")
    print(f"\nYour files are located at:\n{os.path.abspath(destination_root)}")

    if successful_copies > 0 and os.path.exists(destination_root):
        num_files = sum([len(files) for _, _, files in os.walk(destination_root)])
        print(f"\nVerification: Found {num_files} files in the destination folder")
    else:
        print("\nWARNING: No folders appear to have been copied successfully")

# === Configuration ===
base_dir = r"C:\Users\Saad\Desktop\Thesis\Real\healthy_IMPALA"
sagittal_dest = r"C:\Users\Saad\Desktop\Thesis\Real\Sagittal_Selected"
coronal_dest  = r"C:\Users\Saad\Desktop\Thesis\Real\Coronal_Selected_t2_tse_cor"

# === Run the script ===
sagittal_dirs, coronal_dirs = find_target_folders(base_dir)

print("🧭 Sagittal folders found:")
for folder in sagittal_dirs:
    print("  -", folder)

print("\n🧭 Coronal (t2_tse_cor, excluding Tumor) folders found:")
for folder in coronal_dirs:
    print("  -", folder)

copy_folders(sagittal_dirs, sagittal_dest)
copy_folders(coronal_dirs, coronal_dest)
