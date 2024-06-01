pipeline {
    agent any

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

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t persudoku-flask:latest ./app/backend/'
            }
        }

        stage('Manual Approval') {
            steps {
                input message: 'Approve to merge into main?', ok: 'Approve'
            }
        }

        stage('Merge to Main') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh '''
                        git checkout main
                        git merge ${env.BRANCH_NAME}
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/your-repo.git main
                        '''
                    }
                }
            }
        }
    }
}
