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
