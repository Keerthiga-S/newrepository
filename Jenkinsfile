// pipeline {
//     agent any

//     environment {
//         SONAR_HOST_URL = 'http://localhost:9000'
//         SONAR_PROJECT_KEY = 'my-fastapi-project'
//         SONAR_PROJECT_NAME = 'my-fastapi-project'
//         SONAR_SCANNER_TOOL = 'MyScanner'
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Setup Python') {
//             steps {
//                 script {
//                     if (isUnix()) {
//                         sh '''
//                             python3 -m venv venv
//                             . venv/bin/activate
//                             pip install --upgrade pip
//                             pip install -r requirements.txt
//                         '''
//                     } else {
//                         bat '''
//                             python -m venv venv
//                             call venv\\Scripts\\activate
//                             python -m pip install --upgrade pip
//                             pip install -r requirements.txt
//                         '''
//                     }
//                 }
//             }
//         }

//         stage('Run Tests') {
//             steps {
//                 script {
//                     if (isUnix()) {
//                         sh '''
//                             . venv/bin/activate
//                             pytest --cov=app --cov-report xml:coverage.xml --junitxml=pytest-results.xml || true
//                         '''
//                     } else {
//                         bat '''
//                             call venv\\Scripts\\activate
//                             pytest --cov=app --cov-report xml:coverage.xml --junitxml=pytest-results.xml || exit /b 0
//                         '''
//                     }
//                 }
//             }
//         }

//         stage('SonarQube Analysis') {
//             steps {
//                 withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_AUTH_TOKEN')]) {
//                     withSonarQubeEnv('MySonar') {
//                         script {
//                             if (isUnix()) {
//                                 sh """
//                                 ${tool SONAR_SCANNER_TOOL}/bin/sonar-scanner \
//                                     -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
//                                     -Dsonar.projectName=${SONAR_PROJECT_NAME} \
//                                     -Dsonar.sources=app \
//                                     -Dsonar.host.url=${SONAR_HOST_URL} \
//                                     -Dsonar.login=${SONAR_AUTH_TOKEN} \
//                                     -Dsonar.python.coverage.reportPaths=coverage.xml
//                                 """
//                             } else {
//                                 bat """
//                                 "%SONAR_SCANNER_HOME%\\bin\\sonar-scanner.bat" ^
//                                     -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^
//                                     -Dsonar.projectName=%SONAR_PROJECT_NAME% ^
//                                     -Dsonar.sources=app ^
//                                     -Dsonar.host.url=%SONAR_HOST_URL% ^
//                                     -Dsonar.login=%SONAR_AUTH_TOKEN% ^
//                                     -Dsonar.python.coverage.reportPaths=coverage.xml
//                                 """
//                             }
//                         }
//                     }
//                 }
//             }
//         }

//         stage('Quality Gate') {
//             steps {
//                 timeout(time: 5, unit: 'MINUTES') {
//                     waitForQualityGate abortPipeline: true
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             archiveArtifacts artifacts: 'coverage.xml, pytest-results.xml', allowEmptyArchive: true
//             junit testResults: 'pytest-results.xml', allowEmptyResults: true
//         }
//         success {
//             echo "Build succeeded"
//         }
//         failure {
//             echo "Build failed"
//         }
//     }
// }


pipeline {
    agent any

    stages {
        stage('SonarQube Analysis') {
            steps {
                // Inject the token into the environment variable
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_AUTH_TOKEN')]) {
                    // Use the SonarQube server configured in Jenkins (MySonar)
                    withSonarQubeEnv('MySonar') {
                        // Run the SonarScanner
                        sh """
                            ${tool 'MyScanner'}/bin/sonar-scanner \
                                -Dsonar.projectKey=my-fastapi-project \
                                -Dsonar.projectName=my-fastapi-project \
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
