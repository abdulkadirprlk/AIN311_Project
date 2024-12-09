import json
import os
from PIL import Image


def scale_annotations(points, original_size, new_size):
    """
    Scales bounding box points from original image size to new size.
    """
    orig_w, orig_h = original_size
    new_w, new_h = new_size

    scale_x = new_w / orig_w
    scale_y = new_h / orig_h

    return [
        points[0] * scale_x, points[1] * scale_y,
        points[2] * scale_x, points[3] * scale_y
    ]


if __name__ == "__main__":
    # Path to the main dataset directory
    dataset_dir = r'/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset'

    # Target size for resizing
    target_size = (180, 180)

    # Loop through each task folder in the dataset
    for task_folder in os.listdir(dataset_dir):
        task_path = os.path.join(dataset_dir, task_folder)

        # Check if it's a directory and contains the necessary subdirectories
        if os.path.isdir(task_path):
            extracted_frames_dir = os.path.join(task_path, 'cropped_images')
            annotations_json_path = os.path.join(task_path, 'updated_annotations.json')

            # Check if the task has both images and annotations
            if os.path.exists(extracted_frames_dir) and os.path.exists(annotations_json_path):
                print(f"Processing task: {task_folder}")

                # Prepare paths for output
                output_image_dir = os.path.join(task_path, 'scaled_images')
                output_json_path = os.path.join(task_path, 'scaled_annotations.json')

                # Create output directory if it doesn't exist
                os.makedirs(output_image_dir, exist_ok=True)

                # Load JSON data for the current task
                with open(annotations_json_path, 'r') as f:
                    annotations = json.load(f)

                # Prepare new annotations list
                updated_annotations = []

                # Process each item in the annotations list
                for item in annotations:
                    if 'tracks' not in item:
                        updated_annotations.append(item)  # Keep other data unchanged
                        continue

                    updated_item = item.copy()
                    updated_item['tracks'] = []

                    for track in item['tracks']:
                        frame = track['frame']
                        file_name = f'{frame}_cropped.jpg'
                        image_path = os.path.join(extracted_frames_dir, file_name)

                        if not os.path.exists(image_path):
                            print(f"Image for frame {frame} not found.")
                            continue

                        image = Image.open(image_path)
                        original_size = image.size

                        # Resize the image
                        resized_image = image.resize(target_size)
                        resized_image.save(os.path.join(output_image_dir, f'{frame}_scaled.jpg'))

                        # Update bounding boxes in track
                        updated_track = track.copy()
                        updated_track['shapes'] = []

                        for shape in track['shapes']:
                            points = shape['points']
                            updated_points = scale_annotations(points, original_size, target_size)
                            updated_shape = shape.copy()
                            updated_shape['points'] = updated_points
                            updated_track['shapes'].append(updated_shape)

                        updated_item['tracks'].append(updated_track)

                    updated_annotations.append(updated_item)

                # Save updated JSON file
                with open(output_json_path, 'w') as f:
                    json.dump(updated_annotations, f, indent=4)

                print(f"Processed task: {task_folder} successfully!")

    print("All tasks processed successfully!")
