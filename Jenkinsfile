pipeline {
    agent any

    stages {
        stage('Clone Test Repo') {
            steps {
                git url: 'https://github.com/Wahab-x78/test_cases', branch: 'main'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD":/app \
                      -w /app \
                      python:3.11-slim \
                      bash -c "apt-get update && apt-get install -y chromium-driver xsltproc && pip install -r requirements.txt && pytest tests/ -v --junitxml=test-reports/results.xml && mkdir -p email-summary && xsltproc --output email-summary/test-summary.txt tools/junit-to-text.xsl test-reports/results.xml && cp test-reports/results.xml email-summary/"
                '''
            }
        }

        stage('Generate Test Summary') {
            steps {
                sh '''
                    mkdir -p email-summary
                    if [ -f email-summary/test-summary.txt ]; then
                        cat email-summary/test-summary.txt
                    else
                        echo "No test summary generated" > email-summary/test-summary.txt
                    fi
                    ls -la email-summary/
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }

        success {
            script {
                def testSummary = readFile('email-summary/test-summary.txt')
                mail to: 'abdulwahabsarwar91@gmail.com',  // Replace with your email
                     subject: 'Selenium Tests Passed with Test Results',
                     body: """Tests passed successfully! 🎉

Here are the test case results:

${testSummary}

- Jenkins
Run at: ${new Date().format('yyyy-MM-dd HH:mm:ss z', TimeZone.getTimeZone('Asia/Karachi'))} PKT"""
            }
        }

        failure {
            echo 'Tests failed.'
            script {
                def testSummary = fileExists('email-summary/test-summary.txt') ? readFile('email-summary/test-summary.txt') : 'No test summary available due to test failure.'
                mail to: 'abdulwahabsarwar91@gmail.com',  // Replace with your email
                     subject: 'Selenium Tests Failed',
                     body: """Tests failed.

Here are the test case results (if available):

${testSummary}

- Jenkins
Run at: ${new Date().format('yyyy-MM-dd HH:mm:ss z', TimeZone.getTimeZone('Asia/Karachi'))} PKT"""
            }
        }
    }
}