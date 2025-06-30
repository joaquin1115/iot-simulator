# Proyecto IoT: Simulación de Sensores DHT22 con Wokwi y Envío a Servidor Flask

Este proyecto simula una red de sensores DHT22 en [Wokwi](https://wokwi.com/) que envían datos a un servidor Flask ejecutado localmente. Los datos de temperatura y humedad se generan aleatoriamente en Wokwi y son enviados al servidor para procesamiento. Luego, el servidor puede reenviar los datos a ThingsBoard u otro destino.

---

## 🗂 Estructura del repositorio

```
├── flask-server
│   └── main.py           # Servidor Flask que recibe los datos desde Wokwi
└── wokwi-project
    ├── diagram.json      # Circuito virtual de Wokwi con 5 sensores DHT22
    └── main.py           # Código MicroPython que simula los sensores y envía los datos
```

---

## 🚀 Paso 1: Ejecutar el servidor Flask localmente

### 1.1 Crear entorno virtual (opcional pero recomendado)

```bash
cd flask-server
python -m venv venv
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

En el archivo `wokwi-project/main.py`, asegúrate de definir:

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
3. Asegúrate de que el código MicroPython está configurado para conectarse a `Wokwi-GUEST` o a la red que desees.
4. Haz clic en el botón **▶️ Play** para iniciar la simulación.
5. En el panel de **Serial Monitor**, verás las salidas como:

```
Conectando a WiFi..... ¡Conectado!
[sensor_1] Enviando datos: {...}
[sensor_1] Respuesta: 200
```

---

## ✅ Flujo de datos

```
Wokwi (main.py)
   ↓
SERVER_URL = http://<ngrok_url>/procesar_datos
   ↓
Servidor Flask (main.py)
   ↓
Procesamiento / Envío a ThingsBoard / Consola
```

---

## 🛠 Personalización

- Puedes modificar el número de sensores, el umbral de humedad o el modelo de predicción en `flask-server/main.py`.

---

## 🧾 Licencia

Este proyecto es de libre uso para fines educativos y de prueba.
