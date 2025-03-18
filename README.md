# IoT Cloud Monitor 🚀  
**Un sistema IoT per monitorare la temperatura e salvare i dati su AWS IoT Core e PostgreSQL.**  

---

## 📌 Funzionalità  
✅ Raccoglie dati da un sensore virtuale (simulato)  
✅ Invia i dati a **AWS IoT Core** via MQTT  
✅ Salva i dati su **PostgreSQL**  
✅ Visualizza i dati in tempo reale con una **dashboard**  
✅ Predice le temperature future con **Machine Learning**  

---

## 🛠️ Tecnologie utilizzate  
- **Python** (con `boto3`, `paho-mqtt`, `psycopg2`, `Flask`)  
- **AWS IoT Core** (per la gestione dei dati IoT)  
- **PostgreSQL** (per il database)  
- **Plotly** e **Dash** (per la visualizzazione dati)  

---

## 🚀 Setup e Installazione  

## **1️⃣ Clona la repository**  
- git clone https://github.com/TUO_USERNAME/IoT-Cloud-Monitor.git
- cd IoT-Cloud-Monitor

## **2️⃣ Crea un ambiente virtuale e attivalo**
- python3 -m venv iot_env
- source iot_env/bin/activate 

## **3️⃣ Installa le dipendenze**
- pip install -r requirements.txt

## **4️⃣ Configura le variabili di ambiente**

## 🎯 Avvia il simulatore IoT
- python iot_simulator.py

## 📊 Avvia la Dashboard
- python dashboard.py

## 🔮 Prevedere la temperatura futura
- python predict.py

