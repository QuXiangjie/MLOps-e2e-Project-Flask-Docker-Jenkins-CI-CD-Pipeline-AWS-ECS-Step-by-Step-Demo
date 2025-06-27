# MLOps End-to-End Project: Flask + Docker + Jenkins + AWS ECS

A complete MLOps pipeline demonstrating machine learning model deployment using Flask, Docker containerization, Jenkins CI/CD, and AWS ECS orchestration.

## 🏗️ Project Architecture

This project implements a full MLOps workflow with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Developer     │    │   Jenkins       │    │   Production    │
│   Local Code    │───▶│   CI/CD         │───▶│   AWS ECS       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components:
- **Flask Application**: Iris flower classification ML model
- **Custom Jenkins Environment**: CI/CD orchestration with Docker, Trivy, AWS CLI
- **Docker Containerization**: Application and Jenkins environment containers
- **AWS ECS**: Production deployment and scaling

## 📁 Project Structure

```
MLOps-e2e-Project/
├── app.py                 # Flask web application
├── train.py               # ML model training script
├── Dockerfile             # Application container definition
├── Jenkinsfile            # CI/CD pipeline configuration
├── requirements.txt       # Python dependencies
├── .dockerignore         # Docker build exclusions
├── custom_jenkins/       # Jenkins environment setup
│   ├── Dockerfile        # Custom Jenkins container
│   └── manage-jenkins.ps1 # Jenkins management script
├── templates/
│   └── index.html        # Web interface
├── tests/
│   ├── __init__.py
│   └── test_model.py     # Unit tests
└── model/
    └── iris_model.pkl    # Trained ML model (generated)
```

## 🔄 CI/CD Pipeline Workflow

### Pipeline Stages:
1. **Clone Repository** → Pull latest code from GitHub
2. **Lint Code** → Code quality checks (pylint, flake8, black)
3. **Test Code** → Run unit tests with pytest
4. **Trivy FS Scan** → Security vulnerability scanning
5. **Build Docker Image** → Create application container
6. **Trivy Image Scan** → Container security scanning
7. **Push to DockerHub** → Publish container image
8. **Deploy to AWS ECS** → Update production service

### Architecture Flow:
```
┌─────────────────────────────────────────────────────────────────┐
│                    JENKINS CONTAINER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Docker CLI    │  │     Trivy       │  │    AWS CLI      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Python 3      │  │   Credentials   │  │  Build Tools    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                 APPLICATION CONTAINER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Flask App     │  │   ML Model      │  │  Dependencies   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Git
- PowerShell (Windows) or Bash (Linux/Mac)

### 1. Build Custom Jenkins Environment
```bash
cd custom_jenkins
docker build -t custom_jenkins:latest .
```

### 2. Run Jenkins Container
```bash
docker run -d \
  --name custom_jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  custom_jenkins:latest
```

### 3. Get Initial Admin Password
```bash
docker exec custom_jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 4. Configure Jenkins
1. Access Jenkins at `http://localhost:8080`
2. Install suggested plugins
3. Create admin user
4. Configure credentials:
   - GitHub token (`QuXiangjie`)
   - DockerHub token (`mlops-jenkins-dockerhub-token`)
   - AWS credentials (`mlops-awscred`)

### 5. Create Pipeline Job
1. New Item → Pipeline
2. Pipeline definition → Pipeline script from SCM
3. Repository URL: `https://github.com/QuXiangjie/MLOps-e2e-Project-Flask-Docker-Jenkins-CI-CD-Pipeline-AWS-ECS-Step-by-Step-Demo.git`
4. Branch: `*/sandbox` or `*/Version_6/16`

## 🛠️ Key Features

### Machine Learning
- **Model**: Random Forest Classifier for Iris dataset
- **Training**: Automated model training in pipeline
- **Inference**: REST API endpoint for predictions

### Security
- **Vulnerability Scanning**: Trivy for filesystem and container scanning
- **Credential Management**: Secure token storage in Jenkins
- **Code Quality**: Automated linting and formatting

### DevOps
- **Containerization**: Docker for consistent environments
- **CI/CD**: Automated testing, building, and deployment
- **Monitoring**: Pipeline stage tracking and reporting

## 🔧 Configuration Details

### Environment Variables (Jenkinsfile)
```groovy
environment {
    DOCKERHUB_CREDENTIAL_ID = 'mlops-jenkins-dockerhub-token'
    DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
    DOCKERHUB_REPOSITORY = 'jqupitsco/test-mlops-project'
}
```

### AWS ECS Configuration
```bash
aws ecs update-service \
  --cluster magnificent-parrot-4ikbfl \
  --service ECS-Task-Test-service-qtne3pdf \
  --force-new-deployment \
  --region us-east-2
```

## ❓ Architecture Q&A

### Q: Does Jenkinsfile rely on custom_jenkins Dockerfile?
**A: YES, absolutely!** The dependency chain:
```
custom_jenkins/Dockerfile → Jenkins Container → Runs Jenkinsfile → Uses Root Dockerfile
```

The Jenkinsfile requires:
- Docker CLI for `docker.build()`
- Trivy for security scanning
- AWS CLI for ECS deployment
- Python tools for linting and testing

### Q: Can the project run without including custom_jenkins in the DockerHub image?
**A: YES, and you SHOULD exclude it!** 

**Correct Architecture:**
- **DockerHub Image** = Application only (Flask app, ML model, dependencies)
- **Jenkins Environment** = Separate container with CI/CD tools and credentials

**Benefits:**
- ✅ Clean application image for production
- ✅ Security: CI/CD tools and credentials stay separate
- ✅ Performance: Smaller production images
- ✅ Separation of concerns: Build vs Runtime environments

## 🔒 Security Considerations

