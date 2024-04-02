# bitwarden-sync-archive

A tool to sync and archive bitwarden passwords and secrets. The created archive comes with a password, if configured.

# Installation

Just run `bash setup.sh` in the Terminal, it will do all installation for you. Note that the current script works only for Linux/MacOS, for Windows BitWarden installation might differ (feel free to contribute).

After installation, you need to fill in your BitWarden login/password in the `.env` file, as well as the archive password that you'd like to have. You credentials are stored only locally and won't appear in bash history.

# Execution

To run the script, just type `python3 script.py`. It will log in to Bitwarden, export all your secrets from there, and create an archive with a password automatically.
