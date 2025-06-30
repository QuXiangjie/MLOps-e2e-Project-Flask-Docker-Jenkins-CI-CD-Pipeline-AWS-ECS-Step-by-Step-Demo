# Use a Jenkins image as base image
FROM jenkins/jenkins:lts

# Switch to root user for installation
USER root

# Install required system tools and dependencies
RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        python3 \
        python3-pip \
        python3-venv \
        docker.io \
        sudo \
        unzip && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Create a Python virtual environment (venv_Test) and install Python packages
RUN python3 -m venv /opt/venv_Test && \
    /opt/venv_Test/bin/pip install --upgrade pip && \
    /opt/venv_Test/bin/pip install pylint flake8 black

# Add the virtual environment to PATH
ENV PATH="/opt/venv_Test/bin:$PATH"

# Install Trivy for vulnerability scanning
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.41.0

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Configure Docker to run as a non-root user
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Enable Docker-in-Docker (DinD)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user
# USER jenkins


# docker build -t custom_jenkins:latest .
# docker run -d --name custom_jenkins -p 8080:8080 -p 50000:50000 --privileged -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
# docker exec -it custom_jenkins bash
# ls
# apt update -y

# So everytime I change the Dockerfile, I need to rebuild the image and run the container again
# docker build -t custom_jenkins:0.0.1 .
# docker run -d --name custom_jenkins -p 8080:8080 -p 50000:50000 --privileged -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home custom_jenkins:0.0.1

# How to get the initial admin password
# docker exec -it custom_jenkins cat /var/jenkins_home/secrets/initialAdminPassword


# For the plugin installation, you can use the following command:
# Download Docker and Docker Pipeline plugins
