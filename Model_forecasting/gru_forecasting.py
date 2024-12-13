import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping

# Set page configuration
st.set_page_config(page_title="GRU Forecasting", layout="wide")

st.title("GRU Forecasting")
st.write("This page performs GRU-based forecasting with batch size optimization.")

# Load default data
try:
    # Load fact_sales and dim_date
    fact_sales = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\factSales.csv")
    dim_date = pd.read_csv(r"C:\Users\ADMIN\.ssh\dvdrental\dimDate.csv")

    # Preprocess data
    dim_date['date'] = pd.to_datetime(dim_date['date'])
    sales_data = fact_sales.merge(dim_date, on='date_id')
    sales_data['date'] = pd.to_datetime(sales_data['date'])

    # Aggregate sales data by week
    weekly_sales = sales_data.copy()
    weekly_sales['week'] = sales_data['date'].dt.to_period('W')
    weekly_sales = weekly_sales.groupby('week')['sales_amount'].sum().reset_index()
    weekly_sales['week'] = weekly_sales['week'].dt.to_timestamp()

    # Handle missing or invalid values
    if weekly_sales['sales_amount'].isnull().any():
        st.warning("Missing values found in 'sales_amount'. Replacing with 0.")
        weekly_sales['sales_amount'].fillna(0, inplace=True)

    st.success("Default files loaded successfully.")
    
except Exception as e:
    st.error(f"Error loading default files: {e}")
    st.stop()

# Prepare data for GRU
st.write("Preparing data for GRU model...")
data = weekly_sales[['week', 'sales_amount']].copy()
data.set_index('week', inplace=True)

# Normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# Function to create sequences
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length, 0])
        y.append(data[i + sequence_length, 0])
    return np.array(X), np.array(y)

sequence_length = 4
X, y = create_sequences(data_scaled, sequence_length)

# Reshape data for GRU
X = X.reshape(X.shape[0], X.shape[1], 1)

# Split into training and testing sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Train GRU model with batch size optimization
def train_gru_model(X_train, y_train, X_test, y_test, batch_size):
    model = Sequential()
    model.add(GRU(units=64, activation='tanh', return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(GRU(units=32, activation='tanh', return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping],
        verbose=0
    )
    return model, history

st.write("Optimizing batch size...")
batch_sizes = [16, 32, 64, 128]
results = []

for batch_size in batch_sizes:
    model, history = train_gru_model(X_train, y_train, X_test, y_test, batch_size)
    val_loss = min(history.history['val_loss'])
    results.append({'Batch Size': batch_size, 'Validation Loss': val_loss})

results_df = pd.DataFrame(results).sort_values(by='Validation Loss')
best_batch_size = int(results_df.iloc[0]['Batch Size'])

st.write("Batch size optimization results:")
st.dataframe(results_df)
st.write(f"Best batch size: {best_batch_size}")

# Train final model
st.write("Training final GRU model...")
model, history = train_gru_model(X_train, y_train, X_test, y_test, best_batch_size)

# Forecast future steps
future_steps = 12
future_data = data_scaled[-sequence_length:]
future_predictions = []
for _ in range(future_steps):
    future_pred = model.predict(future_data[np.newaxis, :, :])
    future_predictions.append(future_pred[0, 0])
    future_data = np.vstack([future_data[1:], future_pred])

future_predictions_original = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['sales_amount'], label='Actual', color='blue', marker='o')
plt.title('GRU Forecasting')

future_forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(weeks=1), periods=future_steps, freq='W')
plt.plot(future_forecast_index, future_predictions_original, label='Future Forecast', color='green', linestyle='--', marker='o')
plt.axvline(x=data.index[-1], color='orange', linestyle='--', label='Forecast Start')
plt.legend()
st.pyplot(plt)

# Display forecast results
forecast_results = pd.DataFrame({
    'Date': future_forecast_index,
    'Forecasted Sales': future_predictions_original.flatten()
})
st.write("Future Forecasted Sales:")
st.dataframe(forecast_results)