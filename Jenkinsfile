pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Clonando repositorio desde GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '🔨 Construyendo imagen Docker de la aplicación Flask...'
                sh 'docker compose build app'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Ejecutando verificación de la API...'
                sh '''
                    docker compose up -d db
                    sleep 10
                    docker compose up -d app
                    sleep 5
                    curl -f http://localhost:5000/health || exit 1
                    echo "✅ API respondiendo correctamente"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Desplegando servicios en producción...'
                sh 'docker compose up -d'
                echo '✅ Despliegue completado exitosamente'
            }
        }

    }

    post {
        success {
            echo '🎉 Pipeline ejecutado con éxito'
        }
        failure {
            echo '❌ El pipeline falló. Revisar logs.'
        }
    }
}