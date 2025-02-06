import os
from flask import Flask, jsonify

app = Flask(__name__)

# Cargar claves API desde variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CREADOR_DE_SAS = os.getenv("CREADOR_DE_SAS")

@app.route('/')
def home():
    return "¡API funcionando correctamente en Render!"

# Ruta para verificar que ambas claves se están leyendo
@app.route('/api/verificar-claves', methods=['GET'])
def verificar_claves():
    return jsonify({
        "OPENAI_API_KEY": OPENAI_API_KEY if OPENAI_API_KEY else "No encontrada",
        "CREADOR_DE_SAS": CREADOR_DE_SAS if CREADOR_DE_SAS else "No encontrada"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
