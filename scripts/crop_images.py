import json
import os
from PIL import Image

if __name__ == "__main__":
    # Path to the main dataset directory
    dataset_dir = r'/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset_frame_backup'

    # Fixed crop size
    fixed_width, fixed_height = 1080, 1080

    # Loop through each task folder in the dataset
    for task_folder in os.listdir(dataset_dir):
        task_path = os.path.join(dataset_dir, task_folder)

        # Check if it's a directory and contains the necessary subdirectories
        if os.path.isdir(task_path):
            extracted_frames_dir = os.path.join(task_path, 'extracted_frames')
            annotations_json_path = os.path.join(task_path, 'annotations.json')

            # Check if the task has both images and annotations
            if os.path.exists(extracted_frames_dir) and os.path.exists(annotations_json_path):
                print(f"Processing task: {task_folder}")

                # Prepare paths for output
                output_image_dir = os.path.join(task_path, 'cropped_images')
                output_json_path = os.path.join(task_path, 'updated_annotations.json')

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
                        file_name = f'frame_{frame:05}.jpg'
                        image_path = os.path.join(extracted_frames_dir, file_name)

                        if not os.path.exists(image_path):
                            print(f"Image for frame {frame} not found.")
                            continue

                        image = Image.open(image_path)
                        width, height = image.size

                        # Find bounding box extremes
                        x_min = min(shape['points'][0] for shape in track['shapes'])
                        y_min = min(shape['points'][1] for shape in track['shapes'])
                        x_max = max(shape['points'][2] for shape in track['shapes'])
                        y_max = max(shape['points'][3] for shape in track['shapes'])

                        # Center the crop around the bounding box
                        center_x = (x_min + x_max) // 2
                        center_y = (y_min + y_max) // 2

                        # Calculate crop boundaries
                        crop_x_min = max(center_x - fixed_width // 2, 0)
                        crop_y_min = max(center_y - fixed_height // 2, 0)
                        crop_x_max = min(center_x + fixed_width // 2, width)
                        crop_y_max = min(center_y + fixed_height // 2, height)

                        # Adjust cropping if image size is smaller than fixed size
                        if crop_x_max - crop_x_min < fixed_width:
                            crop_x_min = max(0, crop_x_max - fixed_width)
                            crop_x_max = crop_x_min + fixed_width

                        if crop_y_max - crop_y_min < fixed_height:
                            crop_y_min = max(0, crop_y_max - fixed_height)
                            crop_y_max = crop_y_min + fixed_height

                        # Update bounding boxes in track
                        updated_track = track.copy()
                        updated_track['shapes'] = []

                        for shape in track['shapes']:
                            points = shape['points']
                            updated_shape = shape.copy()
                            updated_shape['points'] = [
                                points[0] - crop_x_min, points[1] - crop_y_min,
                                points[2] - crop_x_min, points[3] - crop_y_min
                            ]
                            updated_track['shapes'].append(updated_shape)

                        updated_item['tracks'].append(updated_track)

                        # Crop and save the image
                        cropped_image = image.crop((crop_x_min, crop_y_min, crop_x_max, crop_y_max))
                        cropped_image.save(os.path.join(output_image_dir, f'{frame}_cropped.jpg'))

                    updated_annotations.append(updated_item)

                # Save updated JSON file
                with open(output_json_path, 'w') as f:
                    json.dump(updated_annotations, f, indent=4)

                print(f"Processed task: {task_folder} successfully!")

    print("All tasks processed successfully!")
