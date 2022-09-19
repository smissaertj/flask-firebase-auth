from settings import flask_config
from app import app

if __name__ == '__main__':
    app.run(port=flask_config['PORT'], debug=flask_config['DEBUG'])
