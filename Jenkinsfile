pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHONPATH = "${env.WORKSPACE}"   // Add project root to PYTHONPATH
        SONAR_HOST_URL = "http://host.docker.internal:9000"
        SONAR_AUTH_TOKEN = credentials('sqa_f51df2dd77d533dd8679938696aed6a46d3c5a60')
    }

    stages {
        stage('Setup') {
            steps {
                powershell """
                    # Create virtual environment if not exists
                    if (!(Test-Path $env:VENV_DIR)) { python -m venv $env:VENV_DIR }

                    # Activate virtual environment
                    .\\$env:VENV_DIR\\Scripts\\Activate.ps1

                    # Upgrade pip
                    python -m pip install --upgrade pip

                    # Install dependencies
                    pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                powershell """
                    # Activate virtual environment
                    .\\$env:VENV_DIR\\Scripts\\Activate.ps1

                    # Set PYTHONPATH
                    $env:PYTHONPATH = "$env:WORKSPACE"

                    # Run pytest with coverage
                    pytest --cov=app --cov-report=xml --junitxml=pytest-results.xml
                """
            }
            post {
                always {
                    junit 'pytest-results.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')]
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                powershell """
                    # Activate virtual environment
                    .\\$env:VENV_DIR\\Scripts\\Activate.ps1

                    # Run SonarQube Scanner
                    sonar-scanner -Dsonar.projectKey=my-fastapi \
                                  -Dsonar.sources=. \
                                  -Dsonar.host.url=$env:SONAR_HOST_URL \
                                  -Dsonar.login=$env:SONAR_AUTH_TOKEN \
                                  -Dsonar.python.coverage.reportPaths=coverage.xml
                """
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploy stage here (optional)"
                // Add your deployment commands, e.g., Docker build/run or copy files
            }
        }
    }
}
