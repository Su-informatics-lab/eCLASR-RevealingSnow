node('windows') {
    try {
        // Mark the code checkout 'stage'....
        stage('Checkout') {
            checkout scm
        }

        wrap([$class: 'AnsiColorBuildWrapper']) {
            stage('Build UI') {
                dir('ui') {
                    bat 'npm install'
                    bat 'npm run build'

                    // Stash the built artifacts so they can be included
                    stash includes: 'dist/**', name: 'static_ui'
                }
            }

            stage('Build API') {
                dir('api') {
                    unstash 'static_ui'

                    cleanFolder('static')
                    cleanFolder('snow\\static')
                    cleanFolder('windows')

                    bat 'rename dist static'
                    bat 'move static snow\\'

                    writeFile file: 'snow/.config.env', text: '''TRACKING_API_URL_BASE=http://localhost:8123/rest/ehrselection
TRACKING_API_EXPORT_PATH=upload
TRACKING_API_AUTH_USER=foo
TRACKING_API_AUTH_PASS=bar
TRACKING_API_TIMEOUT=5.0'''

                    bat 'python setup.py windows --template Python-Windows-template -b'

                    archiveArtifacts artifacts: 'windows/*.msi', onlyIfSuccessful: true
                }
            }
        }
    }
    catch (err) {
        echo "Caught: ${err}"
        currentBuild.result = 'FAILURE'
    }
    finally {
        sendNotification()
    }
}

def cleanFolder(String path) {
    if (fileExists(path)) {
        bat "rmdir /s /q ${path}"
    }
}

def sendNotification() {
    def buildSucceeded = 'SUCCESS'.equals(currentBuild.currentResult)

    emailext attachLog: !buildSucceeded,
            body: '$DEFAULT_CONTENT',
            replyTo: '$DEFAULT_REPLYTO',
            subject: '$DEFAULT_SUBJECT',
            to: '$DEFAULT_RECIPIENTS'
}


// vim: syntax=groovy
