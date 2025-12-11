pipeline {
    agent any

    environment {
        VENV = "venv"
        SONAR_SCANNER = tool name: 'MyScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Create venv
                    sh "python3 -m venv ${VENV}"

                    // Activate and install pip upgrade
                    sh """
                        . ${VENV}/bin/activate
                        pip install --upgrade pip
                    """

                    // Install dependencies
                    sh """
                        . ${VENV}/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh """
                        . ${VENV}/bin/activate
                        pytest --junitxml=pytest-report.xml
                    """
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('MySonar') {
                        sh """
                            ${SONAR_SCANNER}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-fastapi \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    echo "Deploying Application..."
                """
            }
        }
    }

    post {
        always {
            echo "Cleanup workspace..."
            deleteDir()
        }
    }
}
