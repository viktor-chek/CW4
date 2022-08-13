from project.config import config
from project.server import create_app

app = create_app(config)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='25000')
