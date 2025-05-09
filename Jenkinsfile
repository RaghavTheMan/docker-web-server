pipeline {
  agent any

  environment {
    IMAGE = "raghavboi/movie-app"  // or just "movie-search" if local
    CRED  = "dockerhub-creds"                // your Docker Hub creds ID, or leave blank to skip
  }


  stages {
    stage('Checkout') {
      steps { git url: 'https://github.com/RaghavTheMan/docker-web-server.git', branch: 'main' }
    }

    stage('Build Image') {
      steps {
        script {
          docker.build("${IMAGE}:${BUILD_NUMBER}")
        }
      }
    }

    stage('Push to Docker Hub') {
      when { expression { return env.CRED != null } }
      steps {
        withCredentials([usernamePassword(credentialsId: CRED,
                                          usernameVariable: 'USER',
                                          passwordVariable: 'PASS')]) {
          sh '''
            echo $PASS | docker login -u $USER --password-stdin
            docker push ${IMAGE}:${BUILD_NUMBER}
            docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:latest
            docker push ${IMAGE}:latest
          '''
        }
      }
    }

    stage('Deploy Locally') {
      steps {
        sh '''
          docker rm -f movie-search 2>/dev/null || true
          docker run -d --name movie-search -p 87:80 ${IMAGE}:latest
        '''
      }
    }
  }

  post {
    always { cleanWs() }
  }
}
