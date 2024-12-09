import json
import os

# Function to update labels in the JSON
def update_labels(json_data, translation_dict):
    for item in json_data:
        for track in item.get("tracks", []):
            label = track.get("label")
            if label in translation_dict:
                track["label"] = translation_dict[label]
    return json_data


if __name__ == "__main__":
    punches = {"Głowa lewą ręką": "Head with left hand",
               "Głowa prawą ręką": "Head with right hand",
               "Korpus lewą ręką": "Body with left hand",
               "Korpus prawą ręką": "Body with right hand",
               "Blok lewą ręką": "Block with left hand",
               "Blok prawą ręką": "Block with right hand",
               "Chybienie lewą ręką": "Miss with left hand",
               "Chybienie prawą ręką": "Miss with right hand"}

    # Base directory containing folders with JSON files
    base_dir = "../boxing_data"

    # Walk through the directory structure
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                # Open, update, and overwrite JSON file
                with open(file_path, "r+", encoding="utf-8") as f:
                    data = json.load(f)  # Load the JSON dataset
                    updated_data = update_labels(data, punches)  # Update labels
                    f.seek(0)  # Move to the start of the file
                    json.dump(updated_data, f, ensure_ascii=False, indent=4)  # Overwrite the file
                    f.truncate()  # Remove any leftover content

    print("All JSON files processed and updated in place.")