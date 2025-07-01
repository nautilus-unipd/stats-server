from flask import Flask
from blueprints.main import main_bp
from blueprints.images import images_bp
from blueprints.logs import logs_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(images_bp)
app.register_blueprint(logs_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

