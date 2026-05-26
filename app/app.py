from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "appdb"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "admin123")
    )
    return conn

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id SERIAL PRIMARY KEY,
                    contenido TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                INSERT INTO mensajes (contenido)
                VALUES ('Contenedor Flask conectado exitosamente con PostgreSQL!')
                ON CONFLICT DO NOTHING
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Base de datos inicializada correctamente")
            break
        except Exception as e:
            print(f"⏳ Esperando base de datos... {e}")
            retries -= 1
            time.sleep(3)

@app.route('/')
def index():
    return jsonify({
        "mensaje": "🚀 API Flask funcionando",
        "estado": "OK",
        "contenedor": "app"
    })

@app.route('/datos')
def datos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, contenido, fecha FROM mensajes")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        resultado = [
            {"id": r[0], "contenido": r[1], "fecha": str(r[2])}
            for r in rows
        ]
        return jsonify({
            "estado": "OK",
            "datos": resultado,
            "mensaje": "✅ Comunicación Flask ↔ PostgreSQL exitosa"
        })
    except Exception as e:
        return jsonify({"estado": "ERROR", "error": str(e)}), 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"estado": "OK", "db": "conectada"})
    except:
        return jsonify({"estado": "ERROR", "db": "desconectada"}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)