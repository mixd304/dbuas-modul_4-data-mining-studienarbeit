import os
import pandas as pd
import numpy as np
import sqlite3
from prophet import Prophet

FILEPATH_TRAIN = os.path.join("input", "train.csv")
FILEPATH_STORE = os.path.join("input", "store.csv")
FILEPATH_TEST = os.path.join("input", "test.csv")

IMG_PATH = os.path.join("output", "images")

if not os.path.exists(IMG_PATH):
    os.makedirs(IMG_PATH)

df_train = pd.read_csv(FILEPATH_TRAIN, low_memory=False)
df_store = pd.read_csv(FILEPATH_STORE)
df_test = pd.read_csv(FILEPATH_TEST, low_memory=False)

df_train_store = pd.merge(df_train, df_store, on="Store", how="inner")

# Initialisieren ein leeren DataFrames, um den Forecast für alle Stores zu speichern
prophet_all_forecasts = pd.DataFrame()

# Da es insgesamt 1115 Stores gibt und der Forecast für alle Stores sehr lange dauern würde, wird der Forecast für 10 Stores je Storetype durchgeführt
for store_type in df_train_store.StoreType.unique():
    stores = df_train_store[df_train_store.StoreType == store_type].Store.unique()[:10]

    for store in stores:

        sales = df_train_store[df_train_store.Store == store].loc[:, ['Date', 'Sales']]
        sales.sort_values(by='Date', inplace=True)
        sales.reset_index(drop=True, inplace=True)
        sales['Date'] = pd.DatetimeIndex(sales['Date'])
        sales = sales.rename(columns={'Date': 'ds', 'Sales': 'y'})

        m = Prophet()
        m.fit(sales)
        future = m.make_future_dataframe(periods=6*7, freq='D')
        forecast = m.predict(future)

        # Store-Informationen zum Forecast-Dataframe hinzufügen
        forecast['store'] = store
        forecast['store_type'] = store_type

        # Anhängen des Forecasts für den aktuellen Store an das all_forecasts-DataFrame
        prophet_all_forecasts = pd.concat([prophet_all_forecasts, forecast])

# Verbindung zur Datenbank herstellen - wenn die Datenbank nicht existiert, wird sie automatisch erstellt
conn = sqlite3.connect('output/rossmann-store-sales-2.db')

# Cursor erstellen
c = conn.cursor()

# Tabelle erstellen, falls sie nicht bereits existiert
c.execute('''CREATE TABLE IF NOT EXISTS sales_forecast_prophet
             (id INTEGER PRIMARY KEY,
              store INTEGER,
              store_type TEXT,
              date TEXT,
              yhat REAL,
              yhat_lower REAL,
              yhat_upper REAL
              )''')

# Tabelle leeren, falls sie bereits existiert und Daten enthält
c.execute('''delete from sales_forecast_prophet''')

prophet_all_forecasts = prophet_all_forecasts[[
    'store', 'store_type', 'ds', 'yhat', 'yhat_lower', 'yhat_upper']]

for row in prophet_all_forecasts.iterrows():
    store = row[1]['store']
    store_type = row[1]['store_type']
    ds = row[1]['ds'].strftime('%Y-%m-%d')
    yhat = row[1]['yhat']
    yhat_lower = row[1]['yhat_lower']
    yhat_upper = row[1]['yhat_upper']

    c.execute('''INSERT INTO sales_forecast_prophet (store, store_type, date, yhat, yhat_lower, yhat_upper)
                    VALUES (?, ?, ?, ?, ?, ?)''', (store, store_type, ds, yhat, yhat_lower, yhat_upper))

# Änderungen bestätigen
conn.commit()

# Verbindung schließen
conn.close()