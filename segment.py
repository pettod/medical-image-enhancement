import numpy as np
from cellpose import models
from PIL import Image


def segment(image_path, output_path=None):
    img = np.array(Image.open(image_path))
    model = models.Cellpose(model_type='cyto')

    # Run Cellpose to get masks
    out = model.eval(img, diameter=None, channels=[0,0])
    masks = out[0]

    # For each detected cell/object
    output = np.zeros_like(img)
    for i in range(1, masks.max()+1):
        # Get mask for current object
        mask = masks == i

        # Apply different colors per channel
        # Red channel - invert
        output[mask, 0] = 255 - np.mean(img[mask, 0])
        # Green channel - enhance
        output[mask, 1] = min(255, np.mean(img[mask, 1]) * 1.5)
        # Blue channel - reduce 
        output[mask, 2] = max(0, np.mean(img[mask, 2]) * 0.7)

    # Add alpha channel for transparency
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


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python segment.py <input_image_path>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = input_path.rsplit('.', 1)[0] + '_segmented.' + input_path.rsplit('.', 1)[1]
    denoised = segment(input_path, output_path)
