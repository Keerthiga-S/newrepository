pipeline {
  agent any

  environment {
    SONAR_AUTH_TOKEN = credentials('sonar-token')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Environment') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest --cov=app --cov-report xml
        '''
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          withSonarQubeEnv('MySonar') {
            sh """
              ${tool 'MyScanner'}/bin/sonar-scanner \
                -Dsonar.projectKey=my-fastapi-project \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://sonarqube.example.com:9000 \
                -Dsonar.token=$SONAR_AUTH_TOKEN \
                -Dsonar.python.coverage.reportPaths=coverage.xml
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

  }

  post {
    success {
      echo "Build Completed Successfully"
    }
    failure {
      echo "Build Failed"
    }
  }
}
