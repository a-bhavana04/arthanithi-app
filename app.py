from flask import Flask
from routes.financial_routes import financial_bp
from routes.stock_routes import stock_bp
from routes.chatbot_routes import chatbot_bp

app = Flask(__name__)

app.register_blueprint(financial_bp, url_prefix='/financial')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

@app.route('/')
def root():
    return {"message": "Unified Flask API is running!"}

if __name__ == '__main__':
    app.run(debug=True)
