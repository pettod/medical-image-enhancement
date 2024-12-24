import cv2
import numpy as np


def sharpen_image(img):
    # Create a Gaussian blur of the image
    blur = cv2.GaussianBlur(img, (0, 0), 3.0)
    
    # Calculate the unsharp mask by subtracting the blurred image
    unsharp_mask = cv2.addWeighted(img, 2.5, blur, -1.5, 0)
    
    # Ensure pixel values stay within valid range
    return np.clip(unsharp_mask, 0, 255).astype(np.uint8)


def deblur(input_path):
    # Load the image
    img = cv2.imread(input_path)
    
    # Apply sharpening
    sharpened = sharpen_image(img)
    
    # Save the result
    cv2.imwrite(input_path, sharpened)
