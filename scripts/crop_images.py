import json
import os
from PIL import Image

if __name__ == "__main__":
    dataset_dir = r'/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset'

    fixed_width, fixed_height = 1080, 1080

    for task_folder in os.listdir(dataset_dir):
        task_path = os.path.join(dataset_dir, task_folder)

        if os.path.isdir(task_path):
            extracted_frames_dir = os.path.join(task_path, 'extracted_frames')
            annotations_json_path = os.path.join(task_path, 'annotations.json')

            if os.path.exists(extracted_frames_dir) and os.path.exists(annotations_json_path):
                print(f"Processing task: {task_folder}")

                output_image_dir = os.path.join(task_path, 'cropped_images')
                output_json_path = os.path.join(task_path, 'cropped_annotations.json')

                os.makedirs(output_image_dir, exist_ok=True)

                with open(annotations_json_path, 'r') as f:
                    annotations = json.load(f)

                updated_annotations = []

                for track in annotations[0]['tracks']:
                    for shape in track['shapes']:
                        frame = shape['frame']

                        if shape['outside']:
                            continue

                        file_name = f'frame_{frame:05}.jpg'
                        image_path = os.path.join(extracted_frames_dir, file_name)

                        if not os.path.exists(image_path):
                            print(f"Image for frame {frame} not found.")
                            continue

                        image = Image.open(image_path)
                        width, height = image.size

                        x_min, y_min, x_max, y_max = shape['points']

                        center_x = (x_min + x_max) / 2
                        center_y = (y_min + y_max) / 2

                        crop_x_min = max(int(center_x - fixed_width / 2), 0)
                        crop_y_min = max(int(center_y - fixed_height / 2), 0)
                        crop_x_max = min(int(center_x + fixed_width / 2), width)
                        crop_y_max = min(int(center_y + fixed_height / 2), height)

                        if crop_x_max - crop_x_min < fixed_width:
                            crop_x_min = max(0, crop_x_max - fixed_width)
                            crop_x_max = crop_x_min + fixed_width

                        if crop_y_max - crop_y_min < fixed_height:
                            crop_y_min = max(0, crop_y_max - fixed_height)
                            crop_y_max = crop_y_min + fixed_height

                        updated_shape = shape.copy()
                        updated_shape['points'] = [
                            x_min - crop_x_min, y_min - crop_y_min,
                            x_max - crop_x_min, y_max - crop_y_min
                        ]

                        updated_track = track.copy()
                        updated_track['shapes'] = [updated_shape]

                        cropped_image = image.crop((crop_x_min, crop_y_min, crop_x_max, crop_y_max))
                        cropped_image.save(os.path.join(output_image_dir, f'{frame}_cropped.jpg'))

                        updated_annotations.append(updated_track)

                with open(output_json_path, 'w') as f:
                    json.dump(updated_annotations, f, indent=4)

                print(f"Processed task: {task_folder} successfully!")

    print("All tasks processed successfully!")
