"""Blueprint for main/core routes."""

from datetime import datetime
import os
from flask import Blueprint, abort, render_template, send_file, request

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Main directory browser route."""
    BASE_DIR = os.path.expanduser("~")
    
    # Get the directory from query parameter, default to BASE_DIR
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
    try:
        return render_template('index.html', files=list(files), current_path=req_path)
    except Exception as e:
        print(f"Error rendering index: {e}")
        return abort(500)


@main_bp.app_template_filter()
def datetime_filter(value):
    """Template filter to format datetime from timestamp."""
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
