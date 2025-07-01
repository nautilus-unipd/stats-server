
from datetime import datetime
import os
import threading
import time
from flask import Blueprint, abort, render_template, send_file, request, redirect, url_for

sensors_bp = Blueprint('sensors', __name__,url_prefix='/sensors')

# Global variable to track if background logger is running
_logger_started = False
_logger_lock = threading.Lock()

def get_cpu_temperature():
    """Get CPU temperature using vcgencmd command"""
    try:
        result = os.popen('vcgencmd measure_temp').readline()
        temp_str = result.split('=')[1].strip().split("'")[0]
        return float(temp_str)
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return 0.0

def temperature_logger():
    """Background function to log temperature every 30 seconds"""
    log_file = os.path.join('static', 'logs', 'cpu_temp.log')
    
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    print("Background temperature logger started - logging every 30 seconds")
    
    while True:
        try:
            temp = get_cpu_temperature()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp}, Background Log, {temp:.2f}°C\n"
            
            with open(log_file, 'a') as f:
                f.write(log_entry)
                
            print(f"Background logged temperature: {temp:.2f}°C at {timestamp}")
            
        except Exception as e:
            print(f"Error in background temperature logging: {e}")
            
        time.sleep(30)  # Wait 30 seconds

def start_background_logger():
    """Start the background temperature logger if not already running"""
    global _logger_started
    
    with _logger_lock:
        if not _logger_started:
            logger_thread = threading.Thread(target=temperature_logger, daemon=True)
            logger_thread.start()
            _logger_started = True
            print("Background temperature logger thread started")


@sensors_bp.route('/', methods=['GET', 'POST'])
def sensors():
    # Start background logger if not already running
    start_background_logger()
    
    # If it's a POST request, redirect to GET to avoid refresh warnings
    if request.method == 'POST':
        return redirect(url_for('sensors.sensors'))
    
    # GET request - display the page
    # Get current temperature for immediate display
    cpu_temp = get_cpu_temperature()
    
    # Also log this manual reading
    os.makedirs('static/logs', exist_ok=True)
    log_file = 'static/logs/cpu_temp.log'
    with open(log_file, 'a') as f:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Manual Reading, {cpu_temp:.2f}°C\n"
        f.write(log_entry)
    
    # Read the log file content to pass to template
    log_content = ""
    try:
        with open(log_file, 'r') as f:
            # Read last 50 lines to avoid loading huge files
            lines = f.readlines()
            log_content = ''.join(lines[-50:]) if lines else "No log entries yet."
    except FileNotFoundError:
        log_content = "No log entries yet."
    
    return render_template('sensors.html', cpu_temp=cpu_temp, log_file=log_file, log_content=log_content)

@sensors_bp.app_template_filter()
def datetime_filter(value):
    """Template filter to format datetime from timestamp."""
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
