pipeline {
    agent any

    stages {
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Get the Jenkins-installed SonarQube Scanner path
                    def scannerHome = tool name: 'MyScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    
                    // Set SonarQube environment variables from the Jenkins SonarQube server
                    withSonarQubeEnv('MySonar') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-fastapi \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        """
                    }
                }
            }
        }
    }
}
