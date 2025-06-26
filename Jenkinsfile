pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'iquantc/mlops-proj-01'
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Clone Repository
                script {
                    checkout scmGit(branches: [[name: '*/sandbox']], 
                    extensions: [], 
                    userRemoteConfigs: [[credentialsId: 'QuXiangjie', url: 'https://github.com/QuXiangjie/MLOps-e2e-Project-Flask-Docker-Jenkins-CI-CD-Pipeline-AWS-ECS-Step-by-Step-Demo.git']])
                }
            }
        }
        stage('Lint Code') {
            steps {
                // Lint code
                script {
                    echo 'Linting Python Code...'
                    sh '''
                    python --version
                    python3 --version
                    python -m pip install --break-system-packages -r requirements.txt
                    pylint app.py train.py --output=pylint-report.txt --exit-zero
                    flake8 app.py train.py --ignore=E501,E302 --output-file=flake8-report.txt
                    black app.py train.py


                    '''
                }
            }
        }
        stage('Test Code') {
            steps {
                // Pytest code
                script {
                    echo 'Testing Python Code...'
                    
                }
            }
        }
        stage('Trivy FS Scan') {
            steps {
                // Trivy Filesystem Scan
                script {
                    echo 'Scannning Filesystem with Trivy...'
                   
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                // Build Docker Image
                script {
                    echo 'Building Docker Image...'
                    
                }
            }
        }
        stage('Trivy Docker Image Scan') {
            steps {
                // Trivy Docker Image Scan
                script {
                    echo 'Scanning Docker Image with Trivy...'
                   
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                // Push Docker Image to DockerHub
                script {
                    echo 'Pushing Docker Image to DockerHub...'
                    
                }
            }
        }
        stage('Deploy') {
            steps {
                // Deploy Image to Amazon ECS
                script {
                    echo 'Deploying to production...'
                     
                    }
                }
            }
        }
    }
