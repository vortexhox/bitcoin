import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # For better date formatting

# Required columns
required_cols = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']

st.set_page_config(page_title="Bitcoin Forecast App", layout="wide")
st.title("📈 Bitcoin Price Predictor App")

# Function to load default dataset
@st.cache_data
def load_default_data():
    return pd.read_csv("bitcoin_forecast_2026_2027.csv")  # Replace with your default CSV path

# Load default data
default_df = load_default_data()

# File uploader
uploaded_file = st.file_uploader("bitcoin_forecast_2026_2027.csv", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if not all(col in df.columns for col in required_cols):
            st.error(f"Uploaded file must contain these columns: {required_cols}")
            st.write("Showing default dataset preview instead.")
            df = default_df
        else:
            st.success("Uploaded file loaded successfully!")
    except Exception as e:
        st.error(f"Error loading uploaded file: {e}")
        st.write("Showing default dataset preview instead.")
        df = default_df
else:
    st.info("No file uploaded. Showing default dataset preview.")
    df = default_df

# Convert 'ds' to datetime
df['ds'] = pd.to_datetime(df['ds'])

# ------------------------
# Forecast Summary Section
# ------------------------
st.write("### 📊 Forecast Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Max Predicted Price", f"${df['yhat'].max():,.2f}")
col2.metric("Min Predicted Price", f"${df['yhat'].min():,.2f}")
col3.metric("Avg Predicted Price", f"${df['yhat'].mean():,.2f}")

# ------------------------
# Date Range Slider (Optional)
# ------------------------
st.write("### 🗓️ Select Date Range to Visualize")
min_date = df['ds'].min().date()
max_date = df['ds'].max().date()
date_range = st.slider("Filter by date range", min_value=min_date, max_value=max_date, value=(min_date, max_date))

filtered_df = df[(df['ds'].dt.date >= date_range[0]) & (df['ds'].dt.date <= date_range[1])]

# ------------------------
# Data Table
# ------------------------
st.write("### 📋 Forecast Comparison Table")
st.dataframe(filtered_df)

# ------------------------
# Confidence Interval Toggle
# ------------------------
show_confidence = st.checkbox("Show Confidence Interval", value=True)

# ------------------------
# Forecast Plot
# ------------------------
st.write("### 📈 Forecast Plot")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['ds'], filtered_df['yhat'], label='Predicted Price', color='blue')

if show_confidence:
    ax.fill_between(filtered_df['ds'], filtered_df['yhat_lower'], filtered_df['yhat_upper'], 
                    color='gray', alpha=0.3, label='Confidence Interval')

ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.set_title("Bitcoin Price Forecast")
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()
st.pyplot(fig)

# ------------------------
# CSV Download Button
# ------------------------
st.write("### 📥 Download Forecast Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", csv, "filtered_forecast.csv", "text/csv")
