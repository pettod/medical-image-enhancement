import cv2
import numpy as np


def sobel_edge_detection(input_path):
    # Read the image in grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if image is loaded successfully
    if img is None:
        print("Error: Image not found!")
        return
    
    # Apply Sobel operator in the X direction (horizontal edges)
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    
    # Apply Sobel operator in the Y direction (vertical edges)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    
    # Compute the magnitude of gradients (edge strength)
    magnitude = cv2.magnitude(sobel_x, sobel_y)
    
    # Convert the magnitude to uint8 format for display
    edges = np.uint8(np.absolute(magnitude))
    
    # Save the result
    cv2.imwrite(input_path, edges)


def edgeDetection(input_path):
    sobel_edge_detection(input_path)
