import shutil
import subprocess
import os
from datetime import datetime, timedelta

# Function to backup PostgreSQL database
def backup_postgres():
    try:
        # Set PostgreSQL connection parameters from settings
        username = 'postgres'
        dbname = 'social_network'
        password = 'postgres'
        backup_dir = 'D:\\bk_pg\\dump'
        port = '5001'

        # Ensure backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Generate timestamp for backup file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(backup_dir, f'postgres_backup_{timestamp}.sql')

        # Set PGPASSWORD environment variable for password authentication
        os.environ['PGPASSWORD'] = password

        # Execute pg_dump command to backup PostgreSQL database
        pg_dump_cmd = ['pg_dump', '-U', username, '-d', dbname, '-f', backup_file, '-p', port]
        subprocess.run(pg_dump_cmd, check=True)

        # Delete old backup files older than 4 weeks
        delete_old_backups(backup_dir, days_to_keep=9)

        print("PostgreSQL backup successful.")

    except subprocess.CalledProcessError as e:
        print("Error occurred during PostgreSQL backup:", e)

# Function to backup MongoDB database
def backup_mongodb():
    try:
        # Set MongoDB connection parameters from settings
        db_name = 'social_network'
        host = 'mongo-0-a,mongo-0-b,mongo-0-c'
        backup_dir = 'D:\\bk_mongo\\dump'

        # Ensure backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Generate timestamp for backup folder
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = os.path.join(backup_dir, f'mongo_backup_{timestamp}')

        # Execute mongodump command to backup MongoDB database
        mongodump_cmd = ['mongodump', '--db', db_name, '--host', f'{host}', '--out', backup_file]
        subprocess.run(mongodump_cmd, check=True)

        # Delete old backup folders older than 4 weeks
        delete_old_backups(backup_dir, days_to_keep=9)

        print("MongoDB backup successful.")

    except subprocess.CalledProcessError as e:
        print("Error occurred during MongoDB backup:", e)

# Function to delete old backup files/folders
def delete_old_backups(backup_dir, days_to_keep):
    now = datetime.now()
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.isfile(item_path):
            file_time = datetime.fromtimestamp(os.path.getctime(item_path))
        else:
            file_time = datetime.fromtimestamp(os.path.getctime(os.path.join(item_path, os.listdir(item_path)[0])))

        if (now - file_time).days > days_to_keep:
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)

# Run PostgreSQL backup
backup_postgres()

# Run MongoDB backup
backup_mongodb()
