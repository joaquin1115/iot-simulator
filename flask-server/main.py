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

THINGSBOARD_URL1 = "http://demo.thingsboard.io/api/v1/09liec8fz5s3jkh2fqnx/telemetry"
THINGSBOARD_URL2 = "http://demo.thingsboard.io/api/v1/3fiqeu0996trifoyeoys/telemetry"
THINGSBOARD_URL3 = "http://demo.thingsboard.io/api/v1/sd3vuk7rhcsqej0a3365/telemetry"
THINGSBOARD_URL4 = "http://demo.thingsboard.io/api/v1/jcshuayijv2pshl1grjr/telemetry"
THINGSBOARD_URL5 = "http://demo.thingsboard.io/api/v1/2qp07gel05og37bg572p/telemetry"

# Para la capacidad de agua
THINGSBOARD_URL6 = "http://demo.thingsboard.io/api/v1/iw94hxtgdizta9u4owbd/telemetry"


url_map = {
    "sensor_1": THINGSBOARD_URL1,
    "sensor_2": THINGSBOARD_URL2,
    "sensor_3": THINGSBOARD_URL3,
    "sensor_4": THINGSBOARD_URL4,
    "sensor_5": THINGSBOARD_URL5
}

tanque_agua = 500.0

# Estado actual de la predicción por sensor
estado_modelo = {sensor_id: 0.0 for sensor_id in SENSORES_INFO}

estado_alerta_anterior = {sensor_id: 0.0 for sensor_id in SENSORES_INFO}

def predecir_eficiencia_agua(N, P, K, temperature, humidity, rainfall, label, soil_moisture, organic_matter):
    """
    Función de predicción temporal para water_usage_efficiency.
    Retorna un valor fijo (4.5), solo llamada cuando alerta_humedad == 1.
    """
    return 4.5

@app.route("/procesar_datos", methods=["POST"])
def procesar_datos():
    global tanque_agua

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

    alerta_anterior = estado_alerta_anterior.get(sensor_id, 0)

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
    elif alerta_anterior == 1 and alerta == 0:
        eficiencia = estado_modelo.get(sensor_id, 0.0)
        # Se modifica aqui por tamaño de parcela
        tanque_agua = max(0.0, tanque_agua - eficiencia)
        print(f"Descontado {eficiencia} L del tanque. Restante: {tanque_agua:.2f} L")
        estado_modelo[sensor_id] = 0.0
    elif alerta == 0:
        estado_modelo[sensor_id] = 0.0

    estado_alerta_anterior[sensor_id] = alerta

    resultado = {
        **data,
        "water_usage_efficiency": estado_modelo[sensor_id]
    }

    capacidad_tanque = {
        "tank_remaining_liters": tanque_agua
    }

    # Enviar a ThingsBoard
    headers = {
        "Content-Type": "application/json"
    }

    url = url_map.get(sensor_id)

    print(f"📤 Enviando a ThingsBoard: {resultado}")
    response = requests.post(url, json=resultado, headers=headers)
    responseCap = requests.post(THINGSBOARD_URL6, json=capacidad_tanque, headers=headers)
    print(f"🔁 Código de respuesta ThingsBoard: {response.status_code}")
    print(f"🔁 Código de respuesta ThingsBoard: {rresponseCap.status_code}")

    return jsonify({
        "enviado_a_thingsboard": response.status_code,
        "resultado": resultado
    })

if __name__ == "__main__":
    app.run(port=5000)
