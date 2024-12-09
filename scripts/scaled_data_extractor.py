import os
import shutil


def move_annotations_to_images_folder(output_dir):
    """
    Moves each `*_scaled_annotations.json` file into its corresponding `*_scaled_images` folder.

    Parameters:
    - output_dir: Path to the directory containing the scaled images and annotations.
    """
    moved_files = 0

    # Iterate through all files in the output directory
    for file_name in os.listdir(output_dir):
        if file_name.endswith("_scaled_annotations.json"):
            # Extract the base name without the extension
            base_name = file_name.replace("_scaled_annotations.json", "")
            images_folder = os.path.join(output_dir, f"{base_name}_scaled_images")
            json_file = os.path.join(output_dir, file_name)

            # Check if the corresponding scaled_images folder exists
            if os.path.exists(images_folder):
                dest_file = os.path.join(images_folder, file_name)
                shutil.move(json_file, dest_file)
                print(f"Moved {file_name} to {images_folder}")
                moved_files += 1
            else:
                print(f"Images folder not found for {file_name}, skipping...")

    if moved_files == 0:
        print("No annotation files found.")
    else:
        print(f"Moved {moved_files} file(s).")


if __name__ == "__main__":
    # Example usage
    output_directory = "/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/output"  # Replace with your output path
    move_annotations_to_images_folder(output_directory)
