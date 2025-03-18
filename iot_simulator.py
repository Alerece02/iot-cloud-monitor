import time
import json
import random
import boto3
import paho.mqtt.client as mqtt
import psycopg2
import socket
import os
from dotenv import load_dotenv  # Per caricare variabili di ambiente da .env
from sqlalchemy import create_engine, text

#Carica le variabili d'ambiente dal file .env
load_dotenv()

#Configurazione AWS IoT
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
THING_NAME = os.getenv("THING_NAME")
TOPIC_SHADOW_UPDATE = f"$aws/things/{THING_NAME}/shadow/update"
TOPIC_SHADOW_GET = f"$aws/things/{THING_NAME}/shadow/get"

#Percorsi certificati AWS
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
ROOT_CA_PATH = os.getenv("ROOT_CA_PATH")

#Configurazione PostgreSQL (con SQLAlchemy)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

#Soglia di temperatura critica
THRESHOLD_TEMP = 30.0  

#Forza IPv4 per evitare problemi di risoluzione
socket.getaddrinfo(AWS_ENDPOINT, 8883, socket.AF_INET)

#Configura il client MQTT (Fix API Deprecation)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=THING_NAME, protocol=mqtt.MQTTv311)
client.tls_set(ROOT_CA_PATH, certfile=CERTIFICATE_PATH, keyfile=PRIVATE_KEY_PATH)

#Callback MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connessione MQTT riuscita!")
    else:
        print(f"❌ Errore di connessione MQTT: Codice {rc}")

client.on_connect = on_connect

#Connessione MQTT con gestione errori
try:
    print("🛠️ Tentativo di connessione MQTT...")
    client.connect(AWS_ENDPOINT, 8883, 60)
    client.loop_start()
    print("✅ Connesso a AWS IoT Core!")
except Exception as e:
    print(f"❌ Errore di connessione MQTT: {e}")
    exit(1)

#Configurazione AWS IoT Shadow
iot_client = boto3.client("iot-data", region_name="eu-north-1")

#Funzione per ottenere la temperatura desiderata dallo Shadow AWS
def get_desired_temperature():
    try:
        response = iot_client.get_thing_shadow(thingName=THING_NAME)
        shadow_data = json.loads(response["payload"].read())
        return shadow_data["state"]["desired"].get("temperature", 22.0)  
    except Exception as e:
        print("⚠️ Errore nel leggere lo Shadow:", e)
        return 22.0  

#Funzione per salvare i dati su PostgreSQL
def save_to_postgres(device_name, temperature):
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO temperature_data (device_name, temperature, timestamp) 
                VALUES (:device_name, :temperature, NOW());
            """)
            conn.execute(query, {"device_name": device_name, "temperature": temperature})
            conn.commit()
            print(f"✅ Dato salvato in PostgreSQL: {device_name} - {temperature}°C")
    except Exception as e:
        print(f"❌ Errore nel salvataggio su PostgreSQL: {e}")

#Parametri di esecuzione
MAX_ITERATIONS = 100  
count = 0  

#Loop principale per inviare dati
while count < MAX_ITERATIONS:
    desired_temp = get_desired_temperature()
    reported_temp = round(desired_temp + random.uniform(-1.5, 1.5), 2)

    payload = {
        "state": {
            "reported": {
                "temperature": reported_temp
            }
        }
    }

    try:
        result = client.publish(TOPIC_SHADOW_UPDATE, json.dumps(payload))
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"📡 Stato aggiornato: Temperatura riportata = {reported_temp}°C")
            save_to_postgres(THING_NAME, reported_temp)

        else:
            print(f"⚠️ Errore nella pubblicazione MQTT: Codice {result.rc}")
    except Exception as e:
        print(f"❌ Errore nella pubblicazione MQTT: {e}")

    count += 1  
    time.sleep(5)  

print("✅ Raggiunto il limite massimo di iterazioni. Il programma termina.")
