from flask import Blueprint, jsonify, Response, request
import pygsheets
import pandas as pd
import matplotlib.pyplot as plt
import io
from models.trading_model import load_model, StockTradingEnv

stock_bp = Blueprint('stock', __name__)

# Load model once
model = load_model()

@stock_bp.route('/predict', methods=['GET'])
def predict_stocks():
    client = pygsheets.authorize(service_file='stock-449613-7413d6080b00.json')
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/...').sheet1
    data = sheet.get_as_df()

    # Data processing and normalization
    env = StockTradingEnv(data)
    obs = env.reset()
    suggestions = []

    for _ in range(len(data)):
        action, _ = model.predict(obs)
        obs, _, done, _ = env.step(action)
        suggestion = "Buy" if action == 1 else "Sell" if action == 2 else "Hold"
        suggestions.append({"step": env.current_step, "suggestion": suggestion, "price": data['Price'].iloc[env.current_step]})
        if done:
            break

    return jsonify({"suggestions": suggestions})

@stock_bp.route('/graph/<stock_symbol>', methods=['GET'])
def generate_graph(stock_symbol):
    client = pygsheets.authorize(service_file='stock-449613-7413d6080b00.json')
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/...').sheet1
    data = sheet.get_as_df()
    stock_data = data[data['SYMBOL'] == stock_symbol]

    if stock_data.empty:
        return jsonify({"error": "Stock symbol not found"}), 404

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['Price'], label='Price', color='blue')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return Response(buf.read(), mimetype='image/png')
