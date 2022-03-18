# TODO: core.variables
import os

ENV = 'dev'

ADMIN_ENABLED = True

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-5owfq%%7(d!)+6^sxc+g637hh9+obhk4fj8_(a5e)3ngir8v^+')

DATABASES = {
    'host': os.environ.get('DATABASE_HOST', 'localhost'),
    'user': os.environ.get('DATABASE_USER', 'root'),
    'pass': os.environ.get('DATABASE_PASS', 'root'),
    'name': os.environ.get('DATABASE_NAME', 'ecaziz_db'),
    'port': os.environ.get('DATABASE_PORT', '3306'),
}

HASHIDS_SALT = {
    'user_id': 'HzN8V2zfccyTcAAL',
    'undangan_id': 'RchKkW2Rm798kqyq',
    'ucapan_id': '5ApYwHieqQRB0ccF',
    'auth_id': 'rR62Of3khjQNKU0o'
}

ALLOWED_HOSTS = [
    '192.168.6.26'
]

ALLOWED_ORIGINS = []

CSRF_TRUSTED = []

JWT_EXPIRED = 30

app_config = {
    'environment': ENV,
    'secret_key': SECRET_KEY,
    'db_host': DATABASES.get('host'),
    'db_port': DATABASES.get('post'),
    'db_user': DATABASES.get('user'),
    'db_pass': DATABASES.get('pass'),
    'db_name': DATABASES.get('name'),
    'salt_user': HASHIDS_SALT.get('user_id'),
    'salt_undangan': HASHIDS_SALT.get('undangan_id'),
    'salt_ucapan': HASHIDS_SALT.get('ucapan_id'),
    'salt_auth': HASHIDS_SALT.get('auth_id'),
    'allowed_hosts': ALLOWED_HOSTS,
    'admin_enabled': ADMIN_ENABLED,
    'is_debug': DEBUG,
    'allowed_origins': ALLOWED_ORIGINS,
    'csrf_trusted': CSRF_TRUSTED,
    'jwt_expired': JWT_EXPIRED
}