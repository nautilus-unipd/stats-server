"""Blueprint for log-related routes."""

from datetime import datetime
import io
import os
import zipfile
from flask import Blueprint, abort, render_template, send_file, request

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')


@logs_bp.route('/', methods=['GET', 'POST'])
def logs():
    """Display logs in a directory."""
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return abort(404)

    logs = []
    for entry in os.scandir(path):
        if entry.is_file():
            logs.append(entry.path)  # Use full path
    try:
        return render_template('logs.html', path=path, logs=logs)
    except Exception as e:
        print(f"Error processing logs: {e}")
        return abort(500)


@logs_bp.route('/serve')
def serve_logs():
    """Serve an individual log file."""
    log_path = request.args.get('path')
    if not log_path or not os.path.isfile(log_path):
        return abort(404)

    try:
        return send_file(log_path)
    except Exception as e:
        print(f"Error serving log file: {e}")
        return abort(404)


@logs_bp.route('/download-all')
def download_all_logs():
    """Download all logs in a directory as a zip file."""
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return abort(404)

    logs = [entry.path for entry in os.scandir(path) if entry.is_file()]
    if not logs:
        return abort(404)

    try:
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for log_path in logs:
                zip_file.write(log_path, arcname=os.path.basename(log_path))
        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, 
                        download_name=f'logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip', 
                        mimetype='application/zip')
    except Exception as e:
        print(f"Error sending all logs: {e}")
        return abort(500)
