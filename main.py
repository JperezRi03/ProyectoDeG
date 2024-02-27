from flask import Flask
from routes import register_routes

app = Flask(__name__, template_folder='templates')
app.secret_key = 'Val06Ju'

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
