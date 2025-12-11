pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        SONAR_HOST_URL = "http://host.docker.internal:9000"
        SONAR_AUTH_TOKEN = credentials('sqa_f51df2dd77d533dd8679938696aed6a46d3c5a60')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
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
                    if (!fileExists(env.VENV_DIR)) {
                        if (isUnix()) {
                            sh "python3 -m venv ${env.VENV_DIR}"
                        } else {
                            bat "python -m venv ${env.VENV_DIR}"
                        }
                    }

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
                script {
                    def scannerHome = tool name: 'MyScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'

                    withSonarQubeEnv('MySonar') {
                        if (isUnix()) {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=my-fastapi \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.login=${SONAR_AUTH_TOKEN} \
                                -Dsonar.python.coverage.reportPaths=coverage.xml
                            """
                        } else {
                            bat """
                                ${scannerHome}\\bin\\sonar-scanner ^
                                -Dsonar.projectKey=my-fastapi ^
                                -Dsonar.sources=. ^
                                -Dsonar.host.url=${SONAR_HOST_URL} ^
                                -Dsonar.login=${SONAR_AUTH_TOKEN} ^
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
            }
        }
    }

    post {
        always {
            node {
                echo "Cleaning workspace..."
                deleteDir()
            }
        }
        success {
            echo "Build, test, and SonarQube analysis completed successfully!"
        }
        failure {
            echo "Build or test failed. Check logs!"
        }
    }
}
