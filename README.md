# Stock-Sathi
This is an industry-grade, end-to-end data analytics project combining real-time data collection, analysis, and visualization.
An end-to-end data analytics project that fetches real-time stock prices, visualizes price movements, and raises alerts if prices fluctuate beyond a certain threshold.

# Live: https://stock-sathi.streamlit.app/
## 🔧 Features
- Real-time stock price fetching (via yfinance)
- Interactive price chart (Plotly)
- Alert on significant price change
- Downloadable data as CSV

## 📂 Folder Structure
```
real_time_stock_analysis/
├── data/
│   └── stock_data.csv
├── scripts/
│   ├── fetch_data.py
│   ├── plot_graphs.py
│   └── alert.py
├── app/
│   └── dashboard.py
├── requirements.txt
└── README.md
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app/dashboard.py
```

## ✅ Output
- Real-time stock price chart
- Price change alerts
- CSV export button
