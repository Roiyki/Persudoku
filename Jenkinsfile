pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave'
            defaultContainer 'custom'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-sa
  containers:
  - name: custom
    image: roiyki/inbound-agent:latest
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
    }
    triggers {
        pollSCM('H/5 * * * *') // Poll SCM every 5 minutes
    }
    stages {
        stage('Setup Git') {
            steps {
                container('custom') {
                    script {
                        sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/SudokuFeatureCI'
                    }
                }
            }
        }
        stage('Clone and Switch to Feature Branch') {
            steps {
                container('custom') {
                    script {
                        sh """
                        cd \$HOME
                        git clone https://github.com/${REPO}
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
                        """
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                container('custom') {
                    sh "pip install -r app/Backend/requirements.txt"
                }
            }
        }
        stage('Run Pytest') {
            steps {
                container('custom') {
                    sh "pytest --junitxml=test-results.xml app/tests/test_main.py"
                }
            }
        }
        stage('Update GitHub Status to Pending') {
            steps {
                container('custom') {
                    script {
                        def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                        sh """
                        curl -X POST \
                        -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                        -H 'Content-Type: application/json' \
                        -d '{"state": "pending", "description": "Pipeline in progress", "context": "jenkins/manual-approval"}' \
                        https://api.github.com/repos/${REPO}/statuses/${commitHash}
                        """
                    }
                }
            }
        }
        stage('Manual Approval') {
            steps {
                container('custom') {
                    script {
                        def manualApprovalGranted = input message: 'Approve deployment to main?', ok: 'Approve'

                        if (manualApprovalGranted) {
                            def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                            sh """
                            curl -X POST \
                            -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                            -H 'Content-Type: application/json' \
                            -d '{"state": "success", "description": "Manual approval granted", "context": "jenkins/manual-approval"}' \
                            https://api.github.com/repos/${REPO}/statuses/${commitHash}
                            """

                            sh 'git checkout main'
                            def featureBranchExists = sh(script: 'git show-ref --verify --quiet refs/heads/feature', returnStatus: true) == 0

                            if (featureBranchExists) {
                                try {
                                    sh 'git merge --no-ff feature'
                                    sh 'git push origin main'
                                    sh 'git branch -d feature'
                                } catch (Exception mergeError) {
                                    echo "Merge failed: ${mergeError}"
                                    currentBuild.result = 'FAILURE'
                                    error("Merge failed")
                                }
                            } else {
                                echo "Feature branch does not exist"
                                currentBuild.result = 'FAILURE'
                                error("Feature branch does not exist")
                            }

                            build job: 'SudokuCI-build', parameters: []
                        } else {
                            error("Manual approval not granted")
                        }
                    }
                }
            }
        }
    }
}
