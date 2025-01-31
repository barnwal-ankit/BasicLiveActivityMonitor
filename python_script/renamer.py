# This Script will rename The CSV files names.
# It only renames the files which Have forearm or thigh in its name as i used forearm and thigh dataset sor training.

import os

# Path to the main folder (update this to your specific path)
main_path = r"C:\Users\Desktop\extracted\csv"

# Walk through all folders and subfolders
for root, dirs, files in os.walk(main_path):
    for i, file in enumerate(files, start=1):  # Enumerate files, starting with 1
        if file.endswith(".csv"):  # Only process .csv files
            # Extract activity name and body part from the folder structure
            folder_path_parts = os.path.normpath(root).split(os.sep)
            if len(folder_path_parts) >= 2:
                body_part = folder_path_parts[-2]  # Second-to-last folder is body part (thigh/forearm)
                activity = folder_path_parts[-1]  # Last folder is activity (climbingup, lying, etc.)
            else:
                continue

            # Determine the body part for the file naming convention
            if body_part == "forearm":
                new_file_name = f"{activity}_{i}.csv"
            elif body_part == "thigh":
                new_file_name = f"{activity}_{i}.csv"
            else:
                continue  # Skip files outside the expected folder structure

            # Get the full paths for the old and new filenames
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)

            print(f"Renamed: {old_file_path} -> {new_file_path}")

print("Renaming completed!")
