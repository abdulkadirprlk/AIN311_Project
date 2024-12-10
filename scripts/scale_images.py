import json
import os
from PIL import Image


def scale_annotations(points, original_size, new_size):
    orig_w, orig_h = original_size
    new_w, new_h = new_size

    scale_x = new_w / orig_w
    scale_y = new_h / orig_h

    return [
        points[0] * scale_x, points[1] * scale_y,
        points[2] * scale_x, points[3] * scale_y
    ]

def process_task(task_path, target_size):
    cropped_images_dir = os.path.join(task_path, 'cropped_images')
    annotations_json_path = os.path.join(task_path, 'cropped_annotations.json')

    if not (os.path.exists(cropped_images_dir) and os.path.exists(annotations_json_path)):
        print(f"Skipping {task_path}, required files not found.")
        return

    # Output paths
    output_image_dir = os.path.join(task_path, 'scaled_images')
    output_json_path = os.path.join(task_path, 'scaled_annotations.json')
    os.makedirs(output_image_dir, exist_ok=True)

    # Load annotations
    with open(annotations_json_path, 'r') as f:
        annotations = json.load(f)

    # Create a dictionary to store the shapes for each frame
    frame_shapes = {}
    for item in annotations:
        for shape in item['shapes']:
            frame = shape['frame']
            if frame not in frame_shapes:
                frame_shapes[frame] = []
            frame_shapes[frame].append(shape)

    updated_annotations = []

    for frame, shapes in frame_shapes.items():
        file_name = f'{frame}_cropped.jpg'
        image_path = os.path.join(cropped_images_dir, file_name)

        if not os.path.exists(image_path):
            print(f"Image for frame {frame} not found.")
            continue

        try:
            # Resize image
            image = Image.open(image_path)
            original_size = image.size
            resized_image = image.resize(target_size)
            resized_image.save(os.path.join(output_image_dir, f'{frame}_scaled.jpg'))

            # Scale bounding box
            updated_shapes = []
            for shape in shapes:
                updated_shape = shape.copy()
                updated_shape['points'] = scale_annotations(
                    shape['points'], original_size, target_size
                )
                updated_shapes.append(updated_shape)

            updated_annotations.append({
                'frame': frame,
                'shapes': updated_shapes
            })
        except Exception as e:
            print(f"Error processing frame {frame}: {e}")
            continue

    # Save updated annotations
    with open(output_json_path, 'w') as f:
        json.dump(updated_annotations, f, indent=4)

    print(f"Processed {task_path} successfully!")


if __name__ == "__main__":
    dataset_dir = r'//dataset'
    target_size = (180, 180)

    for task_folder in os.listdir(dataset_dir):
        task_path = os.path.join(dataset_dir, task_folder)
        if os.path.isdir(task_path):
            process_task(task_path, target_size)

    print("All tasks processed successfully!")
