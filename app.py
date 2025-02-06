import os
from flask import Flask, jsonify

app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return "¡API funcionando correctamente en Render!"

# Ruta para verificar si la clave API está cargada
@app.route('/api/verificar-clave', methods=['GET'])
def verificar_clave():
    api_key = os.getenv("OPENAI_API_KEY")
    return jsonify({"API_KEY": api_key if api_key else "No encontrada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
