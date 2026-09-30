from flask import redirect
from auth.jwt_utils import create_jwt
from extentions import get_db
from auth.oauth import oauth

def register_auth_routes(app):
    @app.route('/auth/google/login')
    def google_login():
        redirect_uri = 'http://localhost:5000/auth/google/callback'
        return oauth.google.authorize_redirect(redirect_uri)

    @app.route('/auth/google/callback')
    def google_callback():
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT id FROM users WHERE google_id = %s", (user_info['sub'],))
        row = cur.fetchone()

        if row is None:
            cur.execute("INSERT INTO users (google_id, email, name) VALUES (%s, %s, %s) RETURNING id", (user_info['sub'], user_info['email'], user_info.get('name'))
                    
                    )
            row = cur.fetchone()
            db.commit()

        user_id = row['id']
        access_token = create_jwt(user_id)
        return redirect(f"{app.config['FRONTEND_URL']}/auth/callback?acces_token={access_token}")