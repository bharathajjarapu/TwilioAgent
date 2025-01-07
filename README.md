# TwilioAgent
Whatsapp AI Agent

## Overview

TwilioAgent is a Flask-based web application that integrates with Twilio and Groq to create an AI-powered WhatsApp assistant. This assistant provides clear, concise, and accurate responses to user messages, maintaining a conversational tone.

## Features

- Responds to incoming WhatsApp messages using AI.
- Maintains conversation history for context-aware responses.
- Provides a manual endpoint to send WhatsApp messages.

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/bharathajjarapu/TwilioAgent.git
    cd TwilioAgent
    ```

2. **Create a `.env` file**:
    ```sh
    touch .env
    ```
    Add the following environment variables to the `.env` file:
    ```
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    GROQ_API_KEY=your_groq_api_key
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Flask app**:
    ```sh
    python app.py
    ```

## Usage

### Webhook Endpoint

The `/webhook` endpoint handles incoming WhatsApp messages. When a message is received, the app retrieves the message details, gets a response from the AI, and sends the AI's response back to the user.

### Send Endpoint

The `/send` endpoint allows manual sending of WhatsApp messages. It expects a JSON payload with `to` and `message` fields.

Example:
```sh
curl -X POST http://localhost:5000/send -H "Content-Type: application/json" -d '{"to": "+1234567890", "message": "Hello, World!"}'
```

## Code Explanation

### app.py

- **Environment Setup**: Loads environment variables using `load_dotenv()`.
- **Twilio and Groq Clients**: Initializes Twilio and Groq clients using API keys from the environment.
- **Constants and Variables**: Sets up constants like `TWILIO_WHATSAPP_NUMBER` and a `message_history` dictionary.
- **Functions**:
  - `get_ai_response(user_message, phone_number)`: Sends the user's message to the Groq AI model and retrieves a response.
  - `send_whatsapp_message(to_number, message_body)`: Sends a WhatsApp message using the Twilio client.
- **Flask Routes**:
  - `/webhook`: Handles incoming WhatsApp messages and sends an AI response back.
  - `/send`: Allows manual sending of WhatsApp messages.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any questions or suggestions, feel free to open an issue.
