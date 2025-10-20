pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'deekshu209'
        IMAGE_NAME = 'motivation-tracker'
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout SCM') {
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
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    bat "docker login -u deekshu209 -p Admins209"
                    bat "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    bat "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred, variable: 'KUBECONFIG')]) {
                    bat "kubectl apply -f k8s/deployment.yaml --kubeconfig=%KUBECONFIG%"
                }
            }
        }

    }

    post {
        success {
            echo "✅ Deployment Succeeded!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}








