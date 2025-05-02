import os
import pydicom

def count_unique_patient_ids(base_path):
    ids = set()
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if not f.lower().endswith(".dcm"):
                continue
            path = os.path.join(root, f)
            try:
                ds = pydicom.dcmread(path, stop_before_pixels=True)
                pid = ds.get("PatientID", None)
                if pid:
                    ids.add(pid)
                # once you've read one .dcm in this folder, you could break
                # if you know all in the same folder are same patient
                break
            except Exception as e:
                print(f"Warning: could not read {path}: {e}")
    return ids

base_dir = r"C:\Users\Saad\Desktop\Thesis\Real\healthy_IMPALA\healthy_IMPALA"
unique_ids = count_unique_patient_ids(base_dir)
print(f"Found {len(unique_ids)} unique PatientID(s): {unique_ids}")