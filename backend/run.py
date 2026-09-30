from flask import Flask
from flask_cors import CORS
from config import Config
from extentions import close_db
from auth.oauth import register_oauth
from auth.routes import register_auth_routes
from users.routes import register_user_profile
from tasks.routes import register_task_routes
import os

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=[app.config['FRONTEND_URL']])

register_oauth(app)
register_auth_routes(app)
register_user_profile(app)
register_task_routes(app)

app.teardown_appcontext(close_db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)