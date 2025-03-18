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

- ## ⚠️ Prerequisiti
- Prima di eseguire questo progetto, assicurati di aver configurato:

    - AWS IoT Core: Creazione del "Thing", certificati e configurazione dell'endpoint
    - PostgreSQL: Creazione del database, dell'utente e della tabella per la raccolta dei dati
      
- Questi dettagli non sono inclusi in questo readme, ma sono necessari per il corretto funzionamento del progetto.

## 🚀 Setup e Installazione  

## 1️⃣ Crea un ambiente virtuale e attivalo
- python3 -m venv iot_env
- source iot_env/bin/activate 

## 2️⃣ Installa le dipendenze
- pip install -r requirements.txt

## 3️⃣ Configura le variabili di ambiente

## 🎯 Avvia il simulatore IoT
- python iot_simulator.py

## 📊 Avvia la Dashboard
- python dashboard.py

## 🔮 Prevedere la temperatura futura
- python predict.py




