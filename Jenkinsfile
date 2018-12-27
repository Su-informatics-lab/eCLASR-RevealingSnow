node('windows') {
    try {
        // Mark the code checkout 'stage'....
        stage('Checkout') {
            checkout scm
        }

        wrap([$class: 'AnsiColorBuildWrapper']) {
            stage('Build UI') {
                dir('ui') {
                    cleanFolder('dist')

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
                    cleanFolder('windows\\content')
                    cleanFiles('windows\\*.msi')

                    bat 'move dist\\static snow\\'
                    bat 'move dist\\index.html snow\\static\\'

                    configFileProvider([configFile(fileId: 'rs-config-environment', replaceTokens: true, targetLocation: 'snow/.config.env')]) {
                        bat 'python setup.py windows --template Python-Windows-template --icon snow -b'
                    }

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

def cleanFiles(String glob) {
    files = findFiles(glob: glob)
    for (file in files) {
        bat "del /q \"${file.path}\""
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
