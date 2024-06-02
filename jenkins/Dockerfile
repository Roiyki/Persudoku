# Use the official Jenkins image with a specific version and JDK
FROM jenkins/jenkins:2.452.1-jdk17

# Switch to root user to install dependencies
USER root

# Update package list and install lsb-release
RUN apt-get update && apt-get install -y lsb-release

# Add Docker's official GPG key
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg

# Add Docker's official APT repository
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

# Update package list again and install Docker CLI
RUN apt-get update && apt-get install -y docker-ce-cli

# Switch back to the Jenkins user
USER jenkins

# Install Jenkins plugins for Blue Ocean and Docker workflow
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
