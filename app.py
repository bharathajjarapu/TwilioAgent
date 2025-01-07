from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Twilio client
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Twilio WhatsApp number
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'

# Message history storage
message_history = {}

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are a helpful and friendly AI assistant on WhatsApp. 
You provide clear, concise, and accurate responses while maintaining a conversational tone. 
Keep responses brief and suitable for WhatsApp, ideally under 3-4 sentences unless more detail is specifically requested."""

def get_ai_response(user_message, phone_number):
    """Get response from Groq AI"""
    if phone_number not in message_history:
        message_history[phone_number] = []
    
    message_history[phone_number].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    recent_history = message_history[phone_number][-5:]
    messages.extend([{
        "role": msg["role"],
        "content": msg["content"]
    } for msg in recent_history])
    
    try:
        completion = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            top_p=0.9
        )
        
        ai_response = completion.choices[0].message.content
        
        message_history[phone_number].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return ai_response
    
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again later."

def send_whatsapp_message(to_number, message_body):
    """Send a WhatsApp message"""
    try:
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return True, message.sid
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False, str(e)

@app.route("/webhook", methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Get incoming message details
        incoming_msg = request.values.get('Body', '').strip()
        sender_phone = request.values.get('From', '')  # This includes 'whatsapp:' prefix
        
        print(f"Received message from {sender_phone}: {incoming_msg}")
        
        # Get AI response
        ai_response = get_ai_response(incoming_msg, sender_phone)
        
        # Create TwiML response
        resp = MessagingResponse()
        resp.message(ai_response)
        
        print(f"Sending response: {ai_response}")
        
        return str(resp)
    
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again.")
        return str(resp)

@app.route("/send", methods=['POST'])
def send():
    """Endpoint to manually send a message"""
    try:
        data = request.get_json()
        to_number = data.get('to')
        message = data.get('message')
        
        if not to_number or not message:
            return {"error": "Missing 'to' or 'message' in request"}, 400
        
        success, result = send_whatsapp_message(to_number, message)
        
        if success:
            return {"success": True, "message_sid": result}
        else:
            return {"success": False, "error": result}, 500
            
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True) 