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
    apt-get install -y python3-pip && \
    apt-get install -y docker.io python3 && \
    ln -sf /usr/bin/python3 /usr/bin/python
# Install trivy for vulnerability scanning
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.41.0
# curl, unzip, sudo
RUN apt-get install -y curl unzip sudo
# add Amazon CLI repository
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Configure Docker to run as a non-root user
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Enable Docker-in-Docker (DinD)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker


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
