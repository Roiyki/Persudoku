#!/bin/bash

# Get branch name from environment variable (optional, adjust if needed)
BRANCH_NAME=${BRANCH_NAME:-"feature"}

# Get username and personal access token from environment variables
USERNAME=${GIT_USERNAME}
PAT=${GIT_PAT}

# Function to handle errors
error_handler() {
  echo "Error: $1"
  exit 1
}

# Validate required environment variables
if [[ -z "$USERNAME" || -z "$PAT" ]]; then
  error_handler "Missing environment variables: GIT_USERNAME or GIT_PAT"
fi

# URL-encode function for username to handle special characters
urlencode() {
    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf "$c" ;;
            *) printf '%%%02X' "'$c" ;;
        esac
    done
}

# URL-encode the username
ENCODED_USERNAME=$(urlencode "$USERNAME")

# Create a temporary directory for cloning
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Construct the clone URL with username and personal access token
CLONE_URL="https://$ENCODED_USERNAME:$PAT@github.com/Roiyki/Persudoku.git"

# Clone the branch using git clone
git clone -b $BRANCH_NAME $CLONE_URL $TEMP_DIR || error_handler "Failed to clone branch"

# Move to the cloned directory (adjust if needed)
cd $TEMP_DIR

# Additional commands (optional)
#  - You can perform other actions here, like running tests or building the project

echo "Branch $BRANCH_NAME cloned successfully."
