pipeline {
    agent any
    stages {
        stage("Check installs") {
            steps{
                sh "sudo apt-get update"
                sh "sudo apt install python3 python3-pip python3-venv"
                sh "pip3 install -r requirements.txt"
                sh "pip3 install gunicorn"
            }
        }
        // stage("Run tests") {
        //     steps{
        //         sh "python3 -m pytest"
        //     }
        // }
        stage("Run program") {
            steps{
                sh "gunicorn --workers=5 project1.py"
            }
        }
    }
}