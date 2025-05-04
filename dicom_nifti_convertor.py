import os
import dicom2nifti
import dicom2nifti.settings
import SimpleITK as sitk

# ============ CONFIG ============

# Disable validation
dicom2nifti.settings.disable_validate_slice_increment()
dicom2nifti.settings.disable_validate_orientation()

# Input-output root pairs
tasks = [
    {
        "input_root": r"C:\Users\Saad\Desktop\Thesis\Real\Sagittal_Selected",
        "output_root": r"C:\Users\Saad\Desktop\Thesis\Real\Sagittal_Selected_NIfTI"
    },
    {
        "input_root": r"C:\Users\Saad\Desktop\Thesis\Real\Coronal_Selected_t2_tse_cor",
        "output_root": r"C:\Users\Saad\Desktop\Thesis\Real\Coronal_Selected_t2_tse_cor_NIfTI"
    }
]

# ============ HELPERS ============

def contains_dicom(folder):
    return any(f.lower().endswith('.dcm') for f in os.listdir(folder))

def write_via_sitk(src_folder, dst_folder):
    series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(src_folder) or []
    if not series_IDs:
        raise RuntimeError("No series found by SimpleITK")
    for sid in series_IDs:
        files = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(src_folder, sid)
        reader = sitk.ImageSeriesReader()
        reader.SetFileNames(files)
        img = reader.Execute()
        out_file = os.path.join(dst_folder, f"{sid}.nii.gz")
        sitk.WriteImage(img, out_file)
    return series_IDs

# ============ MAIN LOOP ============

for task in tasks:
    input_root = task["input_root"]
    output_root = task["output_root"]
    os.makedirs(output_root, exist_ok=True)

    print(f"\n=== Processing: {input_root} → {output_root} ===\n")

    failed = []

    for root, _, _ in os.walk(input_root):
        if not contains_dicom(root):
            continue

        rel = os.path.relpath(root, input_root)
        out = os.path.join(output_root, rel)
        os.makedirs(out, exist_ok=True)

        print(f"\n🔄 Converting: {rel}")

        # Try dicom2nifti
        try:
            dicom2nifti.convert_directory(
                root, out,
                compression=True,
                reorient=True
            )
            print(f"✅ Saved via dicom2nifti → {out}")
            continue

        except Exception as e:
            print(f"⚠️ dicom2nifti failed ({type(e).__name__}): {e}")

        # Try fallback via SimpleITK
        try:
            series = write_via_sitk(root, out)
            print(f"✅ Saved via SimpleITK (series {series}) → {out}")
        except Exception as e2:
            print(f"❌ SimpleITK also failed ({type(e2).__name__}): {e2}")
            failed.append((rel, str(e2)))

    print(f"\n--- Done for {input_root} ---")
    print(f"Failures: {len(failed)}")
    if failed:
        print("Failed cases:")
        for r, e in failed:
            print(f" • {r} → {e}")
