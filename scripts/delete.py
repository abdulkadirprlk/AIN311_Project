import os
import shutil

def delete_scaled_files_and_folders(folder_path):
    """
    Deletes all scaled_annotations.json files and scaled_images folders
    inside the specified folder and its subdirectories.

    Parameters:
    - folder_path: Path to the main folder to search in.
    """
    deleted_files = 0
    deleted_folders = 0

    # Traverse the folder structure
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # Delete scaled_annotations.json files
        for file in files:
            if file == "scaled_annotations.json":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                    deleted_files += 1
                except Exception as e:
                    print(f"Failed to delete file {file_path}: {e}")

        # Delete scaled_images folders
        for dir_name in dirs:
            if dir_name == "scaled_images":
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted folder: {dir_path}")
                    deleted_folders += 1
                except Exception as e:
                    print(f"Failed to delete folder {dir_path}: {e}")

    if deleted_files == 0 and deleted_folders == 0:
        print("No files or folders to delete.")
    else:
        print(f"Deleted {deleted_files} file(s) and {deleted_folders} folder(s).")


if __name__ == "__main__":
    folder_path = "/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset"
    delete_scaled_files_and_folders(folder_path)
