from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return "¡API funcionando correctamente en Render!"

# Ruta para recibir datos (ejemplo con JSON)
@app.route('/api/suma', methods=['POST'])
def suma():
    data = request.get_json()
    if 'num1' in data and 'num2' in data:
        resultado = data['num1'] + data['num2']
        return jsonify({"resultado": resultado})
    return jsonify({"error": "Faltan datos"}), 400

# Ruta para obtener datos (ejemplo con parámetros)
@app.route('/api/mensaje/<nombre>', methods=['GET'])
def mensaje(nombre):
    return jsonify({"mensaje": f"Hola, {nombre}!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
