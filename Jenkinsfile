pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'
            defaultContainer 'jnlp'
            yaml """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins-agent
  template:
    metadata:
      labels:
        app: jenkins-agent
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
