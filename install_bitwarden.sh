#!/bin/bash

# If platform is not provided, by default use 'macos', else sanitize the provided platform argument
platform=${1:-macos}

# Convert platform to lowercase
platform=$(echo "$platform" | tr '[:upper:]' '[:lower:]')

# Form the complete download URL
url="https://vault.bitwarden.com/download/?app=cli&platform=${platform}"

echo "Downloading and installing Bitwarden CLI"
# Download the Bitwarden CLI tool
curl -s -L "${url}" -o bw.zip

# Extract the files from the downloaded zip
unzip bw.zip

# Grant executable permissions to the Bitwarden 'bw' file
chmod +x bw

# Move the Bitwarden 'bw' file to /usr/local/bin
sudo mv bw /usr/local/bin

# Handle the security warning about the unverified developer
# We need admin privileges for this
sudo spctl --add /usr/local/bin/bw

# Cleanup the remaining zip file
rm -f bw.zip

echo "Bitwarden CLI tool has been successfully installed on ${platform}."
