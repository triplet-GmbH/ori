from os import environ
import dotenv

dotenv.load_dotenv()


MONGO_HOSTNAME = environ.get("MONGO_HOSTNAME")
MONGO_PORT = int(environ.get("MONGO_PORT"))
MONGO_USERNAME = environ.get("MONGO_USERNAME")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD")
MONGO_DATABASE = environ.get("MONGO_DATABASE")
