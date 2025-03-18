from flask import Flask, render_template
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Carica le credenziali dal file .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Crea la stringa di connessione SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

app = Flask(__name__)

def get_data():
    """Recupera i dati dal database PostgreSQL"""
    query = "SELECT timestamp, temperature FROM temperature_data ORDER BY timestamp DESC LIMIT 100;"
    df = pd.read_sql(query, engine)  # Usa SQLAlchemy per gestire la connessione
    return df

@app.route('/')
def index():
    df = get_data()
    
    if df.empty:
        return "<h1>❌ Nessun dato disponibile nel database!</h1>"

    df = df.sort_values('timestamp')  # Ordina i dati per tempo

    # Creazione del grafico con linee spigolose (a gradini)
    fig = px.line(df, x='timestamp', y='temperature', title='Temperatura nel tempo', 
                  line_shape='hv')  # 'hv' = Horizontal-Vertical (grafico a scalini)

    graph_html = fig.to_html(full_html=False)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
