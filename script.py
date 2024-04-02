import os
import subprocess
from dotenv import load_dotenv
import py7zr
import json


# Load .env file
load_dotenv()

# Get Bitwarden credentials
BW_USERNAME = os.getenv('BW_USERNAME')
BW_PASSWORD = os.getenv('BW_PASSWORD')

# Get 7z archive password
ARCHIVE_PASSWORD = os.getenv('ARCHIVE_PASSWORD').strip()

os.environ['HISTCONTROL'] = 'ignorespace'

# Command to get Bitwarden status
status_command = ' bw status'
status = json.loads(subprocess.getoutput(status_command))

# If we are not logged to Bitwarden (not even locked)
if status["status"] == "unauthenticated":
    # We need to login
    print("Logging in to Bitwarden...")
    login_command = f' bw login {BW_USERNAME} {BW_PASSWORD}'
    process = subprocess.check_output(login_command, shell=True)
else:
    print("Already logged in to Bitwarden, unlocking the session...")
    # If we are logged in but the vault is locked
    if status["status"] == "locked":
    	# We need to unlock it
        unlock_command = f' bw unlock {BW_PASSWORD} --raw'
        session_key = subprocess.getoutput(unlock_command).strip()
        session_key = session_key.split("\n")[-1] # Get last line (the session key)
        os.environ['BW_SESSION'] = session_key

# Sync Bitwarden Vault
print("Syncing your secrets with the local state...")
sync_command = ' bw sync'
process = subprocess.check_output(sync_command, shell=True)

# Export Vault to CSV
print("Exporting all credentials to a CSV file...")
CREDENTIALS_FILE_NAME = 'output.csv'
export_command = f' bw export --output {CREDENTIALS_FILE_NAME} --format csv {BW_PASSWORD}'
process = subprocess.check_output(export_command, shell=True)

# Create 7z password-protected archive
from datetime import datetime

if not os.path.exists('backups'):
	os.mkdir('backups')

current_date = datetime.now().strftime('%Y_%m_%d')
archive_filename = f'backups/bw_{current_date}.7z'
with py7zr.SevenZipFile(archive_filename, mode='w', password=ARCHIVE_PASSWORD) as archive:
    archive.write(f'./{CREDENTIALS_FILE_NAME}', 'base.csv')

os.remove(CREDENTIALS_FILE_NAME) # Removing CSV file after it is archived
