
from flask import Flask

app = Flask(__name__)
app.secret_key = b'wghF8A6py9RKkVEPNYbE'
from app import views

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
print(f'ENV is set to: {app.config["ENV"]}')