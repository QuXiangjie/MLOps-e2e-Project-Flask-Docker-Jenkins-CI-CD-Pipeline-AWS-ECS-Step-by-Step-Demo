# Use a Jenkins image as base image for long term support (LTS)
# This Dockerfile sets up a Jenkins instance with Docker installed
FROM jenkins/jenkins:lts

# Install Docker
USER root

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip pytest
# 安装 trivy awscli docker 等你需要的工具

# RUN apt-get update -y && \
#     apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
#     curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
#     add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
#     apt-get update -y && \
#     apt-get install -y docker-ce-cli docker-ce

# Install Docker CLI only (not the daemon), using modern GPG method
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    groupadd -f docker && \
    usermod -aG docker jenkins && \
    rm -rf /var/lib/apt/lists/*



# RUN usermod -aG docker jenkins
# Configure Docker to run as a non-root user

# Adding jenkins user to the docker group allows Jenkins to run Docker commands
# The docker group is a Linux user group that controls who can run Docker commands




# Enable DinD
# In CI/CD pipelines, Docker in Docker (DinD) is often used to build and run Docker containers within a Jenkins job.
# When running DinD insde a container, you need a directory for Docker to store its data.
RUN mkdir -p /var/lib/docker

# By marking /var/lib/docker as a volume, Docker stores its data outside the container’s writable layer.
# Also, this directory is often declared as a volume (VOLUME /var/lib/docker) so the data persists beyond the life of the container.
VOLUME /var/lib/docker

# docker build -t jenkins-dind .
# docker run -d \
#   --name jenkins-dind \
#   -p 8080:8080 \
#   -p 50000:50000 \
#   --privileged \
#   -v /var/run/docker.sock:/var/run/docker.sock \
#   -v jenkins_home:/var/jenkins_home \
#   jenkins-dind
#docker run -d --name jenkins-dind -p 8080:8080 -p 50000:50000 --privileged -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind



# docker ps
# Check if Docker container is running


# To check the initial admin password, you can run the following command:
# docker exec jenkins-dind cat /var/jenkins_home/secrets/initialAdminPassword

#docker exec -it jenkins-dind bash
#/# ls
#ln -s /usr/bin/python3 /usr/bin/python
