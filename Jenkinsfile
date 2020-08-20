pipeline {
    agent any
    stages {
        stage("Check installs") {
            sh "sudo apt-get update"
            sh "sudo apt install python3 python3-pip python3-venv"
            sh "pip3 install -r requirements.txt"
        }
        stage("Run tests") {
            sh "pytest"
        }
        stage("Run program") {
            sh "python3 project1.py"
        }
    }
}