pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'                       // Python virtual environment folder
        SONARQUBE = 'MySonar'                   // Jenkins SonarQube server name
        SCANNER = 'MyScanner'                   // Jenkins SonarQube scanner tool name
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Keerthiga-S/newrepository.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Create virtual environment
                    bat "python -m venv ${VENV_DIR}"
                    // Activate and upgrade pip
                    bat """
                        ${VENV_DIR}\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                    """
                    // Install dependencies
                    bat """
                        ${VENV_DIR}\\Scripts\\activate.bat
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run pytest and generate reports
                    bat """
                        ${VENV_DIR}\\Scripts\\activate.bat
                        pytest --junitxml=pytest-results.xml --cov=app --cov-report xml:coverage.xml
                    """
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool name: "${SCANNER}", type: 'hudson.plugins.sonar.SonarRunnerInstallation'

                    withSonarQubeEnv("${SONARQUBE}") {
                        bat """
                            ${scannerHome}\\bin\\sonar-scanner.bat ^
                            -Dsonar.projectKey=my-fastapi ^
                            -Dsonar.sources=. ^
                            -Dsonar.host.url=%SONAR_HOST_URL% ^
                            -Dsonar.login=%SONAR_AUTH_TOKEN%
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying application..."
                // Add your deployment commands here
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            deleteDir() // No node {} needed here
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs!"
        }
    }
}
