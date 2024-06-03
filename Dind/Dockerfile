# Use the official Docker-in-Docker image as a base
FROM docker:dind

# Set environment variables for Docker TLS
ENV DOCKER_TLS_CERTDIR=/certs

# Create the necessary directories
RUN mkdir -p /certs/client

# Set the volume for the certs and Jenkins data
VOLUME /certs/client
VOLUME /var/jenkins_home

# Expose Docker daemon port
EXPOSE 2376

# Start Docker daemon in the container
CMD ["dockerd-entrypoint.sh"]
