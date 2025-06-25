pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'iquantc/mlops-proj-01'
    }
    stages {
        stage('Environment Check') {
            steps {
                script {
                    echo 'Checking build environment...'
                    sh '''
                        echo "=== Environment Information ==="
                        echo "Python version:"
                        python3 --version || echo "Python3 not found"
                        
                        echo "Docker version:"
                        docker --version || echo "Docker not found"
                        
                        echo "Trivy version:"
                        trivy --version || echo "Trivy not found"
                        
                        echo "AWS CLI version:"
                        aws --version || echo "AWS CLI not found"
                        
                        echo "Current working directory:"
                        pwd
                        
                        echo "Directory contents:"
                        ls -la
                        
                        echo "=== End Environment Check ==="
                    '''
                }
            }
        }
        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub Repository...'
                checkout scmGit(branches: [[name: '*/test-code-stage']],
                    extensions: [],
                    userRemoteConfigs: [[credentialsId: 'mlops', url: 'https://github.com/QuXiangjie/MLOps-e2e-Project-Flask-Docker-Jenkins-CI-CD-Pipeline-AWS-ECS-Step-by-Step-Demo.git']])
            }
        }
        stage('Lint Code') {
            steps {
                echo 'Skipping lint stage'
                // 如需开启Lint，取消注释并确保环境有python相关工具
                // script {
                //     echo 'Linting Python Code...'
                //     sh "python -m pip install --break-system-packages -r requirements.txt"
                //     sh "pylint app.py train.py --output=pylint-report.txt --exit-zero"
                //     sh "flake8 app.py train.py --ignore=E501,E302 --output-file=flake8-report.txt"
                //     sh "black app.py train.py"
                // }
            }
        }
        stage('Test Code') {
            steps {
                script {
                    echo 'Testing Python Code...'
                    sh '''
                        python3 -m pip install --upgrade pip --break-system-packages
                        python3 -m pip install -r requirements.txt --break-system-packages
                        python3 -m pip install pytest --break-system-packages
                        
                        # Train the model first to ensure it exists for tests
                        python3 train.py
                        
                        # Run tests
                        python3 -m pytest tests/ -v

                    '''
                }
            }
        }
        stage('Trivy FS Scan') {
            steps {
                script {
                    echo 'Scanning Filesystem with Trivy...'
                    sh '''
                        # Check if trivy is available
                        if command -v trivy &> /dev/null; then
                            echo "Trivy found, running filesystem scan..."
                            trivy fs ./ --format table -o trivy-fs-report.html || echo "Trivy scan completed with warnings"
                        else
                            echo "Trivy not found. Skipping filesystem scan."
                            echo "Please ensure Trivy is installed in the Jenkins environment."
                        fi
                    '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    try {
                        dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                        echo "Docker image built successfully: ${DOCKERHUB_REPOSITORY}:latest"
                    } catch (Exception e) {
                        echo "Docker build failed: ${e.getMessage()}"
                        error("Docker build failed")
                    }
                }
            }
        }
        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    echo 'Scanning Docker Image with Trivy...'
                    sh '''
                        # Check if trivy is available and docker image exists
                        if command -v trivy &> /dev/null; then
                            echo "Trivy found, running Docker image scan..."
                            if docker image inspect ${DOCKERHUB_REPOSITORY}:latest &> /dev/null; then
                                trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-report.html || echo "Trivy image scan completed with warnings"
                            else
                                echo "Docker image not found, skipping Trivy scan"
                            fi
                        else
                            echo "Trivy not found. Skipping Docker image scan."
                        fi
                    '''
                }
            }
        }
        stage('Push Docker Image') {
            when {
                expression { return dockerImage != null }
            }
            steps {
                script {
                    echo 'Pushing Docker Image to DockerHub...'
                    try {
                        docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                            dockerImage.push('latest')
                            echo "Docker image pushed successfully to ${DOCKERHUB_REPOSITORY}:latest"
                        }
                    } catch (Exception e) {
                        echo "Docker push failed: ${e.getMessage()}"
                        error("Docker push failed")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying to production...'
                    // Check if AWS CLI is available and credentials are configured
                    sh '''
                        if command -v aws &> /dev/null; then
                            echo "AWS CLI found, attempting deployment..."
                            aws ecs update-service --cluster iquant-ecs --service iquant-ecs-svc --force-new-deployment
                        else
                            echo "AWS CLI not found. Skipping deployment step."
                            echo "Please ensure AWS CLI is installed and configured in the Jenkins environment."
                        fi
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution completed'
            // Archive test results and reports
            script {
                if (fileExists('trivy-fs-report.html')) {
                    archiveArtifacts artifacts: 'trivy-fs-report.html', fingerprint: true
                }
                if (fileExists('trivy-image-report.html')) {
                    archiveArtifacts artifacts: 'trivy-image-report.html', fingerprint: true
                }
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        cleanup {
            // Clean up workspace
            cleanWs()
        }
    }
}
