# Proyecto IoT: Simulación de Sensores DHT22 con Wokwi y Envío a Servidor Flask

Este proyecto simula una red de sensores DHT22 en [Wokwi](https://wokwi.com/) que envían datos a un servidor Flask ejecutado localmente. Los datos de temperatura y humedad se generan aleatoriamente en Wokwi y son enviados al servidor para procesamiento. Luego, el servidor reenvía los datos a una plataforma de IoT, en este caso ThingsBoard.

---

## 🗂 Estructura del repositorio

```
├── flask-server
│   └── main.py           # Servidor Flask que recibe los datos desde Wokwi y los envía a ThingsBoard
└── wokwi-project
    ├── diagram.json      # Circuito virtual de Wokwi con 5 sensores DHT22
    └── main.py           # Código MicroPython que simula los sensores y envía los datos
```

---

## 🚀 Paso 1: Ejecutar el servidor Flask localmente

### 1.1 Crear entorno virtual (opcional)

```bash
cd flask-server
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 1.2 Instalar dependencias

```bash
pip install flask requests
```

### 1.3 Ejecutar el servidor

```bash
python main.py
```

Esto inicia el servidor Flask en `http://localhost:5000`.

---

## 🌐 Paso 2: Exponer el servidor con Ngrok

### 2.1 Instalar [Ngrok](https://ngrok.com/download)

Descarga e instala ngrok si aún no lo tienes.

### 2.2 Conectar tu cuenta de ngrok (solo la primera vez)

```bash
ngrok config add-authtoken <YOUR_AUTH_TOKEN>
```

### 2.3 Iniciar túnel HTTP al puerto 5000

```bash
ngrok http --scheme=http 5000
```

Ngrok mostrará una URL pública como:

```
Forwarding http://1a2b3c4d.ngrok.io -> http://localhost:5000
```

---

## 📲 Paso 3: Configurar la URL en el proyecto Wokwi

En el archivo `wokwi-project/main.py`, define:

```python
SERVER_URL = "http://1a2b3c4d.ngrok.io/procesar_datos"
```

> **IMPORTANTE:** Reemplaza la URL con la que te dé ngrok al correr el túnel.

---

## 🧪 Paso 4: Ejecutar el proyecto en Wokwi

1. Abre [https://wokwi.com/](https://wokwi.com/).
2. Carga el contenido de la carpeta `wokwi-project`, incluyendo:
   - `main.py`
   - `diagram.json`
3. Asegúrate de que el código MicroPython está configurado para conectarse a `Wokwi-GUEST`.
4. Haz clic en el botón **▶️ Play** para iniciar la simulación.
5. En el monitor serie, verás:

```
Conectando a WiFi..... ¡Conectado!
[sensor_1] Enviando datos: {...}
[sensor_1] Respuesta: 200
```

---

## 🌍 Envío de datos a ThingsBoard

Este proyecto está configurado para enviar los datos al backend de **ThingsBoard**, una plataforma IoT de código abierto.

### 🔧 Configuración en `flask-server/main.py`

En lugar de enviar los datos a Thinger.io, usa la siguiente variable:

```python
THINGSBOARD_URL = "http://demo.thingsboard.io/api/v1/<ACCESS_TOKEN>/telemetry"
```

Ejemplo:

```python
THINGSBOARD_URL = "http://demo.thingsboard.io/api/v1/h2kq7d5uz48s8n34r012/telemetry"
```

Donde `h2kq7d5uz48s8n34r012` es el token del dispositivo en ThingsBoard. Para este proyecto se usaron seis dispositivos.

---

### 🛠 Cómo crear un dispositivo en ThingsBoard

1. Entra a [https://demo.thingsboard.io](https://demo.thingsboard.io).
2. Inicia sesión.
3. Ve a **Entidades > Dispositivos > + Agregar nuevo dispositivo**.
4. Asigna un nombre como `sensodanper_1`, deja los demás campos por defecto. Estos para los 6 dispositivos.
5. Haz clic en **"Siguiente: Credenciales"**.
6. Copia el token en la pestaña **"Access token"**.
7. Sustitúyelo en `THINGSBOARD_URL` dentro de `main.py`.

---

### 📨 Ejemplo del JSON enviado

```json
{
  "sensor_id": "sensor_1",
  "temperature": 27.3,
  "humidity": 45.2,
  "alerta_humedad": 0,
  "water_usage_efficiency": 0.0,
  "lat": -7.31,
  "lng": -79.53
}
```

Estos datos aparecerán en la pestaña **Latest Telemetry** del dispositivo en ThingsBoard.

---

## ✅ Flujo de datos

```
Wokwi (main.py)
   ↓
SERVER_URL = http://<ngrok_url>/procesar_datos
   ↓
Servidor Flask (main.py)
   ↓
Procesamiento
   ↓
Envío vía HTTP POST
   ↓
ThingsBoard (telemetría en dashboard)
```

---
## ✅ Configurar Panel

Una vez en ThingsBoard. Ingresas a la sección dashboards, haces click a "Add Dashboards" e importar "menu.json" lo cual lo encuentras en seción principal del Github.

Verfique que todos los widgets esten relacionados a un dispositivo.

---

## 🧾 Licencia

Este proyecto es de libre uso para fines educativos y de prueba.
