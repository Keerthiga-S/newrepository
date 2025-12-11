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
                sh """
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    pytest --junitxml=pytest-report.xml || true
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonar') {
                    sh """
                        ${SONAR_SCANNER}/bin/sonar-scanner \
                        -Dsonar.projectKey=my-fastapi \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=pytest-report.xml \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    """
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
            echo "Cleaning workspace..."
            deleteDir()
        }
    }
}
