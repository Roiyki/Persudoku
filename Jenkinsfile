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

         stage('Run Tests') {
            steps {
                // Run the tests using pytest
                sh '"C:\\Users\\roiyd\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\pytest.exe" app\\tests'
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
                sh 'git checkout main && git merge ${env.BRANCH_NAME} --no-ff --no-edit && git push origin main'
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
