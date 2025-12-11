pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        SONAR_HOST_URL = "http://host.docker.internal:9000"
        SONAR_AUTH_TOKEN = credentials('sqa_f51df2dd77d533dd8679938696aed6a46d3c5a60')
    }

    options {
        // Automatically clean workspace after build
        cleanWs()
        // Keep only last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    // Create virtual environment
                    if (!fileExists(env.VENV_DIR)) {
                        sh "python -m venv ${env.VENV_DIR}"
                    }
                    // Activate virtual environment and install dependencies
                    if (isUnix()) {
                        sh """
                            source ${env.VENV_DIR}/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    } else {
                        bat """
                            ${env.VENV_DIR}\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                            source ${env.VENV_DIR}/bin/activate
                            pytest --junitxml=pytest-results.xml --cov=app --cov-report=xml:coverage.xml
                        """
                    } else {
                        bat """
                            ${env.VENV_DIR}\\Scripts\\activate.bat
                            pytest --junitxml=pytest-results.xml --cov=app --cov-report=xml:coverage.xml
                        """
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonar') {
                    script {
                        if (isUnix()) {
                            sh """
                                source ${env.VENV_DIR}/bin/activate
                                sonar-scanner \
                                    -Dsonar.projectKey=my-fastapi \
                                    -Dsonar.sources=. \
                                    -Dsonar.host.url=${env.SONAR_HOST_URL} \
                                    -Dsonar.login=${env.SONAR_AUTH_TOKEN} \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml
                            """
                        } else {
                            bat """
                                ${env.VENV_DIR}\\Scripts\\activate.bat
                                sonar-scanner ^
                                    -Dsonar.projectKey=my-fastapi ^
                                    -Dsonar.sources=. ^
                                    -Dsonar.host.url=${env.SONAR_HOST_URL} ^
                                    -Dsonar.login=${env.SONAR_AUTH_TOKEN} ^
                                    -Dsonar.python.coverage.reportPaths=coverage.xml
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deployment steps go here..."
                // Example: sh 'docker build -t myapp . && docker run -d -p 8000:8000 myapp'
            }
        }
    }

    post {
        always {
            node {
                echo "Cleaning up workspace..."
                cleanWs()
            }
        }
        success {
            echo "Build, test, SonarQube analysis completed successfully!"
        }
        failure {
            echo "Build or test failed. Check logs!"
        }
    }
}
