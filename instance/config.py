import os
from dotenv import load_dotenv

load_dotenv()
OUR_HOST=os.getenv("DB_HOST", "")
OUR_DB=os.getenv("DB_DB", "")
OUR_USER=os.getenv("DB_USER", "")
OUR_PORT=os.getenv("DB_PORT", "")
OUR_PW=os.getenv("DB_PW", "")
OUR_SECRET=os.getenv("SECRET", "")
OUR_JWTSECRET=os.getenv("JWTSECRET", "")

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET
SECRET_KEY = OUR_SECRET

## $env:FLASK_APP="apirest"
## $env:FLASK_ENV="development"
## flask run --host=0.0.0.0