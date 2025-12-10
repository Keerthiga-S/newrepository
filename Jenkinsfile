pipeline {
    agent {
        docker { image 'python:3.11-slim' }  // Python pre-installed
    }

    environment {
        SONAR_AUTH_TOKEN = credentials('sonar-token')  // Jenkins secret-text ID
        SONAR_SERVER_NAME = 'MySonar'
        SONAR_SCANNER_TOOL = 'MyScanner'

        SONAR_PROJECT_KEY = 'my-fastapi-project'
        SONAR_PROJECT_NAME = 'my-fastapi-project'
        SONAR_HOST_URL = 'http://sonarqube:9000'  // Use container name for Docker networking
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --cov=app --cov-report xml:coverage.xml --junitxml=pytest-results.xml || true
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONAR_SERVER_NAME}") {
                    sh """
                        ${tool SONAR_SCANNER_TOOL}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.projectName=${SONAR_PROJECT_NAME} \
                            -Dsonar.sources=app \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN} \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'coverage.xml, pytest-results.xml', allowEmptyArchive: true
            junit testResults: 'pytest-results.xml', allowEmptyResults: true
        }
        success {
            echo "Build succeeded"
        }
        failure {
            echo "Build failed"
        }
    }
}
