from os import environ
import secrets

import dotenv

dotenv.load_dotenv()


MONGO_HOSTNAME = environ.get("MONGO_HOSTNAME")
MONGO_PORT = int(environ.get("MONGO_PORT", "27017"))
MONGO_USERNAME = environ.get("MONGO_USERNAME")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD")
MONGO_DATABASE = environ.get("MONGO_DATABASE")
SESSION_SECRET = environ.get("SESSION_SECRET", secrets.token_hex(16))

RUN_MIGRATIONS = environ.get("RUN_MIGRATIONS", "false").lower() == "true"
AUTO_RELOAD = environ.get("AUTO_RELOAD", "true").lower() == "true"