pipeline {
    agent any

    environment {
        SONAR_AUTH_TOKEN = credentials('sonar-token') // Jenkins secret-text id
        SONAR_SERVER_NAME = 'MySonar'
        SONAR_SCANNER_TOOL = 'MyScanner'

        SONAR_PROJECT_KEY = 'my-fastapi-project'
        SONAR_PROJECT_NAME = 'my-fastapi-project'
        SONAR_HOST_URL = 'http://localhost:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    // Activate virtual environment and install dependencies
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            pytest --cov=app --cov-report xml:coverage.xml --junitxml=pytest-results.xml || true
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate
                            pytest --cov=app --cov-report xml:coverage.xml --junitxml=pytest-results.xml || exit /b 0
                        '''
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv("${SONAR_SERVER_NAME}") {
                        if (isUnix()) {
                            sh """
                                ${tool SONAR_SCANNER_TOOL}/bin/sonar-scanner \
                                    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                    -Dsonar.projectName=${SONAR_PROJECT_NAME} \
                                    -Dsonar.sources=app \
                                    -Dsonar.host.url=${SONAR_HOST_URL} \
                                    -Dsonar.login=${SONAR_AUTH_TOKEN} \
                                    -Dsonar.python.coverage.reportPaths=coverage.xml
                            """
                        } else {
                            bat """
                                "%SONAR_SCANNER_HOME%\\bin\\sonar-scanner.bat" ^ 
                                    -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^ 
                                    -Dsonar.projectName=%SONAR_PROJECT_NAME% ^ 
                                    -Dsonar.sources=app ^ 
                                    -Dsonar.host.url=%SONAR_HOST_URL% ^ 
                                    -Dsonar.login=%SONAR_AUTH_TOKEN% ^ 
                                    -Dsonar.python.coverage.reportPaths=coverage.xml
                            """
                        }
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
