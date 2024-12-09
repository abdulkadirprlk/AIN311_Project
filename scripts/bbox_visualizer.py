import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


def visualize_bboxes(image_path, bboxes, title="Bounding Boxes"):
    """
    Visualizes bounding boxes on an image.

    Parameters:
    - image_path (str): Path to the image file.
    - bboxes (list of lists): Bounding boxes as [[x_min, y_min, x_max, y_max], ...].
    - title (str): Title of the plot.

    Returns:
    - None: Displays the image with bounding boxes.
    """
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image)
    ax.set_title(title)
    ax.axis("off")

    # Draw each bounding box
    for bbox in bboxes:
        x_min, y_min, x_max, y_max = bbox

        # Calculate width and height of the bounding box
        bbox_width = x_max - x_min
        bbox_height = y_max - y_min

        # Create a rectangle patch
        rect = patches.Rectangle(
            (x_min, y_min), bbox_width, bbox_height,
            linewidth=2, edgecolor='r', facecolor='none'
        )

        # Add the patch to the axes
        ax.add_patch(rect)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Example usage
    image_path = '/Users/abdulkadir/Documents/AIN313 Machine Learning/AIN313_Project/dataset/task_kam2_gh078416/cropped_images/653_cropped.jpg'
    bboxes = [[
                            459.2001953125,
                            421.16015625,
                            602.1201171875,
                            496.8000000000011
                        ]]  # Example bounding boxes
    visualize_bboxes(image_path, bboxes, title="Example Bounding Boxes")
