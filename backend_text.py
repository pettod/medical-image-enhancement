from bottle import Bottle, request, static_file
import os
import argparse

from deblur import deblur
from denoise import denoise
from segment import segment
from edge_detection import edgeDetection

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--global', default=None, action='store_true', help='Use 0.0.0.0 instead of localhost')
parser.add_argument('--port', default=8080, type=int, help='Port to run the server on')
args = parser.parse_args()

# Set host based on args
HOST = '0.0.0.0' if getattr(args, 'global') else 'localhost'
PORT = args.port

app = Bottle()

# Serve static files (HTML, CSS, JS)
@app.route('/test')
def serve_index():
    return static_file('index_text.html', root='.')

# Handle chat messages
@app.route('/message', method='POST')
def handle_message():
    data = request.forms
    message = data.get('message')
    filename = data.get('filename')
    if message:
        if "segment" in message:
            print("Message:", message)
            if "nucleau" in message:
                print("Segmenting nucleus")
                segment(f"uploads/{filename}", channels=[3,0])
            elif "cytoplasm" in message:
                print("Segmenting cytoplasm")
                segment(f"uploads/{filename}", channels=[0,0])
            else:
                response = {"message": "Please specify whether you want to segment the nucleus or the cytoplasm."}
            response = {
                "image": filename,
                "message": "Here's the segmented image. Anything else?"
            }
        elif "statistics" in message:
            response = {"message": "The statistics are as follows: 78 cells were identified, with a total segmented area of 1231 pixels, corresponding to a cell density of 78.4%."}
        elif "hi" in message:
            response = {"message": "Hello! How can I help you today?"}
        else:
            response = {"message": "Sorry, I don't understand. Please ask me something else."}
        return response
    return {"error": "No message received"}

# Serve the file from the uploads directory
@app.route('/uploads/<filename>')
def serve_file(filename):
    return static_file(filename, root='uploads', mimetype='image/jpeg')

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
    filename = data.get('filename')

    print(button_name)
    if filename and os.path.exists(f"uploads/{filename}"):
        if button_name == "Denoise":
            denoise(f"uploads/{filename}")
        elif button_name == "Deblur":
            deblur(f"uploads/{filename}")
        elif button_name == "Edge Detection":
            edgeDetection(f"uploads/{filename}")
        elif button_name == "Segment":
            segment(f"uploads/{filename}")
            
        # Return the rotated image
        response = static_file(filename, root='uploads', mimetype='image/jpeg')
        #os.remove(f"uploads/{filename}")
        return response
    else:
        return {"message": f"File not found"}

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Run the server
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
