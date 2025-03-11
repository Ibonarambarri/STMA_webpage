from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "Bienvenido a STMA API"})

@app.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        "empresa": "STMA Intelligent Solutions",
        "servicios": ["Consultoría", "Desarrollo", "Seguridad"]
    })

handler = app