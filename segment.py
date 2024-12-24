import cv2
import numpy as np


def contour_segmentation(input_path):
    # Load the image
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty segmentation map
    segmentation_map = np.zeros_like(gray)

    # Draw each contour with a unique color (here, different intensity)
    for i, contour in enumerate(contours):
        cv2.drawContours(segmentation_map, [contour], -1, (i * 20), -1)

    # Save the segmented image
    cv2.imwrite(input_path, segmentation_map)


def segment(input_path):
    contour_segmentation(input_path)
