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
    data = request.json
    message = data.get('message')
    if message:
        # Here you would process the message and generate a response
        # For now just echo back the message
        return {"response": message}
    return {"error": "No message received"}

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
        if button_name == "Denoise":
            denoise(f"uploads/{file_name}")
        elif button_name == "Deblur":
            deblur(f"uploads/{file_name}")
        elif button_name == "Edge Detection":
            edgeDetection(f"uploads/{file_name}")
        elif button_name == "Segment":
            segment(f"uploads/{file_name}")
            
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
    app.run(host=HOST, port=PORT, debug=True)
