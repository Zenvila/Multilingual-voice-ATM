# Multilingual Voice Assistant ATM - MVP

A Flask-based MVP that simulates a Multilingual Voice Assistant for ATM users, designed with simplicity and accessibility in mind.

## Features

- **Simple ATM UI** with large, clear buttons for easy navigation
- **Multilingual Support**: Urdu, English, Pakistani Punjabi (Shahmukhi script), Pashto, Sindhi, Arabic
- **Currency**: All amounts in Pakistani Rupees (PKR)
- **Voice Assistant**: Step-by-step voice guidance using OpenAI API (with browser TTS fallback)
- **Mock Banking Operations**: Withdraw cash, check balance
- **Secure Architecture**: Separated UI, Logic, and Data layers
- **Blockchain-style Transaction Logging**: Hashed transaction records with linked chains

## Project Structure

```
Multilingual_ATM/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── data_layer/
│   ├── __init__.py
│   └── database.py             # SQLite database layer
├── logic_layer/
│   ├── __init__.py
│   ├── atm_logic.py            # Business logic for ATM operations
│   └── transaction_logger.py   # Blockchain-style transaction logging
├── templates/
│   └── index.html              # Main ATM UI
├── static/
│   ├── css/
│   │   └── style.css           # Styling for UI
│   └── js/
│       └── main.js             # Frontend JavaScript
└── README.md
```

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API (Optional but Recommended)**:
   - Get your OpenAI API key from https://platform.openai.com/api-keys
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - If you don't set up OpenAI, the app will use fallback instructions (still works!)

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Sample Accounts

The application comes with pre-configured sample accounts for testing:

- **Account**: `1234567890`, **PIN**: `1234`, **Balance**: Rs. 100,000.00
- **Account**: `0987654321`, **PIN**: `5678`, **Balance**: Rs. 50,000.00

## Usage

1. **Normal ATM Usage**:
   - Enter account number and PIN
   - Select an action (Withdraw or Check Balance)
   - Complete the transaction

2. **Using Voice Assistant**:
   - Click the red **HELP** button (top right)
   - Select your preferred language
   - The voice assistant will guide you through each step
   - Instructions are provided both as text and voice

## Architecture

### Three-Layer Architecture

1. **UI Layer** (`templates/`, `static/`):
   - HTML/CSS/JavaScript frontend
   - User interface and interactions
   - Voice assistant integration

2. **Logic Layer** (`logic_layer/`):
   - Business logic for ATM operations
   - PIN verification
   - Transaction processing
   - Voice instruction generation

3. **Data Layer** (`data_layer/`):
   - SQLite database operations
   - Account management
   - Transaction storage
   - Blockchain-style hash chaining

### Security Features

- PIN hashing (SHA-256)
- Session-based authentication
- Transaction logging with linked hashes
- Separated concerns (UI doesn't handle sensitive data directly)

## Voice Assistant

The voice assistant uses **OpenAI API** to generate dynamic, context-aware instructions in the selected language. It uses OpenAI's GPT model to create natural, step-by-step guidance and OpenAI's TTS (Text-to-Speech) API for high-quality voice output.

**Features:**
- **OpenAI GPT Integration**: Generates instructions dynamically based on context and step
- **OpenAI TTS**: High-quality voice output in multiple languages
- **Fallback Mode**: If OpenAI API key is not set, uses predefined instructions with browser TTS
- **Language Support**: Works with all 6 supported languages (Urdu, English, Punjabi, Pashto, Sindhi, Arabic)

**How it works:**
1. User clicks Help button and selects a language
2. OpenAI generates step-by-step instructions in that language
3. Instructions are spoken using OpenAI TTS
4. User receives guidance for each step of the ATM operation

## Transaction Logging

Each transaction is logged with:
- Transaction type
- Amount (if applicable)
- Previous transaction hash (blockchain-style linking)
- Current transaction hash
- Timestamp
- Additional data

This creates an immutable chain of transactions that can be verified for integrity.

## Future Enhancements

- Integration with OpenAI Realtime Voice API for more natural conversations
- Real ATM hardware integration
- Additional languages
- Biometric authentication
- Receipt printing simulation
- Transaction history viewing

## Notes

- This is an MVP/demo application for demonstration purposes
- PIN hashing is simplified (use proper encryption in production)
- Database is SQLite (can be upgraded to PostgreSQL/MySQL)
- Voice assistant uses browser TTS (can be upgraded to OpenAI API)

# Multilingual Voice Assistant ATM - MVP
[![Research Paper](https://img.shields.io/badge/Preprint-ResearchGate-blue)](https://doi.org/10.13140/RG.2.2.32966.43841)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://multilingual-voice-atm-production.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)

> 🌐 **Live Demo:** https://multilingual-voice-atm-production.up.railway.app  
> 📄 **Research Paper:** https://doi.org/10.13140/RG.2.2.32966.43841


## License

This project is for educational and demonstration purposes.
