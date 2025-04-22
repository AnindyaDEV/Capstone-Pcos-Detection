from flask import Blueprint, request, jsonify
from chatbot.engine import PCOSChatEngine

chatbot_bp = Blueprint('chatbot', __name__)
engine = PCOSChatEngine()

@chatbot_bp.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json
    user_id = data.get('user_id', 'default_user')
    message = data['message']
    
    # Get chatbot response
    response_data = engine.handle_message(user_id, message)
    
    # Ensure consistent response format
    return jsonify({
        'response': response_data.get('response', "I didn't understand that."),
        'options': response_data.get('options', []),
        'redirect': response_data.get('redirect')
    })