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
    environment {
        GITHUB_TOKEN = credentials('github-secret-read-jenkins')
        GITHUB_USER = credentials('github-secret-read-jenkins')
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
                    sh "pip install -r $HOME/Persudoku/app/Backend/requirements.txt"
                }
            }
        }
        stage('Run Pytest') {
            steps {
                container('custom') {
                    // Source the .env file again (to make sure variables are available)
                    sh 'source $HOME/Persudoku/.env'
                    sh "pytest --junitxml=test-results.xml $HOME/Persudoku/app/tests/test_main.py"
                }
            }
        }
        stage('Manual Approval') {
            steps {
                container('custom') {
                    script {
                        // Execute git rev-parse HEAD to get the current commit hash
                        def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()

                        // Send GitHub status check
                        sh """
                        curl -X POST \
                        -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                        -H 'Content-Type: application/json' \
                        -d '{"state": "pending", "description": "Manual approval required", "context": "jenkins/manual-approval"}' \
                        https://api.github.com/repos/${GITHUB_USERNAME}/Persudoku/statuses/${commitHash}
                        """

                        // Now you would typically wait for the GitHub status to be updated manually
                        // After manual approval, update the status to "success" or "failure" accordingly
                    }
                }
            }
        }
    }
}
