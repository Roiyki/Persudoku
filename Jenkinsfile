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
      env:
        - name: API_TOKEN
          valueFrom:
            secretKeyRef:
              name: api-token-secret
              key: api_token
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
