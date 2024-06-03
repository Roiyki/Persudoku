pipeline {
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml '''
            apiVersion: v1
            kind: Pod
            metadata:
              labels:
                app: jenkins-agent
            spec:
              containers:
              - name: jnlp
                image: jenkins/inbound-agent:latest
                args: ["$(JENKINS_URL)", "$(JENKINS_SECRET)", "$(JENKINS_AGENT_NAME)"]
                env:
                - name: JENKINS_URL
                  value: "http://jenkins:8080"
                - name: JENKINS_SECRET
                  value: "your-secret"
                - name: JENKINS_AGENT_NAME
                  value: "your-agent-name"
              - name: jenkins-dind
                image: docker:20.10.8-dind
                imagePullPolicy: IfNotPresent
                securityContext:
                  privileged: true
                ports:
                - containerPort: 2376
                  name: dind
                volumeMounts:
                - name: docker-certs
                  mountPath: /certs/client
            '''
            namespace: 'jenkins-namespace'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    def branch = env.BRANCH_NAME ?: 'feature' // Change to your feature branch name
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${branch}"]],
                        userRemoteConfigs: [[url: 'https://github.com/Roiyki/Persudoku.git']]
                    ])
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Run the tests using pytest
                container('jenkins-dind') {
                    sh 'pytest app/tests/'
                }
            }
        }

        stage('Merge to Main') {
            when {
                // Only execute this stage if the branch is a feature branch and tests pass
                allOf {
                    branch 'feature/*'
                    not {
                        changeRequest()
                    }
                    expression {
                        currentBuild.result == 'SUCCESS'
                    }
                }
            }
            steps {
                // Merge the feature branch into main
                container('jenkins-dind') {
                    sh 'git checkout main && git merge ${env.BRANCH_NAME} --no-ff --no-edit && git push origin main'
                }
            }
            post {
                success {
                    // Send a notification to approve the merge
                    input 'Please approve the merge to main'
                }
            }
        }
    }
}