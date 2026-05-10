# Multilingual Voice Assistant ATM - MVP

[![Research Paper](https://img.shields.io/badge/Preprint-ResearchGate-blue)](https://doi.org/10.13140/RG.2.2.14223.14243)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://multilingual-voice-atm-production.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> 🌐 **Live Demo:** https://multilingual-voice-atm-production.up.railway.app
> 
> 📄 **Research Paper:** https://doi.org/10.13140/RG.2.2.14223.14243

A Flask-based MVP that simulates a Multilingual Voice Assistant for ATM users, designed with simplicity and accessibility in mind. Built to solve a real problem — out of Pakistan's 241.5 million people, around **165 million can't understand English**, creating a daily barrier to basic banking.

---

## Features

- **Simple ATM UI** with large, clear buttons for easy navigation
- **Multilingual Support**: Urdu, English, Pakistani Punjabi (Shahmukhi script), Pashto, Sindhi, Arabic
- **Currency**: All amounts in Pakistani Rupees (PKR)
- **Voice Assistant**: Step-by-step voice guidance using OpenAI API (with browser TTS fallback)
- **Mock Banking Operations**: Withdraw cash, check balance
- **Secure Architecture**: Separated UI, Logic, and Data layers
- **Blockchain-style Transaction Logging**: Hashed transaction records with linked chains

---

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

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Zenvila/Multilingual-voice-ATM.git
   cd Multilingual-voice-ATM
   ```

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

---

## Sample Accounts

| Account Number | PIN  | Balance        |
|----------------|------|----------------|
| 1234567890     | 1234 | Rs. 100,000.00 |
| 0987654321     | 5678 | Rs. 50,000.00  |

---

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

---

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

---

## Voice Assistant

The voice assistant uses **OpenAI API** to generate dynamic, context-aware instructions in the selected language.

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

---

## Transaction Logging

Each transaction is logged with:
- Transaction type
- Amount (if applicable)
- Previous transaction hash (blockchain-style linking)
- Current transaction hash
- Timestamp
- Additional data

This creates an immutable chain of transactions that can be verified for integrity.

---

## Future Enhancements

- Integration with OpenAI Realtime Voice API for more natural conversations
- Real ATM hardware integration
- Additional languages (Balochi, Brahui)
- Biometric authentication
- Receipt printing simulation
- Transaction history viewing
- Formal user study with target demographic

---

## Research

This project is accompanied by a published research paper:

**VoiceATM: A Multilingual Voice Assistant System for Bridging Language Barriers in Banking Accessibility**  
Haris Arain — ResearchGate Preprint, May 2026  
DOI: [10.13140/RG.2.2.14223.14243](https://doi.org/10.13140/RG.2.2.14223.14243)

---

## Notes

- This is an MVP/demo application for demonstration purposes
- PIN hashing is simplified (use proper encryption in production)
- Database is SQLite (can be upgraded to PostgreSQL/MySQL)
- Voice assistant uses browser TTS fallback when OpenAI key is not configured

---

## License

This project is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — you are free to share and adapt with attribution.
