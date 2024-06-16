pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave-pipeline-a'
            defaultContainer 'custom'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-sa
  containers:
  - name: custom
    image: roiyki/inbound-agent-root:latest
    command:
    - cat
    tty: true
"""
        }
    }

    environment {
        GITHUB_TOKEN = credentials('github-secret-read-jenkins')
        GITHUB_USER = 'Roiyki'
        REPO = 'Roiyki/Persudoku'
        GIT_CREDENTIALS_ID = 'github-secret-read-jenkins'
        MONGO_URI = 'mongodb://mongo-service.mongo-namespace:27017/sudoku_app'
    }

    stages {
        stage('Setup') {
            steps {
                checkout scm
                script {
                    def initEnv = { echo 'Environment setup initialized' }
                    def getUniqueBuildIdentifier = { suffix = '' ->
                        def now = new Date()
                        def formattedDate = now.format("yyyyMMdd-HHmmss", TimeZone.getTimeZone('UTC'))
                        return formattedDate + (suffix ? '-' + suffix : '')
                    }
                    initEnv()
                    def id = getUniqueBuildIdentifier()
                    if (env.BRANCH_NAME == 'main') {
                        env.BUILD_ID = "1." + id
                    } else {
                        env.BUILD_ID = "0." + id
                    }
                    currentBuild.displayName += " {build-name:" + env.BUILD_ID + "}"
                }
            }
        }

        stage('Clone and Switch to Feature Branch') {
            steps {
                catchError {
                    container('custom') {
                        sh '''
                            cd /home/jenkins/agent/workspace
                            git clone https://${GITHUB_TOKEN}@github.com/${REPO}.git
                            cd Persudoku
                            git fetch origin
                            if git rev-parse --quiet --verify feature; then
                                git checkout feature
                            else
                                git checkout -b feature
                            fi
                            git checkout main -- .
                            git add .
                            git pull origin main
                            git config --global user.email "roiydonagi@gmail.com"
                            git config --global user.name "Roiyki"
                            git commit -m "Copy files from main branch to feature branch" || true
                            git push origin feature
                        '''
                    }
                }
            }
        }

        stage('Install Requirements') {
            steps {
                catchError {
                    container('custom') {
                        dir('/home/jenkins/agent/workspace/Persudoku') {
                            sh "pip install -r app/Backend/requirements.txt"
                        }
                    }
                }
            }
        }

        stage('Run Pytest') {
            steps {
                catchError {
                    container('custom') {
                        dir('/home/jenkins/agent/workspace/Persudoku') {
                            sh "pytest --junitxml=test-results.xml app/tests/test_main.py"
                        }
                    }
                }
            }
        }

        stage('Create Pull Request (feature)') {
            when {
                branch 'feature'
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'git-secret', variable: 'GIT_TOKEN')]) {
                        def createPR = """
                            curl -u ${env.GITHUB_USERNAME}:${env.GIT_TOKEN} -X POST -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/${env.GITHUB_REPO}/pulls -d '{
                                "title": "Auto PR from Jenkins: ${env.BUILD_ID}",
                                "head": "${env.BRANCH_NAME}",
                                "base": "main"
                            }'
                        """
                        sh createPR
                    }
                }
            }
        }

        stage('Manual Approval (feature)') {
            when {
                branch 'feature'
            }
            steps {
                script {
                    input message: 'Approve the merge to main?', ok: 'Approve'
                }
            }
        }

        stage('Merge Feature Branch (feature)') {
            when {
                branch 'feature'
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'git-secret', variable: 'GIT_TOKEN')]) {
                        def prList = sh(script: """
                            curl -u ${env.GITHUB_USERNAME}:${env.GIT_TOKEN} -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/${env.GITHUB_REPO}/pulls?head=${env.GITHUB_USERNAME}:${env.BRANCH_NAME}
                        """, returnStdout: true).trim()
                        def prNumber = new groovy.json.JsonSlurper().parseText(prList).find { it.head.ref == "${env.BRANCH_NAME}" }.number
                        def mergePR = """
                            curl -u ${env.GITHUB_USERNAME}:${env.GIT_TOKEN} -X PUT -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/${env.GITHUB_REPO}/pulls/${prNumber}/merge
                        """
                        sh(mergePR)
                    }
                }
            }
        }

        stage('Manual Approval') {
            when {
                beforeAgent true
                expression { true }
            }
            steps {
                script {
                    def manualApprovalGranted = input message: 'Approve deployment to main?', ok: 'Approve'

                    if (manualApprovalGranted) {
                        container('custom') {
                            dir('/home/jenkins/agent/workspace/Persudoku') {
                                def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                                sh """
                                curl -X POST \
                                -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                                -H 'Content-Type: application/json' \
                                -d '{"state": "success", "description": "Manual approval granted", "context": "jenkins/manual-approval"}' \
                                https://api.github.com/repos/${REPO}/statuses/${commitHash}
                                """

                                sh 'git checkout main'
                                sh 'git branch -D feature'
                                sh "git push origin --delete feature"
                                build job: 'sudokuCI2', parameters: []
                            }
                        }
                    } else {
                        container('custom') {
                            dir('/home/jenkins/agent/workspace/Persudoku') {
                                sh 'git checkout feature'
                                sh 'git reset --hard HEAD~1'
                                sh 'git push origin feature --force'
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline POST:'
        }
        success {
            echo 'Pipeline SUCCESS!'
        }
        failure {
            echo 'Pipeline FAILED, check the logs for more information!'
        }
    }
}
