# Jenkins Docker Management Script for Windows PowerShell

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("build", "start", "stop", "restart", "logs", "password", "status")]
    [string]$Action
)

$CONTAINER_NAME = "jenkins-dind"
$IMAGE_NAME = "jenkins-dind"

switch ($Action) {
    "build" {
        Write-Host "Building Jenkins Docker image..." -ForegroundColor Green
        docker build -t $IMAGE_NAME .
    }
    
    "start" {
        Write-Host "Starting Jenkins container..." -ForegroundColor Green
        # Stop and remove existing container if it exists
        docker stop $CONTAINER_NAME 2>$null
        docker rm $CONTAINER_NAME 2>$null
        
        # Start new container
        docker run -d `
            --name $CONTAINER_NAME `
            -p 8080:8080 `
            -p 50000:50000 `
            --privileged `
            -v /var/run/docker.sock:/var/run/docker.sock `
            -v jenkins_home:/var/jenkins_home `
            $IMAGE_NAME
            
        Write-Host "Jenkins is starting up..." -ForegroundColor Yellow
        Write-Host "Access Jenkins at: http://localhost:8080" -ForegroundColor Cyan
        Write-Host "Use 'manage-jenkins.ps1 password' to get the initial admin password" -ForegroundColor Cyan
    }
    
    "stop" {
        Write-Host "Stopping Jenkins container..." -ForegroundColor Yellow
        docker stop $CONTAINER_NAME
    }
    
    "restart" {
        Write-Host "Restarting Jenkins container..." -ForegroundColor Yellow
        docker restart $CONTAINER_NAME
    }
    
    "logs" {
        Write-Host "Showing Jenkins logs..." -ForegroundColor Green
        docker logs $CONTAINER_NAME
    }
    
    "password" {
        Write-Host "Getting initial admin password..." -ForegroundColor Green
        try {
            $password = docker exec $CONTAINER_NAME cat /var/jenkins_home/secrets/initialAdminPassword
            Write-Host "Initial Admin Password: $password" -ForegroundColor Cyan
        }
        catch {
            Write-Host "Could not retrieve password. Make sure Jenkins container is running." -ForegroundColor Red
        }
    }
    
    "status" {
        Write-Host "Checking Jenkins container status..." -ForegroundColor Green
        docker ps -f name=$CONTAINER_NAME
    }
}

# Usage examples
Write-Host ""
Write-Host "Usage examples:" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 build     - Build the Jenkins image" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 start     - Start Jenkins container" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 stop      - Stop Jenkins container" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 restart   - Restart Jenkins container" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 logs      - Show Jenkins logs" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 password  - Get initial admin password" -ForegroundColor Gray
Write-Host "  .\manage-jenkins.ps1 status    - Check container status" -ForegroundColor Gray
