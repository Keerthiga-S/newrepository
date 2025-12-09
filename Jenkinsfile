pipeline {
  agent any

  tools {
    sonar 'MyScanner'
  }

  triggers {
    pollSCM('H/5 * * * *')
  }

  environment {
    BUILD_ENV = "dev"
    SONAR_AUTH_TOKEN = credentials('sonar-token')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        echo 'Building...'
        sh '''
          echo "This is my first Jenkins build step"
          echo "Running build script..."
        '''
      }
    }

    stage('Test') {
      steps {
        echo 'Running tests (if any)...'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          withSonarQubeEnv('MySonar') {
            sh """
              sonar-scanner \
                -Dsonar.projectKey=myproject \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://10.10.121.240:9000 \
                -Dsonar.login=$SONAR_AUTH_TOKEN
            """
          }
        }
      }
    }

    stage('Quality Gate') {
      steps {
        script {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Archive') {
      steps {
        echo 'Archiving artifacts...'
        sh 'echo build-output > build-output.txt || true'
        archiveArtifacts artifacts: 'build-output.txt', fingerprint: true
      }
    }

  }

  post {
    always {
      echo 'Always: cleanup / publish reports'
    }
    success {
      echo 'Build succeeded'
    }
    failure {
      echo 'Build failed'
    }
  }
}
