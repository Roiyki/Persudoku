pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave' // Assign a label to the pod
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
        GITHUB_USER = credentials('github-secret-read-jenkins')
    }
    triggers {
        pollSCM('H/5 * * * *') // Poll SCM every 5 minutes
    }
    stages {
        stage('Setup Git') {
            steps {
                container('custom') {
                    script {
                        // Configure Git to trust the Jenkins workspace directory
                        sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/SudokuFeatureCI'
                    }
                }
            }
        }
        stage('Clone and Switch to Feature Branch') {
            steps {
                container('custom') {
                    script {
                        // Clone the repository
                        sh """
                        cd \$HOME
                        git clone https://github.com/Roiyki/Persudoku
                        cd Persudoku
                        git fetch origin
                        if git rev-parse --quiet --verify feature; then
                            git checkout feature
                        else
                            git checkout -b feature
                        fi
                
                        # Copy files from main branch to feature branch
                        git checkout main -- .
                        git add .
                
                        # Configure Git user identity
                        git config --global user.email "you@example.com"
                        git config --global user.name "Your Name"
                
                        # Commit changes
                        git commit -m "Copy files from main branch to feature branch"
                        """
                    }
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                container('custom') {
                    // Source the .env file again (to make sure variables are available)
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
        stage('Manual Approval') {
            steps {
                container('custom') {
                    script {
                        // Execute git rev-parse HEAD to get the current commit hash
                        def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()

                        // Send GitHub status check
                        sh """
                        curl -X POST \
                        -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                        -H 'Content-Type: application/json' \
                        -d '{"state": "pending", "description": "Manual approval required", "context": "jenkins/manual-approval"}' \
                        https://api.github.com/repos/${GITHUB_USER}/Persudoku/statuses/${commitHash}
                        """

                        // Now you would typically wait for the GitHub status to be updated manually
                        // For demonstration purposes, assuming manual approval is granted
                        def manualApprovalGranted = true

                        if (manualApprovalGranted) {
                            // Check out main branch
                            sh 'git checkout main'

                            // Check if the feature branch exists
                            def featureBranchExists = sh(script: 'git show-ref --verify --quiet refs/heads/feature', returnStatus: true) == 0

                            if (featureBranchExists) {
                                // Merge feature branch into main
                                try {
                                    sh 'git merge --no-ff feature'
                                    // Push changes to remote main branch
                                    sh 'git push origin main'
                                    // Delete feature branch
                                    sh 'git branch -d feature'
                                } catch (Exception mergeError) {
                                    // Log merge error
                                    echo "Merge failed: ${mergeError}"
                                    // Exit the pipeline with an error status
                                    currentBuild.result = 'FAILURE'
                                    error("Merge failed")
                                }
                            } else {
                                echo "Feature branch does not exist"
                                // Exit the pipeline with an error status
                                currentBuild.result = 'FAILURE'
                                error("Feature branch does not exist")
                            }

                            // Trigger SudokuCI-build pipeline
                            build job: 'SudokuCI-build', parameters: [
                                // Add parameters if needed
                            ]
                        }
                    }
                }
            }
        }
    }
}