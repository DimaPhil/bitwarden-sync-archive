#!/bin/bash

# Make sure python3 and pip are installed
command -v python3 > /dev/null 2>&1 || { echo >&2 "Python 3 is required but it's not installed.  Aborting."; exit 1; }
command -v pip3 > /dev/null 2>&1 || { echo >&2 "pip for Python 3 is required but it's not installed.  Aborting."; exit 1; }

# If a platform is not provided, use 'macos' as default, else sanitize the provided platform argument
platform=${1:-macos}

bash ./install_bitwarden.sh $platform

pip3 install -r requirements.txt

cp .env.example .env

echo "Now open the .env file and replace placeholders with actual values"
