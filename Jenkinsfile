pipeline {
  environment {
    registry = "oabuoun/web-calculator"
    registryCredential = "dockerhub"
    dockerImage = ''
  }

  agent any

  options {
    skipStagesAfterUnstable()
  }

  stages {
    stage('Cloning our Git') {
    		steps {
            git branch: 'main',
            url: 'https://github.com/oabuoun/calculator.git'
    		}
    }

    stage('Build') {
      agent {
          docker {
              image 'python:2-alpine'
          }
      }
      steps {
          sh 'python3 -v -m py_compile calculator/*'
          stash(name: 'compiled-results', includes: 'sources/*.py*')
      }
    }

    stage('Test') {
    	agent {
    			docker {
    					image 'qnib/pytest'
    			}
    	}
    	steps {
    			sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
    	}
    	post {
    			always {
    					junit 'test-reports/results.xml'
    			}
    	}
    }

    stage('Build-Image') {
    	steps{
    			script {
    			dockerImage = docker.build registry + ":$BUILD_NUMBER"
    			}
    	}
    }

    stage('Deploy Image') {
    	steps{
    			script {
    					docker.withRegistry( '', registryCredential ) {
    							dockerImage.push()
    					}
    			}
    	}
    }

    stage('Remove Unused docker image') {
    	steps{
    			sh "docker rmi $registry:$BUILD_NUMBER"
    	}
    }
  }
}
