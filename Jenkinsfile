pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        IMAGE = "fortune-teller:${BUILD_NUMBER}"
        KUBECTL = 'kubectl --context docker-desktop --server https://host.docker.internal:6443 --tls-server-name kubernetes.docker.internal'
    }

    stages {
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t ${IMAGE} -t fortune-teller:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    $KUBECTL apply -f k8s/service.yaml
                    # Deploy this build's image instead of :latest so every build triggers a rollout
                    sed "s|image: fortune-teller:latest|image: ${IMAGE}|" k8s/deployment.yaml \
                        | $KUBECTL apply -f -
                    $KUBECTL rollout status deployment/fortune-teller --timeout=180s
                '''
            }
        }
    }
}