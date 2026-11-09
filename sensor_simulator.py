import time
import json
import random
import ssl
import paho.mqtt.client as mqtt

BROKER = "udb16521.ala.us-east-1.emqxsl.com"
PORT = 8883
USER = "vinospsensor"
PASSWORD = "vinospsensor2026"

TOPIC_BASE = "vinosparry/bodega01"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+] Conexión exitosa a EMQX Cloud mediante SSL/TLS (Puerto 8883)")
        client.subscribe(f"{TOPIC_BASE}/#")
        print(f"[+] Suscrito correctamente al tópico: {TOPIC_BASE}/#")
    else:
        print(f"[-] Falló la conexión. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    print(f"[Lectura desde Broker] {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id="Codespaces_VinosParry_Sensor")
client.username_pw_set(USER, PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

client.on_connect = on_connect
client.on_message = on_message

print("Conectando con el servidor EMQX Cloud...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        lecturas = {
            "sensor01/temperatura": round(random.uniform(12.0, 18.0), 2),
            "sensor02/humedad": round(random.uniform(60.0, 80.0), 2),
            "sensor03/co2": round(random.uniform(400, 1200), 1),
            "sensor04/presion": round(random.uniform(1008.0, 1015.0), 2)
        }

        for sub_topic, valor in lecturas.items():
            full_topic = f"{TOPIC_BASE}/{sub_topic}"
            payload = json.dumps({"valor": valor, "timestamp": time.time()})
            client.publish(full_topic, payload)
            print(f"[Publicado exitosamente] {full_topic} -> {payload}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nSimulación detenida.")
    client.loop_stop()
    client.disconnect()