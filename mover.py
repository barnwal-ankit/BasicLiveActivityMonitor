# This Script will move .csv and .sqlite files which contains forearm or thigh in its name, it just make all files inside a single folder instead of multiple folder.
# It will create two folder at the base path csv and sqlite.
# sqlite folder contains all the sqlite files and csv folder will contains the csv files

import os
import shutil
from tqdm import tqdm  # For progress bar

# Updated base path
base_path = r"C:\Users\Desktop\extracted\All_files"        #change with you path where you want to save the files.
# Centralized extraction folders for csv and sqlite files
extract_path = r"C:\Users\Desktop\extracted"               #change with you path where all the extracted files are.
csv_folder = os.path.join(extract_path, "csv")
sqlite_folder = os.path.join(extract_path, "sqlite")

# Ensure the centralized folders exist
os.makedirs(csv_folder, exist_ok=True)
os.makedirs(sqlite_folder, exist_ok=True)
print(f"Ensured the folders exist: {csv_folder}, {sqlite_folder}")

# Process all proband folders in the base path
print("\nStarting the file relocation process...\n")
proband_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

for proband_folder in tqdm(proband_folders, desc="Processing Proband Folders", unit="folder"):
    proband_folder_path = os.path.join(base_path, proband_folder)

    # Extract proband number from the folder name (e.g., proband1)
    proband_number = proband_folder.split('_')[0]  # Assumes naming like proband1_acc_*

    # Process files inside the proband folder
    for file_name in os.listdir(proband_folder_path):
        file_path = os.path.join(proband_folder_path, file_name)

        # Skip directories, process only files
        if os.path.isfile(file_path):
            # Check if file contains "forearm" or "thigh"
            if "forearm" in file_name.lower() or "thigh" in file_name.lower():
                # Determine file extension and target folder
                if file_name.endswith(".csv"):
                    target_folder = csv_folder
                elif file_name.endswith(".sqlite"):
                    target_folder = sqlite_folder
                else:
                    continue  # Skip files that aren't .csv or .sqlite

                # Rename file to include proband number
                new_file_name = f"{os.path.splitext(file_name)[0]}_{proband_number}{os.path.splitext(file_name)[1]}"
                destination_file = os.path.join(target_folder, new_file_name)

                # Move file to the appropriate folder
                try:
                    shutil.move(file_path, destination_file)
                    print(f"  Moved {file_name} to {destination_file}")
                except Exception as e:
                    print(f"  Error moving {file_name}: {e}")

print("\nAll proband folders processed. File relocation complete.")
