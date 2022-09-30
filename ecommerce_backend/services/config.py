import os

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret