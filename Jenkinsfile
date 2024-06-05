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
    stages {
        stage('Clone and Switch to Feature Branch') {
            steps {
                container('custom') {
                    sh '''
                    cd $HOME
                    git clone https://github.com/Roiyki/Persudoku
                    cd Persudoku
                    git checkout feature
                    '''
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
    }
}
