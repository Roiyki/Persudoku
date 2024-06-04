pipeline {
    agent {
        kubernetes {
            inheritFrom 'jenkins-agent'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-agent
spec:
  containers:
    - name: jnlp
      image: roiyki/inbound-agent:latest
  restartPolicy: Always
"""
        }
    }
    stages {
        stage('Clone and Test') {
            steps {
                container('jnlp') {
                    sh 'git clone -b feature https://github.com/Roiyki/Persudoku.git'
                    sh 'pytest Persudoku/app/Backend'
                }
            }
        }
        stage('Trigger Main Pipeline') {
            when {
                allOf {
                    branch 'master'
                    expression {
                        currentBuild.result == 'SUCCESS'
                    }
                }
            }
            steps {
                input 'Do you want to trigger the main pipeline?'
                // Trigger the main pipeline
            }
        }
    }
}