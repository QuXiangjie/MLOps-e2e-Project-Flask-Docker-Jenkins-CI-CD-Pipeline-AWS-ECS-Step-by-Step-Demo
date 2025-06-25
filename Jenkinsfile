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
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }
        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    echo 'Scanning Docker Image with Trivy...'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-report.html"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image to DockerHub...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
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
}
