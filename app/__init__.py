from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# app = Flask(__name__)
# app.config.from_object(Config)
db = SQLAlchemy(conn)


from app import routes, models




# DATABASE_URL=postgres://{user}:{password}@{hostname}:{port}/{database-name}
