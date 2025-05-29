# 📈 Bitcoin Price Predictor App

This Streamlit app allows users to visualize and analyze Bitcoin price forecasts with upper and lower confidence intervals.

## 🔍 Features

- Upload your own forecast CSV file
- Visualize predictions using interactive Matplotlib charts
- Displays upper and lower confidence intervals
- Automatically uses default data if no file is uploaded

## 📁 Required CSV Columns

Your uploaded file must contain the following columns:

- `ds`: Dates (in YYYY-MM-DD format)
- `yhat`: Predicted price
- `yhat_lower`: Lower bound of prediction
- `yhat_upper`: Upper bound of prediction

If these columns are missing, the app will automatically revert to a default dataset.

## ▶️ Run the App Locally

```bash
pip install -r requirements.txt
streamlit run app.py
