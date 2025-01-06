import numpy as np
from cellpose import models
from PIL import Image
import torch


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu") # else "mps" if torch.backends.mps.is_available()


def segment(image_path, output_path=None, channels=[0, 0]):
    img = np.array(Image.open(image_path))
    model = models.Cellpose(model_type='cyto3', device=DEVICE)

    # Run Cellpose to get masks
    out = model.eval(img, diameter=None, channels=channels)
    masks = out[0]

    # For each detected cell/object
    output = np.zeros_like(img)
    for i in range(1, masks.max()+1):
        # Get mask for current object
        mask = masks == i
        colorMask(mask, img, i, output, different_colors=True)

    # Add alpha channel for transparency
    if image_path.endswith('.png'):
        output_rgba = np.zeros((output.shape[0], output.shape[1], 4), dtype=output.dtype)
        output_rgba[..., :3] = output
        output_rgba[..., 3] = 255  # Set fully opaque by default
    
        # Make zero values transparent
        zero_mask = np.all(output == 0, axis=2)
        output_rgba[zero_mask, 3] = 0
        output = output_rgba

    if output_path:
        Image.fromarray(output).save(output_path)
    else:
        Image.fromarray(output).save(image_path)


def colorMask(mask, img, i, output, different_colors=False):
    if different_colors:
        # Calculate mean intensity of the image in the mask region
        mask_mean = np.mean(img[mask])
        
        # Choose base colors that contrast with mean intensity
        if mask_mean < 128:
            # For darker regions, use bright colors with random variation
            base_color = (
                np.random.randint(200, 256),  # red component
                np.random.randint(200, 256),  # green component
                np.random.randint(200, 256)   # blue component
            )
        else:
            # For brighter regions, use darker colors with random variation
            base_color = (
                np.random.randint(0, 180),  # red component
                np.random.randint(0, 180),  # green component 
                np.random.randint(0, 180)   # blue component
            )
            
        # Add small random variations to each color channel
        r = min(255, max(0, base_color[0] + np.random.randint(-20, 21)))
        g = min(255, max(0, base_color[1] + np.random.randint(-20, 21)))
        b = min(255, max(0, base_color[2] + np.random.randint(-20, 21)))
        
        output[mask, 0] = r
        output[mask, 1] = g 
        output[mask, 2] = b
    else:
        # Apply different colors per channel
        # Red channel - invert
        output[mask, 0] = 255 - np.mean(img[mask, 0])
        # Green channel - enhance
        output[mask, 1] = min(255, np.mean(img[mask, 1]) * 1.5)
        # Blue channel - reduce 
        output[mask, 2] = max(0, np.mean(img[mask, 2]) * 0.7)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python segment.py <input_image_path>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = input_path.rsplit('.', 1)[0] + '_segmented.' + input_path.rsplit('.', 1)[1]
    segment(input_path, output_path)
