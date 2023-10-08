import os
from dotenv import load_dotenv

# Load environment variables from .env and .env.local files
load_dotenv('.env', '.env.local')

FRONTENED_PATH = 'frontend'
FRONTENED_DEPENDENCIES = 'frontend/node_modules'
STATIC_FILES_PATH = 'static'

MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
HASH_SALT_LENGTH = int(os.getenv('HASH_SALT_LENGTH'))
PORT = int(os.getenv('PORT', 3000))

# Check if MONGODB_URI is defined
if not MONGODB_URI:
    print('ERROR: \'MONGODB_URI\' environment variable is not defined.')
    print('  Please define it in your \'.env.local\' file.')
    exit(1)

# Check if DATABASE_NAME is defined
if not DATABASE_NAME:
    print('ERROR: \'DATABASE_NAME\' environment variable is not defined.')
    print('  Please define it in your \'.env.local\' file.')
    exit(1)

# Check if HASH_SALT_LENGTH is defined
if not HASH_SALT_LENGTH:
    print('ERROR: \'HASH_SALT_LENGTH\' environment variable is not defined.')
    print('  Please define it in your \'.env.local\' file.')
    exit(1)