### Docker Hub Public Repository
⚠️ **Security Notice**: This project uses a public DockerHub repository. For production:
- Use private repositories for proprietary code
- Implement image signing and verification
- Regular vulnerability scanning
- Access control and monitoring

### Best Practices Implemented:
- Credentials stored securely in Jenkins
- Multi-stage security scanning (Trivy)
- Code quality gates (linting, testing)
- Immutable container images

## 📝 Development Workflow

1. **Local Development**
   ```bash
   python train.py          # Train model
   python app.py           # Run Flask app
   pytest tests/           # Run tests
   ```

2. **Commit & Push**
   ```bash
   git add .
   git commit -m "feature: description"
   git push origin branch-name
   ```

3. **Automated Pipeline**
   - Jenkins detects changes
   - Runs full CI/CD pipeline
   - Deploys to AWS ECS if successful

## 🚀 Production Deployment

The application is deployed on AWS ECS with:
- **Auto-scaling**: Based on CPU/memory utilization
- **Load Balancing**: Application Load Balancer for high availability
- **Health Checks**: Container health monitoring
- **Blue-Green Deployment**: Zero-downtime updates

Access the live application: [ECS Service URL]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is for educational purposes and demonstrates MLOps best practices.

---

**Built with** ❤️ **for learning MLOps, Docker, Jenkins, and AWS ECS integration**

Question: The dockerfile in custom_jenkins stores the environment of Jenkinsfile, it also stores AWS access Token, Github Token and DockerHub token, so the Jenkinsfile in the root can clone, build docker Image and push it to Dockerhub and update AWS ECS. First you need to verify the workflow I explain for this project, and tell me where I did wrong and where I did right. Then answer me question, the Jenkinsfile running has to reply on the local dockerfile in custom_jenkins? second question is that if I don't include custom_jenkins in build docker image to dockerhub, can this project run, becasue i think clone-push to dockerhub and AWS update are in jenkinsfile, if it relys on jenkins file to run the process, but jenkins file are running based on local Dockerfile?

Great questions! Let me analyze your project structure and workflow to clarify the architecture and dependencies.

## **Your Workflow Analysis:**

### **✅ What You Did Right:**

1. **Separation of Concerns**: 
   - Dockerfile → Jenkins environment setup
   - Root Dockerfile → Application containerization
   - Jenkinsfile → CI/CD pipeline definition

2. **Complete CI/CD Pipeline**: Your Jenkinsfile covers the full workflow:
   - Clone → Lint → Test → Scan → Build → Push → Deploy

3. **Security**: Storing credentials in Jenkins (not hardcoded)

4. **Tool Installation**: Custom Jenkins has Docker CLI, Trivy, AWS CLI, Python

### **❌ Areas That Need Attention:**

1. **Missing Jenkins Plugin Installation**: Your custom Jenkins needs Docker Pipeline plugin
2. **Credential Management**: Need to ensure all tokens are properly configured in Jenkins
3. **Branch Consistency**: Jenkinsfile references `sandbox` branch but you created `Version_6/16`

## **Answer to Your Key Questions:**

### **Question 1: Does Jenkinsfile rely on custom_jenkins Dockerfile?**

**YES, absolutely!** Here's the dependency chain:

```
custom_jenkins/Dockerfile → Jenkins Container → Runs Jenkinsfile → Uses Root Dockerfile
```

**Why:**
- Your Jenkinsfile uses `docker.build()` - this requires Docker CLI
- Your Jenkinsfile uses `trivy` commands - this requires Trivy installed  
- Your Jenkinsfile uses `aws ecs update-service` - this requires AWS CLI
- Your Jenkinsfile uses `python`, `pylint`, `pytest` - these need to be installed

**Without custom_jenkins**, your pipeline would fail because the Jenkins agent wouldn't have these tools.

### **Question 2: Can the project run without including custom_jenkins in the Docker image pushed to DockerHub?**

**YES, and you SHOULD exclude it!** Here's why:

**Current Setup (Correct):**
```
DockerHub Image = Application Only (from root Dockerfile)
├── Flask app
├── Python dependencies  
├── Trained model
└── Application code

Jenkins Environment = Custom Jenkins Container (separate)
├── Docker CLI
├── Trivy
├── AWS CLI
├── Python tools
└── Stored credentials
```

**This is the correct architecture because:**

✅ **Application image is clean** - only contains what's needed to run the app  
✅ **Jenkins tools stay in CI environment** - not shipped to production  
✅ **Security** - credentials stay in Jenkins, not in application image  
✅ **Performance** - smaller application image for faster deployments  

## **How It Actually Works:**

1. **Jenkins Container** (from Dockerfile):
   - Runs 24/7 with all CI/CD tools
   - Stores credentials securely
   - Executes the pipeline

2. **Pipeline Execution**:
   - Jenkins clones your code
   - Uses root Dockerfile to build application image
   - Pushes **only the application image** to DockerHub
   - Updates ECS to use the new application image

3. **Production**:
   - ECS pulls the clean application image from DockerHub
   - Runs only your Flask app (no CI/CD tools)

## **Recommendations:**

### **1. Fix Custom Jenkins Dockerfile:**
```dockerfile
# Add Docker Pipeline plugin installation
RUN jenkins-plugin-cli --plugins docker-workflow:latest
```

### **2. Verify .dockerignore:**
Make sure custom_jenkins is excluded from the application build:
```dockerignore
custom_jenkins/
Jenkinsfile
*.md
```

### **3. Branch Consistency:**
Update Jenkinsfile to match your current branch:
```groovy
checkout scmGit(branches: [[name: '*/Version_6/16']], 
```

Your architecture is fundamentally correct - you just need to ensure the custom Jenkins container has all required tools and plugins installed!