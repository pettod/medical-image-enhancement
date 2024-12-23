from bottle import Bottle, request, static_file
import os
from PIL import Image
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--global', default=None, action='store_true', help='Use 0.0.0.0 instead of localhost')
args = parser.parse_args()

# Set host based on args
HOST = '0.0.0.0' if getattr(args, 'global') else 'localhost'

app = Bottle()

# Serve static files (HTML, CSS, JS)
@app.route('/')
def serve_index():
    return static_file('index.html', root='.')

# Handle file uploads
@app.route('/upload', method='POST')
def handle_upload():
    upload = request.files.get('file')
    if upload:
        # Get file name and extension
        name, ext = os.path.splitext(upload.filename)
        # Check if file exists and remove it
        if os.path.exists(f"uploads/{upload.filename}"):
            os.remove(f"uploads/{upload.filename}")
        # Save file
        upload.save(f"uploads/{upload.filename}")
        return {"message": f"File {upload.filename} uploaded successfully"}
    return {"message": "No file received"}

# Handle button clicks
@app.route('/button-click', method='POST')
def handle_button():
    data = request.json
    button_name = data.get('button_name')
    file_name = data.get('file_name')

    print(button_name)
    if file_name and os.path.exists(f"uploads/{file_name}"):
        rotation = 0
        if button_name == "Denoise":
            rotation = 90
        elif button_name == "Deblur":
            rotation = 180
        elif button_name == "Super Resolve":
            rotation = -90
        elif button_name == "Segment":
            rotation = -90

        # Open and rotate the image
        img_path = f"uploads/{file_name}"
        with Image.open(img_path) as img:
            # Rotate 90 degrees clockwise
            rotated = img.rotate(rotation, expand=True)
            # Save rotated image
            rotated.save(img_path)
            
        # Return the rotated image
        response = static_file(file_name, root='uploads', mimetype='image/jpeg')
        #os.remove(f"uploads/{file_name}")
        return response
    else:
        return {"message": f"File not found"}

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Run the server
if __name__ == '__main__':
    app.run(host=HOST, port=8080, debug=True)
