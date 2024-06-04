pipeline {
    agent {
        kubernetes {
            // Define the pod template
            yaml """
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-agent
spec:
  containers:
    - name: jnlp
      image: roiyki/inbound-agent:latest
      // Add tty for interactive shell
      tty: true
      // Add volume mounts if necessary
      // Add environment variables if necessary
  restartPolicy: Always
"""
        }
    }
    stages {
        stage('Clone and Test') {
            steps {
                // Use the container named 'jnlp'
                container('jnlp') {
                    // Make sure the git clone and test commands are running from the correct directory
                    dir('workspace') {
                        // Clone the repository
                        sh 'git clone -b feature https://github.com/Roiyki/Persudoku.git'
                        // Change directory to the cloned repository
                        dir('Persudoku') {
                            // Run the tests
                            sh 'pytest app/Backend'
                        }
                    }
                }
            }
        }
        stage('Trigger Main Pipeline') {
            when {
                // Only trigger the main pipeline if the branch is 'master' and the current build result is 'SUCCESS'
                allOf {
                    branch 'master'
                    expression {
                        currentBuild.result == 'SUCCESS'
                    }
                }
            }
            steps {
                // Ask for user input before triggering the main pipeline
                input 'Do you want to trigger the main pipeline?'
                // Trigger the main pipeline here
            }
        }
    }
}
