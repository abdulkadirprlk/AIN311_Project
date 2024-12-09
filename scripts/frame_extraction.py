import json
import os
import cv2


# Extract relevant frames
def extract_frames(json_data):
    frames = set()
    for item in json_data:
        for track in item.get("tracks", []):
            for shape in track.get("shapes", []):
                if not shape.get("outside", False):
                    frames.add(shape["frame"])
    return sorted(frames)


if __name__ == "__main__":
    # Base directory containing all tasks
    base_dir = "/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset"

    # Loop through all task folders
    for task_folder in os.listdir(base_dir):
        task_path = os.path.join(base_dir, task_folder)

        if os.path.isdir(task_path):  # Process only directories
            json_file = os.path.join(task_path, "annotations.json")
            video_folder = os.path.join(task_path, "data")

            # Find the video file in the 'data' subfolder (assuming it is the only video file)
            video_file = None
            for file in os.listdir(video_folder):
                if file.endswith(".mp4"):
                    video_file = os.path.join(video_folder, file)
                    break

            # Check if both JSON file and video exist
            if os.path.exists(json_file) and video_file:
                # Output directory for frames
                output_dir = os.path.join(task_path, "extracted_frames")
                os.makedirs(output_dir, exist_ok=True)

                # Load JSON dataset
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    relevant_frames = extract_frames(data)
                    print(f"Relevant Frames in {json_file}: {relevant_frames}")

                # Open the video
                cap = cv2.VideoCapture(video_file)

                if not cap.isOpened():
                    print(f"Error: Cannot open video {video_file}")
                    continue

                # Read frames in sequence and save relevant ones (sequential reading instead of seeking)
                frame_idx = 0
                ret = True
                while ret:
                    ret, frame = cap.read()
                    if frame_idx in relevant_frames:
                        output_file = os.path.join(output_dir, f"frame_{frame_idx:05d}.jpg")

                        # Check if the frame already exists
                        if not os.path.exists(output_file):
                            cv2.imwrite(output_file, frame)
                            print(f"Saved frame {frame_idx} to {output_file}")
                        else:
                            print(f"Frame {frame_idx} already exists, skipping...")
                    frame_idx += 1

                cap.release()

            else:
                print(f"Missing JSON or video file for task {task_folder}. Skipping...")

    print("Frame extraction complete.")
