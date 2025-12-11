pipeline {
    agent any

    environment {
        SONARQUBE = 'MySonar' // Jenkins SonarQube server
        SCANNER = 'MyScanner' // Jenkins-installed scanner
    }

    stages {
        stage('Build') {
            steps {
                echo "Installing dependencies..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "Running tests and generating coverage..."
                sh 'pytest --junitxml=report.xml --cov=. --cov-report=xml:coverage.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool name: "${SCANNER}", type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    withSonarQubeEnv("${SONARQUBE}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-fastapi \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
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

        stage('Deploy') {
            steps {
                echo "Deploying application..."
                sh 'docker build -t my-fastapi:latest .'
                sh 'docker run -d -p 8000:8000 my-fastapi:latest'
            }
        }
    }
}
