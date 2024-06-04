FROM python:3.9

WORKDIR /app

# Copy your application code
COPY . .

# Install git and pytest
RUN apt-get update && apt-get install -y git openssh-client python3-pip
RUN pip install pytest

# Environment variables for security (replace with actual setup)
ENV GIT_USERNAME=$GIT_USERNAME
ENV GIT_PAT=$GIT_PAT

# Function to clone a branch (replace with your logic)
COPY clone_branch.sh clone_branch.sh
RUN chmod +x clone_branch.sh