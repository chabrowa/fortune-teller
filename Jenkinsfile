pipeline {
    agent any

    triggers {
        pollSCM('H/60 * * * *')
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
                sh 'docker build -t fortune-teller:${BUILD_NUMBER} -t fortune-teller:latest .'
            }
        }
    }
}