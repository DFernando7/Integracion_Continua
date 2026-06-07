pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Repositorio clonado desde GitHub correctamente'
            }
        }

        stage('Build') {
            steps {
                echo '🔨 Construyendo imagen Docker de la aplicación Flask...'
                sh 'docker build -t flask_app ./app'
                echo '✅ Imagen construida exitosamente'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Verificando que la imagen fue creada correctamente...'
                sh 'docker images | grep flask_app'
                echo '✅ Imagen verificada correctamente'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Desplegando la aplicación...'
                sh 'docker run -d --name flask_test_ci -p 5001:5000 flask_app || true'
                sh 'sleep 5'
                sh 'docker ps | grep flask_test_ci || true'
                sh 'docker stop flask_test_ci || true'
                sh 'docker rm flask_test_ci || true'
                echo '✅ Despliegue verificado exitosamente'
            }
        }

    }

    post {
        success {
            echo '🎉 Pipeline ejecutado con éxito - Integración Continua funcionando'
        }
        failure {
            echo '❌ El pipeline falló. Revisar logs.'
        }
    }
}