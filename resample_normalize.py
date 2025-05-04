import os
import SimpleITK as sitk
import numpy as np

# === Configuration ===
input_root = r"C:\Users\Saad\Desktop\Thesis\Real\Sagittal_Selected_NIfTI"
output_root = r"C:\Users\Saad\Desktop\Thesis\Real\Sagittal_Selected_NIfTI_Resample"
new_spacing = [1.0, 1.0, 1.0]

# === Helper Function ===
def resample_and_normalize(input_path, output_path):
    image = sitk.ReadImage(input_path)
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    new_size = [
        int(round(osz * ospc / nspc)) 
        for osz, ospc, nspc in zip(original_size, original_spacing, new_spacing)
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetDefaultPixelValue(image.GetPixelIDValue())

    resampled_image = resampler.Execute(image)

    # Normalize
    array = sitk.GetArrayFromImage(resampled_image).astype(np.float32)
    norm_array = (array - np.mean(array)) / np.std(array)
    norm_image = sitk.GetImageFromArray(norm_array)
    norm_image.CopyInformation(resampled_image)

    sitk.WriteImage(norm_image, output_path)

# === Main Loop ===
for root, _, files in os.walk(input_root):
    for file in files:
        if file.endswith(".nii") or file.endswith(".nii.gz"):
            input_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, input_root)
            output_dir = os.path.join(output_root, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, file)

            print(f"🔄 Processing: {input_path}")
            try:
                resample_and_normalize(input_path, output_path)
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Failed on {input_path}: {e}")
