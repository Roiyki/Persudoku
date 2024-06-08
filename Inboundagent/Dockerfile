# FROM python:3.9

# WORKDIR /app

# # Install git and pytest as root
# USER root
# RUN apt-get update && \
#     apt-get install -y git openssh-client python3-pip && \
#     pip install pytest

# # Switch back to the default user (usually non-root)
# USER <original_user>

# # Copy your application code
# COPY . .

FROM roiyki/inbound-agent

# Install sudo package
RUN apt-get update && apt-get install -y sudo

# Add jenkins user to sudoers file
RUN echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers