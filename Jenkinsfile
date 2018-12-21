node('windows') {
    try {
        // Mark the code checkout 'stage'....
        stage('Checkout') {
            checkout scm
        }

        wrap([$class: 'AnsiColorBuildWrapper']) {
            stage('Build UI') {
                bat ''' cd ui
                        npm install
                        npm run build'''

                // Stash the built artifacts so they can be included
                stash includes: 'ui/dist/**', name: 'static_ui'
            }

            stage('Build API') {
                unstash 'static_ui'

                bat ''' cd api
                        python setup.py windows --template Python-Windows-template -b'''

                archiveArtifacts artifacts: 'api/windows/*.msi', onlyIfSuccessful: true
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


def sendNotification() {
    def buildSucceeded = 'SUCCESS'.equals(currentBuild.currentResult)

    emailext attachLog: !buildSucceeded,
            body: '$DEFAULT_CONTENT',
            replyTo: '$DEFAULT_REPLYTO',
            subject: '$DEFAULT_SUBJECT',
            to: '$DEFAULT_RECIPIENTS'
}


// vim: syntax=groovy
