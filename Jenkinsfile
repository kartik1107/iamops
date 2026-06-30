pipeline {

    agent {
        kubernetes {

            defaultContainer 'python'

            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: ec2-pricing
spec:
  containers:
  - name: python
    image: kartikvijan14/jenkins-python-agent:1.0
    imagePullPolicy: Always
    command:
      - cat
    tty: true
'''
        }
    }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(
            numToKeepStr: '10',
            artifactNumToKeepStr: '5'
        ))
    }

    parameters {

        choice(
            name: 'INSTANCE_FAMILY',
            choices: [
                't3',
                't4g',
                'm5',
                'm6i',
                'm7',
                'c5',
                'c6i',
                'c7g',
                'r5',
                'r6i',
                'r7g'
            ],
            description: 'Select EC2 Instance Family'
        )
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                container('python') {
                    sh '''
                        echo "======================================"
                        echo "Environment Verification"
                        echo "======================================"

                        python --version
                        pip --version
                        git --version
                        curl --version | head -1

                        echo "======================================"
                    '''
                }
            }
        }

        stage('Verify Files') {
            steps {
                container('python') {
                    sh '''
                        echo "Workspace Contents"
                        ls -lh

                        if [ ! -f get_ec2_price.py ]; then
                            echo "ERROR: get_ec2_price.py not found."
                            exit 1
                        fi
                    '''
                }
            }
        }

        stage('Find Cheapest EC2 Instance') {
            steps {
                container('python') {
                    sh '''
                        echo ""
                        echo "======================================"
                        echo "Searching Cheapest EC2 Instance"
                        echo "======================================"

                        python get_ec2_price.py ${INSTANCE_FAMILY}
                    '''
                }
            }
        }
    }

    post {

        success {
            echo '''
==========================================
Pipeline completed successfully.
==========================================
'''
        }

        failure {
            echo '''
==========================================
Pipeline failed.
==========================================
'''
        }

        always {
            deleteDir()
        }
    }
}
