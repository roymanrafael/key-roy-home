"""
TUYA PROXY — Puente entre tu panel KEY/ROY HOME y la nube de Tuya
═══════════════════════════════════════════════════════════════

INSTALACIÓN (una sola vez):
    pip install tinytuya flask flask-cors

USO:
    python3 tuya_proxy.py
    (dejalo corriendo en una terminal mientras usás el panel)

Probar que funciona:
    Abrí en el navegador: http://localhost:8787/status/6000051778ee4c84805e
    Deberías ver un JSON con los datos del aire acondicionado.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tinytuya

# ── TUS CREDENCIALES (ya las tenés) ──
API_KEY    = "my3cqccuke8fmxasgeek"
API_SECRET = "42ba1a0754434cbb8533d03eadee893c"
REGION     = "us"                            # Western America Data Center

cloud = tinytuya.Cloud(apiRegion=REGION, apiKey=API_KEY, apiSecret=API_SECRET)

app = Flask(__name__)
CORS(app)  # permite que el panel (HTML) le hable a este servidor

@app.route("/devices")
def devices():
    """Lista todos tus dispositivos vinculados"""
    return jsonify(cloud.getdevices())

@app.route("/status/<dev_id>")
def status(dev_id):
    """Devuelve el estado completo de un dispositivo (incluye temperatura)"""
    result = cloud.getstatus(dev_id)
    return jsonify(result)

@app.route("/cmd/<dev_id>", methods=["POST"])
def cmd(dev_id):
    """Envía un comando (encender, apagar, cambiar temp seteada, etc)"""
    data = request.get_json()
    commands = {"commands": [{"code": data["code"], "value": data["value"]}]}
    result = cloud.sendcommand(dev_id, commands)
    return jsonify(result)

@app.route("/stream/<dev_id>")
def stream(dev_id):
    """Pide URL de video en vivo (para la cámara)"""
    res = cloud.cloudrequest(
        f"/v1.0/devices/{dev_id}/stream/actions/allocate",
        post={"stream_type": "hls"}
    )
    return jsonify(res)

if __name__ == "__main__":
    print("=" * 50)
    print("  TUYA PROXY corriendo en http://localhost:8787")
    print("  Dejá esta terminal abierta mientras usás el panel")
    print("=" * 50)
    app.run(host="127.0.0.1", port=8787)
