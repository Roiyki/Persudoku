pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-agent
spec:
  containers:
    - name: jnlp
      image: roiyki/inbound-agent:latest
      tty: true
      volumeMounts:
        - mountPath: /home/jenkins/agent
          name: workspace-volume
  restartPolicy: Never
  volumes:
    - emptyDir:
        medium: ""
      name: workspace-volume
"""
        }
    }
    stages {
        stage('Clone and Test') {
            steps {
                container('jnlp') {
                    dir('workspace') {
                        sh 'git clone -b feature https://github.com/Roiyki/Persudoku.git'
                        dir('Persudoku') {
                            sh 'pytest app/Backend'
                        }
                    }
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
                // Trigger the main pipeline here
            }
        }
    }
}