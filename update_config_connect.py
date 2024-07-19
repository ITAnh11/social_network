import json
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get environment variables
aws_postgres_endpoint = os.getenv('AWS_POSTGRES_ENDPOINT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')

# Path to the JSON config file
config_file_path = 'postgres-connect.json'

# Read the JSON config file
with open(config_file_path, 'r') as file:
    config = json.load(file)

# Update the config with environment variables
config['config']['database.hostname'] = aws_postgres_endpoint
config['config']['database.user'] = postgres_user
config['config']['database.password'] = postgres_password
config['config']['database.dbname'] = postgres_db

# Write the updated config back to the JSON file
with open(config_file_path, 'w') as file:
    json.dump(config, file, indent=4)

print("Config file updated successfully.")