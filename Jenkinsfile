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
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/feature']], userRemoteConfigs: [[url: 'https://github.com/Roiyki/Persudoku']]])
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
                        // Wait for manual approval
                        input message: "Do you want to proceed with deployment?", ok: "Deploy"
                    }
                }
            }
        }
    }
}
