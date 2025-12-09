pipeline {
  agent any

  triggers {
    pollSCM('H/5 * * * *')
  }

  environment {
    BUILD_ENV = "dev"
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
