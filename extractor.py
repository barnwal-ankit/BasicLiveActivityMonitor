# This Python Script Extracts The zip Files Of Real world 2016 Dataset.
# But before using it "The realworld2016_dataset.zip" needs to be extracted then this script will autimatically extract the zip files inside the dataset.

import zipfile
import os
from tqdm import tqdm  # For progress bar

# Base path where all proband folders are located
base_path = r"c:\Users\Desktop\realworld2016_dataset" # location of Dataset Change with the location of your downloaded dataset.
extract_path = r"c:\Users\Desktop\extracted"   # Location where extracted files will be saved change the location where you want to save the extracted files.

# Loop through all proband folders
print("Starting the extraction process...\n")
for i in range(1, 2):  # Assuming proband1 to proband15
    proband_folder = os.path.join(base_path, f"proband{i}", "data")
    print(f"\nProcessing Proband {i} in folder: {proband_folder}...")
    
    if os.path.exists(proband_folder):  # Check if the proband folder exists
        # Get all zip files in the "data" directory that contain "acc" in their name
        zip_files = [f for f in os.listdir(proband_folder) if f.endswith(".zip") and "acc" in f]
        
        # Process each matching zip file
        for zip_file_name in tqdm(zip_files, desc=f"  Extracting Proband {i}", unit="file"):
            zip_file_path = os.path.join(proband_folder, zip_file_name)
            extracted_folder = os.path.join(proband_folder, zip_file_name.replace(".zip", ""))
            
            if os.path.exists(zip_file_path):  # Confirm the zip file exists
                print(f"  Found zip: {zip_file_name}")
                
                # Create a folder with the same name as the zip file (without .zip)
                if not os.path.exists(extracted_folder):
                    os.makedirs(extracted_folder)
                    print(f"  Created folder: {extracted_folder}")
                
                # Extract the contents of the zip file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extracted_folder)
                
                print(f"  Extracted {zip_file_name} to {extracted_folder}")
            else:
                print(f"  Zip file not found: {zip_file_name}")
    else:
        print(f"Proband folder not found: {proband_folder}")

print("\nAll probands processed. Extraction complete.")
