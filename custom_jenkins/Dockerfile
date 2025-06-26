# Use a Jenkins image as base image
FROM jenkins/jenkins:lts

# Install Docker
USER root
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Configure Docker to run as a non-root user
# Create docker group and add jenkins user to it
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Enable Docker-in-Docker (DinD)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker
