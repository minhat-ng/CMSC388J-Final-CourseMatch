# Stores all configuration values
import certifi
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGODB_HOST = os.environ.get('MONGODB_HOST')
# pass = CIrvD08SGbew9j8V