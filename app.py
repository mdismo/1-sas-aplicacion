import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Ruta principal que muestra el archivo HTML
@app.route('/')
def home():
    return render_template("index.html")

# Ruta para verificar las claves API
@app.route('/api/verificar-claves', methods=['GET'])
def verificar_claves():
    openai_key = os.getenv("OPENAI_API_KEY")
    creador_key = os.getenv("CREADOR_DE_SAS")
    return jsonify({
        "OPENAI_API_KEY": openai_key if openai_key else "No encontrada",
        "CREADOR_DE_SAS": creador_key if creador_key else "No encontrada"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
