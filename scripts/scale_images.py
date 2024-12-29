import json
import os
from PIL import Image

def scale_images_and_annotations(dataset_dir, target_width, target_height):
    for task_folder in os.listdir(dataset_dir):
        task_path = os.path.join(dataset_dir, task_folder)

        if os.path.isdir(task_path):
            cropped_images_dir = os.path.join(task_path, 'cropped_images')
            cropped_annotations_path = os.path.join(task_path, 'cropped_annotations.json')

            if os.path.exists(cropped_images_dir) and os.path.exists(cropped_annotations_path):
                print(f"Processing scaling for task: {task_folder}")

                scaled_images_dir = os.path.join(task_path, 'scaled_images')
                scaled_annotations_path = os.path.join(task_path, 'scaled_annotations.json')

                os.makedirs(scaled_images_dir, exist_ok=True)

                with open(cropped_annotations_path, 'r') as f:
                    annotations = json.load(f)

                # Copy annotations to maintain the original hierarchy
                updated_annotations = annotations.copy()

                # Scaling factor
                scale_x = target_width / 1080
                scale_y = target_height / 1080

                for track in updated_annotations[0]['tracks']:
                    for shape in track['shapes']:
                        # Scale bounding box coordinates
                        x_min, y_min, x_max, y_max = shape['points']
                        shape['points'] = [
                            x_min * scale_x, y_min * scale_y,
                            x_max * scale_x, y_max * scale_y
                        ]

                for file_name in os.listdir(cropped_images_dir):
                    if file_name.endswith('.jpg'):
                        image_path = os.path.join(cropped_images_dir, file_name)
                        image = Image.open(image_path)

                        # Resize the image using LANCZOS filter
                        scaled_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        scaled_image.save(os.path.join(scaled_images_dir, file_name))

                # Save updated annotations
                with open(scaled_annotations_path, 'w') as f:
                    json.dump(updated_annotations, f, indent=4)

                print(f"Scaling completed for task: {task_folder}")

if __name__ == "__main__":
    dataset_dir = r'/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN311_Project/dataset'
    target_width, target_height = 180, 180
    scale_images_and_annotations(dataset_dir, target_width, target_height)
