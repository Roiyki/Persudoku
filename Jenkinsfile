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
                        git clone https://github.com/Roiyki/Persudoku
                        cd Persudoku
                        """
                        // Source the .env file to load variables into the environment
                        sh 'source $HOME/Persudoku/.env'
                        
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
                    // Source the .env file again (to make sure variables are available)
                    sh 'source $HOME/Persudoku/.env'
                    sh "pip install -r $HOME/${GITHUB_REPO}/app/Backend/requirements.txt"
                }
            }
        }
        stage('Run Pytest') {
            steps {
                container('custom') {
                    // Source the .env file again (to make sure variables are available)
                    sh 'source $HOME/Persudoku/.env'
                    sh "pytest --junitxml=test-results.xml $HOME/${GITHUB_REPO}/app/tests/test_main.py"
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
                        // Merge feature branch into main branch
                        sh """
                        git fetch origin
                        git checkout main
                        git merge --no-ff feature
                        git push origin main
                        """
                        
                        // Delete feature branch
                        sh """
                        git push origin --delete feature
                        """
                        
                        // Trigger GitHub webhook
                        withCredentials([usernamePassword(credentialsId: 'github-secret-read-jenkins', usernameVariable: "${USERNAME}", passwordVariable: "${TOKEN}")]) { // Replace 'GITHUB_CREDENTIALS_ID' with your Jenkins credentials ID
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
