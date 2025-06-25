# Use a Jenkins image as base image for long term support (LTS)
# This Dockerfile sets up a Jenkins instance with Docker installed
FROM jenkins/jenkins:lts

# Install Docker
USER root

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    ca-certificates \
    libssl-dev \
    && apt-get clean
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
# Install Trivy for vulnerability scanning
# Trivy is a simple and comprehensive vulnerability scanner for containers and other artifacts.
RUN apt-get update && apt-get install -y wget apt-transport-https gnupg lsb-release \
 && wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor -o /usr/share/keyrings/trivy.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list \
 && apt-get update && apt-get install -y trivy \
 && rm -rf /var/lib/apt/lists/*



# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
 && apt-get update && apt-get install -y unzip \
 && unzip awscliv2.zip \
 && ./aws/install \
 && rm -rf awscliv2.zip aws \
 && rm -rf /var/lib/apt/lists/*

# Enable DinD
# In CI/CD pipelines, Docker in Docker (DinD) is often used to build and run Docker containers within a Jenkins job.
# When running DinD inside a container, you need a directory for Docker to store its data.
# Create the directory as root user before switching to jenkins user
RUN mkdir -p /var/lib/docker && \
    chown jenkins:jenkins /var/lib/docker && \
    ln -s /usr/bin/python3 /usr/bin/python

# Ensure jenkins user owns the jenkins home directory
RUN mkdir -p /var/jenkins_home && \
    chown jenkins:jenkins /var/jenkins_home

# Switch back to jenkins user
USER jenkins

# By marking /var/lib/docker as a volume, Docker stores its data outside the container’s writable layer.
# Also, this directory is often declared as a volume (VOLUME /var/lib/docker) so the data persists beyond the life of the container.
VOLUME /var/lib/docker

# Build and run instructions:
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
# docker run -d `
#   --name jenkins-dind `
#   -p 8080:8080 `
#   -p 50000:50000 `
#   --privileged `
#   -v /var/run/docker.sock:/var/run/docker.sock `
#   -v jenkins_home:/var/jenkins_home `
#   jenkins-dind



# docker ps
# Check if Docker container is running


# To check the initial admin password:
# docker exec jenkins-dind cat /var/jenkins_home/secrets/initialAdminPassword
