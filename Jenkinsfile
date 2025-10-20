pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'Deekshu_209'
        IMAGE_NAME = 'motivation-tracker'
        KUBECONFIG_CRED = credentials('kubeconfig-cred')
        DOCKERHUB_CRED = credentials('dockerhub-cred')
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                bat "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                bat """
                echo %DOCKERHUB_CRED_PSW% | docker login -u %DOCKERHUB_CRED_USR% --password-stdin
                docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG_FILE')]) {
                    bat """
                    set KUBECONFIG=%KUBECONFIG_FILE%
                    powershell -Command "(Get-Content k8s\\deployment.yaml) -replace '<dockerhub_user>', '${DOCKERHUB_USER}' | Set-Content k8s\\deployment.yaml"
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}
