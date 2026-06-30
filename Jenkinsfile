pipeline {
    agent any

    parameters {
        choice(
            name: 'INSTANCE_FAMILY',
            choices: ['t', 'm', 'c', 'r'],
            description: 'EC2 Instance Family'
        )

        string(
            name: 'MIN_VCPU',
            defaultValue: '2',
            description: 'Minimum vCPUs'
        )

        string(
            name: 'MIN_MEMORY',
            defaultValue: '4',
            description: 'Minimum Memory (GiB)'
        )
    }

    environment {
        VANTAGE_TOKEN = credentials('vntg_tkn_6eb36e28befe679a8d08134abdacbf7d66cd2d4c')
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install requests
                '''
            }
        }

        stage('Find Cheapest EC2') {
            steps {
                sh """
                python3 ec2_price.py \
                    --family ${params.INSTANCE_FAMILY} \
                    --vcpu ${params.MIN_VCPU} \
                    --memory ${params.MIN_MEMORY} \
                    --token ${VANTAGE_TOKEN}
                """
            }
        }
    }
}
