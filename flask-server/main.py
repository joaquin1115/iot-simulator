from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Valores fijos por sensor
SENSORES_INFO = {
    "sensor_1": {"N": 90, "P": 40, "K": 40, "rainfall": 12.5, "organic_matter": 2.5, "label": "Loam"},
    "sensor_2": {"N": 85, "P": 38, "K": 42, "rainfall": 11.0, "organic_matter": 2.1, "label": "Clay"},
    "sensor_3": {"N": 88, "P": 41, "K": 39, "rainfall": 10.5, "organic_matter": 2.3, "label": "Sand"},
    "sensor_4": {"N": 92, "P": 43, "K": 37, "rainfall": 13.0, "organic_matter": 2.7, "label": "Loam"},
    "sensor_5": {"N": 86, "P": 39, "K": 40, "rainfall": 12.0, "organic_matter": 2.6, "label": "Silt"},
}

THINGSBOARD_URL = "http://demo.thingsboard.io/api/v1/<ACCESS_TOKEN>/telemetry"

# Estado actual de la predicción por sensor
estado_modelo = {sensor_id: 0.0 for sensor_id in SENSORES_INFO}

def predecir_eficiencia_agua(N, P, K, temperature, humidity, rainfall, label, soil_moisture, organic_matter):
    """
    Función de predicción temporal para water_usage_efficiency.
    Retorna un valor fijo (4.5), solo llamada cuando alerta_humedad == 1.
    """
    return 4.5

@app.route("/procesar_datos", methods=["POST"])
def procesar_datos():
    data = request.json
    sensor_id = data.get("sensor_id")
    print(f"📥 Recibido de Wokwi: {data}")

    if sensor_id not in SENSORES_INFO:
        return jsonify({"error": "sensor_id desconocido"}), 400

    info = SENSORES_INFO[sensor_id]
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    soil = data.get("soil_moisture", 0)
    alerta = data.get("alerta_humedad", 0)

    # Lógica de control de predicción
    if alerta == 1:
        # Ejecutar predicción y almacenar el valor
        eficiencia = predecir_eficiencia_agua(
            N=info["N"],
            P=info["P"],
            K=info["K"],
            temperature=temperature,
            humidity=humidity,
            rainfall=info["rainfall"],
            label=info["label"],
            soil_moisture=soil,
            organic_matter=info["organic_matter"]
        )
        estado_modelo[sensor_id] = eficiencia
    elif alerta == 0:
        estado_modelo[sensor_id] = 0.0

    resultado = {
        **data,
        "water_usage_efficiency": estado_modelo[sensor_id]
    }

    # Enviar a ThingsBoard
    headers = {
        "Content-Type": "application/json"
    }

    print(f"📤 Enviando a ThingsBoard: {resultado}")
    response = requests.post(THINGSBOARD_URL, json=resultado, headers=headers)
    print(f"🔁 Código de respuesta ThingsBoard: {response.status_code}")

    return jsonify({
        "enviado_a_thingsboard": response.status_code,
        "resultado": resultado
    })

if __name__ == "__main__":
    app.run(port=5000)
