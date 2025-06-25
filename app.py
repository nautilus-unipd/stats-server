from datetime import datetime
import os
from flask import Flask, abort, render_template, send_file, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    BASE_DIR = os.path.expanduser("~")
    
    # Get the directory from query parameter, default to empty string
    req_path = request.args.get('path', BASE_DIR)
    
    # Return 404 if path doesn't exist
    if not os.path.exists(req_path):
        return abort(404)
    
    # Check if path is a file and serve
    if os.path.isfile(req_path):
        return send_file(req_path)
    
    # Show directory contents
    files = os.scandir(req_path)            
    files = sorted(files, key=lambda e: e.name)

    return render_template('index.html', files=list(files), current_path=req_path)

@app.route('/images/', methods=['GET', 'POST'])
def images():
    image_extensions = (
    '.jpg',  # Joint Photographic Experts Group (JPEG)
    '.jpeg', # Joint Photographic Experts Group (JPEG)
    '.png',  # Portable Network Graphics
    '.gif',  # Graphics Interchange Format
    '.bmp',  # Bitmap
    '.tiff', # Tagged Image File Format
    '.tif',  # Tagged Image File Format
    '.webp', # WebP (Google's modern image format)
    '.heic', # High Efficiency Image File Format (Apple)
    '.heif', # High Efficiency Image File Format
    '.raw',  # Raw image formats (various camera manufacturers)
    '.dng',  # Digital Negative (Adobe standard raw)
    '.jp2',  # JPEG 2000
    '.jpf',  # JPEG 2000 Part 2 (extended JP2)
    '.jpm',  # JPEG 2000 Part 6 (compound image file format)
    '.svg',  # Scalable Vector Graphics (XML-based vector image format)
    '.ico',  # Icon file format (Windows icons)
    '.jfif', # JPEG File Interchange Format (older JPEG variant)
    '.rle',  # Run-length encoded bitmap (older Windows bitmap variant)
    '.exif', # Exchangeable Image File Format (data often embedded in JPEGs/TIFFs)
    '.ppm',  # Portable Pixmap Format
    '.pgm',  # Portable Graymap Format
    '.pbm',  # Portable Bitmap Format
    '.pnm',  # Portable Anymap Format (PPM, PGM, PBM)
    '.hdr',  # High Dynamic Range (various specific formats like Radiance HDR)
    )

    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return abort(404)
    
    images = []
    for entry in os.scandir(path):
        if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in image_extensions):
            images.append(entry.path)  # Use full path
            
    return render_template('images.html', path=path, images=images)

@app.route('/log/', methods=['GET', 'POST'])
def log():
    return 'Hello log'

@app.template_filter()
def datetime_filter(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/serve-image')
def serve_image():
    filepath = request.args.get('filepath')
    if not filepath or not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return abort(404)
    
    try:
        return send_file(filepath, mimetype='image/jpeg')  # Or use mimetypes.guess_type(filepath)[0]
    except Exception as e:
        print(f"Error serving image: {e}")
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True)
