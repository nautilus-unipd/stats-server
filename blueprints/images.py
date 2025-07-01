"""Blueprint for image-related routes."""

from datetime import datetime
import io
import os
import zipfile
from flask import Blueprint, abort, render_template, send_file, request
from utils.constants import IMAGE_EXTENSIONS

images_bp = Blueprint('images', __name__, url_prefix='/images')


@images_bp.route('/', methods=['GET', 'POST'])
def images():
    """Display images in a directory."""
    path = request.args.get('path')
    page = request.args.get('page', 1, type=int)
    
    img_per_page = 18  
    
    if not path or not os.path.exists(path):
        return abort(404)
    
    images = []
    for entry in os.scandir(path):
        if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            images.append(entry.path)  # Use full path
            
    start = (page - 1) * img_per_page
    end = start + img_per_page

    total_pages = (len(images) + img_per_page - 1) // img_per_page  
    
    try:
        return render_template('images.html', path=path, images=images[start:end], page=page, total_pages=total_pages)
    except Exception as e:
        print(f"Error processing images: {e}")
        return abort(500)


@images_bp.route('/serve')
def serve_image():
    """Serve an individual image file."""
    filepath = request.args.get('filepath')
    if not filepath or not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return abort(404)
    
    try:
        return send_file(filepath, mimetype='image/jpeg')  # Or use mimetypes.guess_type(filepath)[0]
    except Exception as e:
        print(f"Error serving image: {e}")
        return abort(404)


@images_bp.route('/download')
def download_image():
    """Download an individual image file."""
    filepath = request.args.get('filepath')
    if not filepath or not os.path.isfile(filepath):
        abort(404)
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        print(f"Error sending file for download: {e}")
        abort(500)


@images_bp.route('/download-all')
def download_all_images():
    """Download all images in a directory as a zip file."""
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return abort(404)

    images = [entry.path for entry in os.scandir(path) 
              if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]
    if not images:
        return abort(404)

    try:
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for image_path in images:
                zip_file.write(image_path, arcname=os.path.basename(image_path))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, 
                        download_name=f'images_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip', 
                        mimetype='application/zip')
    except Exception as e:
        print(f"Error sending all images: {e}")
        return abort(500)
