import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Carica le credenziali
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Crea la stringa di connessione SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def get_data():
    """Recupera i dati dal database PostgreSQL usando SQLAlchemy"""
    query = "SELECT timestamp, temperature FROM temperature_data ORDER BY timestamp DESC LIMIT 100;"
    df = pd.read_sql(query, engine)  # Usa SQLAlchemy per gestire la connessione
    return df

def predict_temperature():
    df = get_data()
    
    if df.empty:
        print("❌ Nessun dato disponibile per la previsione!")
        return

    df = df.sort_values('timestamp')  # Ordina i dati per tempo
    df['timestamp'] = pd.to_datetime(df['timestamp']).astype(int) // 10**9  # Converti in secondi UNIX
    
    X = df[['timestamp']].values
    y = df['temperature'].values

    model = LinearRegression()
    model.fit(X, y)

    next_time = np.array([[X[-1][0] + 3600]])  # Previsione per 1 ora nel futuro
    predicted_temp = model.predict(next_time)

    print(f"📈 Temperatura prevista tra 1 ora: {predicted_temp[0]:.2f}°C")

if __name__ == '__main__':
    predict_temperature()
