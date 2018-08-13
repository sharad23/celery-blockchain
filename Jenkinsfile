def IMAGE_NAME="modana-api"
def CONTAINER_NAME ="modana-api-cont"
def CONTAINER_TAG="latest"
def HTTP_PORT="8000"

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
                sh 'cd app && ./manage.py test'
            }
        }
    }
}
node {
    stage('Build') {
        imagePrune(CONTAINER_NAME)
        sh "docker build -t $IMAGE_NAME ."
        sh "docker build -t celery -f Celery ."
        sh "docker build -t flower -f Flower ."

    }
    stage('Deploy'){
        sh "docker run --name postgres -d -p 5432:5432 -v modana_new_data:/var/lib/postgresql/data/ postgres"
        sh "docker run -d  -p 15672:15672  -p 5672:5672 --name rabbit1 rabbitmq:3"
        sh "docker run -p $HTTP_PORT:8000 -d --link rabbit1:rabbit -e ENV=dev --link postgres:db --name=$CONTAINER_NAME  $IMAGE_NAME "
        sh "docker run -d --link rabbit1:rabbit --link postgres:db -e ENV=dev --name celery celery"
        sh "docker run -d -p 5555:5555 --link rabbit1:rabbit -e ENV=dev --name flower flower"
    }
}

def imagePrune(containerName){
    try {
        sh "docker image prune -f"
        sh "docker stop $containerName"
        sh "docker rm $containerName"
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
        sh "docker stop postgres"
        sh "docker rm postgres"
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