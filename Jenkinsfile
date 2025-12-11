pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON = "${VENV_DIR}\\Scripts\\python.exe"
        PIP = "${VENV_DIR}\\Scripts\\pip.exe"
        SONAR_TOKEN = credentials('MySonarToken') // Replace with your Jenkins secret
        SONAR_HOST_URL = 'http://host.docker.internal:9000'
        PYTHONPATH = "${env.WORKSPACE}"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Keerthiga-S/newrepository.git'
            }
        }

        stage('Build & Install Dependencies') {
            steps {
                powershell """
                # Create virtual environment if not exists
                if (-not (Test-Path -Path '${VENV_DIR}')) {
                    python -m venv ${VENV_DIR}
                }

                # Activate virtual environment
                & ${VENV_DIR}\\Scripts\\Activate.ps1

                # Upgrade pip
                & ${PIP} install --upgrade pip

                # Install dependencies
                & ${PIP} install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                powershell """
                # Activate virtual environment
                & ${VENV_DIR}\\Scripts\\Activate.ps1

                # Set PYTHONPATH
                \$env:PYTHONPATH='${PYTHONPATH}'

                # Run pytest with coverage
                & ${PYTHON} -m pytest --cov=app --cov-report=xml --junitxml=pytest-results.xml
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                powershell """
                # Activate virtual environment
                & ${VENV_DIR}\\Scripts\\Activate.ps1

                # Run SonarScanner
                sonar-scanner -Dsonar.projectKey=my-fastapi `
                              -Dsonar.sources=. `
                              -Dsonar.host.url=${SONAR_HOST_URL} `
                              -Dsonar.login=${SONAR_TOKEN} `
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                """
            }
        }

        stage('Deploy') {
            steps {
                echo "Add deployment commands here"
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace"
            cleanWs()
        }
    }
}
