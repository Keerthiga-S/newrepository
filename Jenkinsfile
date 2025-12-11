pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonar') {
                    sh """
                        ${tool 'MyScanner'}/bin/sonar-scanner \
                        -Dsonar.projectKey=my-fastapi \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://host.docker.internal:9000 \
                        -Dsonar.login=${SONARQUBE_AUTH_TOKEN}
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
