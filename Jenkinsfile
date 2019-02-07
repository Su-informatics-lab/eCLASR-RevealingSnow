node('windows') {
    try {
        // Mark the code checkout 'stage'....
        stage('Checkout') {
            checkout scm
        }

        wrap([$class: 'AnsiColorBuildWrapper']) {
            stage('Test UI') {
                dir('ui') {
                    bat 'npm install'
                    bat 'npm run test:jenkins'

                    junit 'report.xml'
                    publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: false,
                            keepAll: true,
                            reportDir: 'test/unit/coverage/lcov-report',
                            reportFiles: 'index.html',
                            reportName: 'UI Code Coverage'
                    ])
                }
            }

            stage('Test API') {
                dir('api') {
                    bat 'pipenv install --dev'
                    bat 'pipenv run nosetests --with-xunit --with-coverage --cover-package=snow --cover-html tests'

                    junit 'nosetests.xml'
                    publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: false,
                            keepAll: true,
                            reportDir: 'cover',
                            reportFiles: 'index.html',
                            reportName: 'API Code Coverage'
                    ])
                }
            }

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
                    cleanFolder('windows')

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

def sendNotification() {
    def buildSucceeded = 'SUCCESS'.equals(currentBuild.currentResult)

    emailext attachLog: !buildSucceeded,
            body: '$DEFAULT_CONTENT',
            replyTo: '$DEFAULT_REPLYTO',
            subject: '$DEFAULT_SUBJECT',
            to: '$DEFAULT_RECIPIENTS'
}


// vim: syntax=groovy
