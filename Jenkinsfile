pipeline {
    agent any

    environment {
        // SonarQube server configured in Jenkins
        SONAR_HOST_URL = "http://host.docker.internal:9000"
        SONAR_AUTH_TOKEN = credentials('sonar-token')  // Your Jenkins credential ID
        VENV_DIR = "venv"  // virtual environment directory
        IMAGE_NAME = "my-fastapi-app"
        DOCKER_TAG = "latest"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    # Create virtual environment
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate

                    # Upgrade pip
                    pip install --upgrade pip

                    # Install dependencies
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    # Run tests and generate coverage
                    pytest --cov=. --cov-report=xml
                '''
            }
            post {
                always {
                    junit '**/test-reports/*.xml'  // if you generate junit xml
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonar') {  // Jenkins SonarQube installation name
                    sh '''
                        source $VENV_DIR/bin/activate
                        /var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/MyScanner/bin/sonar-scanner \
                            -Dsonar.projectKey=my-fastapi \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Docker Build & Deploy') {
            steps {
                sh '''
                    # Build Docker image
                    docker build -t $IMAGE_NAME:$DOCKER_TAG .

                    # Push to local Docker registry (optional)
                    # docker tag $IMAGE_NAME:$DOCKER_TAG your-registry/$IMAGE_NAME:$DOCKER_TAG
                    # docker push your-registry/$IMAGE_NAME:$DOCKER_TAG

                    # Run container (for demo)
                    docker stop $IMAGE_NAME || true
                    docker rm $IMAGE_NAME || true
                    docker run -d --name $IMAGE_NAME -p 8000:8000 $IMAGE_NAME:$DOCKER_TAG
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
