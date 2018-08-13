pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3'
                }
            }
            steps {

                sh 'pip install -r requirements.txt'
                sh 'nosetests --with-coverage --cover-erase  --cover-package=tasks'
            }
        }
    }
}
node {
    stage('Build') {
        imagePrune()
        sh "docker build -t celery -f Celery ."
        sh "docker build -t flower -f Flower ."

    }
    stage('Deploy'){
        sh "docker run -d  -p 15672:15672  -p 5672:5672 --name rabbit1 rabbitmq:3"
        sh "docker run -d --link rabbit1:rabbit --name celery celery"
        sh "docker run -d -p 5555:5555 --link rabbit1:rabbit --name flower flower"
    }
}

def imagePrune(){
    try {
        sh "docker image prune -f"
    } catch(error){
        sh "echo $error"
    }
    try {
        sh "docker stop celery"
        sh "docker rm celery"
    }
     catch(error){
        sh "echo $error"
    }
    try {
        sh "docker stop flower"
        sh "docker rm flower"
    }
     catch(error){
        sh "echo $error"
    }
    try {
        sh "docker stop rabbit1"
        sh "docker rm rabbit1"
    }
     catch(error){
        sh "echo $error"
    }
}