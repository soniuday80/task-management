from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session, request

oauth = OAuth()

def register_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        openid_configuration_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }   
        
    )
