pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccount: jenkins-sa
  containers:
  - name: custom
    image: roiyki/inbound-agent:latest
    command:
    - cat
    tty: true
'''
        }
    }
    triggers {
        pollSCM('* * * * *') // Poll SCM every minute
    }
    stages {
        stage('Setup Git') {
            steps {
                container('custom') {
                    script {
                        // Add exception for Jenkins workspace directory
                        sh 'git config --global --add safe.directory $HOME/agent/workspace'
                    }
                }
            }
        }
        stage('Clone and Switch to Feature Branch') {
            steps {
                container('custom') {
                    script {
                        // Clone the repository
                        sh '''
                        cd $HOME
                        git clone https://github.com/Roiyki/Persudoku
                        cd Persudoku
                        '''
                        // Check if the feature branch exists
                        sh '''
                        git fetch origin
                        if git rev-parse --quiet --verify feature; then
                            git checkout feature
                        else
                            git checkout -b feature
                        fi
                        '''
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                container('custom') {
                    sh 'pip install -r $HOME/Persudoku/app/Backend/requirements.txt'
                }
            }
        }
        stage('Run Pytest') {
            steps {
                container('custom') {
                    sh 'pytest --junitxml=test-results.xml $HOME/Persudoku/app/tests/test_main.py'
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
        }
    }
}
