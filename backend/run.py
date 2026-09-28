from flask import Flask
from flask_cors import CORS
from config import Config
from backend.extentions import close_db
from auth.oauth import register_oauth
from auth.routes import register_auth_routes


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=[app.config['FRONTEND_URL']])

register_oauth(app)
register_auth_routes(app)

app.teardown_appcontext(close_db)

if __name__ == '__main__':
    app.run(debug=True)