from flask import Blueprint, request, jsonify
from models.chatbot_model import generate_response

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/completion', methods=['POST'])
def chat_completion():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    response = generate_response(prompt)
    return jsonify({"response": response})

@chatbot_bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}
