pipeline {
  agent any

<<<<<<< HEAD
  environment {
=======
  triggers {
    pollSCM('H/5 * * * *')
  }

  environment {
    BUILD_ENV = "dev"
>>>>>>> 868ca63e5c2229d86596fbbae3ae85e4add0463b
    SONAR_AUTH_TOKEN = credentials('sonar-token')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

<<<<<<< HEAD
    stage('Setup Python Environment') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
=======
    stage('Build') {
      steps {
        echo 'Building...'
        sh '''
          echo "This is my first Jenkins build step"
          echo "Running build script..."
>>>>>>> 868ca63e5c2229d86596fbbae3ae85e4add0463b
        '''
      }
    }

<<<<<<< HEAD
    stage('Run Tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest --cov=app --cov-report xml
        '''
=======
    stage('Test') {
      steps {
        echo 'Running tests (if any)...'
>>>>>>> 868ca63e5c2229d86596fbbae3ae85e4add0463b
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          withSonarQubeEnv('MySonar') {
            sh """
              ${tool 'MyScanner'}/bin/sonar-scanner \
<<<<<<< HEAD
                -Dsonar.projectKey=my-fastapi-project \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://127.0.0.1:9000 \
                -Dsonar.token=$SONAR_AUTH_TOKEN \
                -Dsonar.python.coverage.reportPaths=coverage.xml
=======
                -Dsonar.projectKey=myproject \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://10.10.121.240:9000 \
                -Dsonar.login=$SONAR_AUTH_TOKEN
>>>>>>> 868ca63e5c2229d86596fbbae3ae85e4add0463b
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

<<<<<<< HEAD
  }

  post {
    success {
      echo "Build Completed Successfully"
    }
    failure {
      echo "Build Failed"
=======
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
>>>>>>> 868ca63e5c2229d86596fbbae3ae85e4add0463b
    }
  }
}
