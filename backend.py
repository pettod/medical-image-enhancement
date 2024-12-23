from bottle import Bottle, request, static_file
import os

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
    
    if file_name and os.path.exists(f"uploads/{file_name}"):
        os.remove(f"uploads/{file_name}")
        return {"message": f"File {file_name} deleted after {button_name} operation"}
    else:
        return {"message": f"File not found"}

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
