FROM docker:20.10.10-alpine3.14

# Install Docker and Git
RUN apk add --no-cache docker git

# Create a directory for Docker's runtime files
RUN mkdir -p /var/run/docker

# Optional: Set the PATH if needed
ENV PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Ensure Docker daemon starts
CMD ["dockerd"]

# Set permissions for /var/run/docker.sock
RUN chmod 777 /var/run/docker.sock