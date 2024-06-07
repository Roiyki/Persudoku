pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave' // Assign a label to the pod
            defaultContainer 'custom'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-sa
  containers:
  - name: custom
    image: roiyki/inbound-agent:latest
    command:
    - cat
    tty: true
"""
        }
    }
    triggers {
        pollSCM('H/5 * * * *') // Poll SCM every 5 minutes
    }
    environment {
        DOTENV = readProperties(file: '/.env') // Replace with the path to your .env file
        GITHUB_USERNAME = "${DOTENV.GITHUB_USERNAME}"
        GITHUB_TOKEN = "${DOTENV.GITHUB_TOKEN}"
        GITHUB_REPO = "${DOTENV.GITHUB_REPO}"
    }
    stages {
        stage('Setup Git') {
            steps {
                container('custom') {
                    script {
                        // Configure Git to trust the Jenkins workspace directory
                        sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/SudokuFeatureCI'
                    }
                }
            }
        }
        stage('Clone and Switch to Feature Branch') {
            steps {
                container('custom') {
                    script {
                        // Clone the repository
                        sh """
                        cd \$HOME
                        git clone https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}
                        cd ${GITHUB_REPO}
                        """
                        // Check if the feature branch exists
                        sh """
                        git fetch origin
                        if git rev-parse --quiet --verify feature; then
                            git checkout feature
                        else
                            git checkout -b feature
                        fi
                        """
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                container('custom') {
                    sh 'pip install -r $HOME/${GITHUB_REPO}/app/Backend/requirements.txt'
                }
            }
        }
        stage('Run Pytest') {
            steps {
                container('custom') {
                    sh 'pytest --junitxml=test-results.xml $HOME/${GITHUB_REPO}/app/tests/test_main.py'
                }
            }
        }
        stage('Manual Approval') {
            steps {
                container('custom') {
                    script {
                        input message: "Do you want to proceed with deployment?", ok: "Deploy"
                    }
                }
            }
            post {
                success {
                    script {
                        // Trigger GitHub webhook
                        withCredentials([usernamePassword(credentialsId: 'GITHUB_CREDENTIALS_ID', usernameVariable: 'USERNAME', passwordVariable: 'TOKEN')]) { // Replace 'GITHUB_CREDENTIALS_ID' with your Jenkins credentials ID
                            sh """
                                curl -X POST \
                                -u ${USERNAME}:${TOKEN} \
                                -H 'Content-Type: application/json' \
                                -d '{"event_type": "run_second_pipeline"}' \
                                https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/dispatches
                            """
                        }
                    }
                }
            }
        }
    }
}
