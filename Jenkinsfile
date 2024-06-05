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
  serviceAccountName: jenkins-sa
  containers:
    - name: jnlp
      image: roiyki/inbound-agent:latest
      tty: true
      env:
        - name: JENKINS_SECRET
          valueFrom:
            secretKeyRef:
              name: jenkins-credentials
              key: jenkins_secret
        - name: JENKINS_AGENT_NAME
          value: "sudokuci1-7-cw2zc-gwlrt-50dlk"
        - name: JENKINS_NAME
          value: "sudokuci1-7-cw2zc-gwlrt-50dlk"
        - name: JENKINS_WEB_SOCKET
          value: "true"
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
                script {
                    def apiToken = env.API_TOKEN
                    // Use the API token as needed, for example to trigger another job or an API call
                    sh """
                    curl -X POST -H 'Authorization: Bearer ${apiToken}' https://api.example.com/trigger-main-pipeline
                    """
                }
            }
        }
    }
}
