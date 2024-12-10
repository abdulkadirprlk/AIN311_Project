import os
import shutil

# Base directory containing the dataset folders
base_dir = "/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN311_Project/dataset"

# Output directory where scaled images and annotations will be consolidated
output_dir = "/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN311_Project/output"
os.makedirs(output_dir, exist_ok=True)

# Iterate through all folders in the base directory
for root, dirs, files in os.walk(base_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)

        # Check if the directory contains "scaled_images" and "scaled_annotations.json"
        scaled_images_path = os.path.join(dir_path, "scaled_images")
        scaled_annotations_path = os.path.join(dir_path, "scaled_annotations.json")

        if os.path.exists(scaled_images_path) and os.path.exists(scaled_annotations_path):
            print(f"Processing: {dir_path}")

            # Create a subdirectory for each task in the output directory
            task_output_dir = os.path.join(output_dir, dir_name)
            os.makedirs(task_output_dir, exist_ok=True)

            # Copy scaled_images folder
            destination_images_path = os.path.join(task_output_dir, "scaled_images")
            shutil.copytree(scaled_images_path, destination_images_path)

            # Copy scaled_annotations.json
            destination_annotations_path = os.path.join(task_output_dir, "scaled_annotations.json")
            shutil.copy2(scaled_annotations_path, destination_annotations_path)

print("Data consolidation completed.")