"""
Multilingual Voice Assistant for ATM - Flask Application
Main entry point for the ATM simulation system.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

from data_layer.database import Database
from logic_layer.atm_logic import ATMLogic
from logic_layer.transaction_logger import TransactionLogger

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
CORS(app)

# Initialize layers
db = Database()
atm_logic = ATMLogic(db)
tx_logger = TransactionLogger(db)

# Initialize OpenAI client (if API key is available)
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = None
if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
    print("OpenAI API initialized successfully")
else:
    print("Warning: OPENAI_API_KEY not found. Using fallback instructions.")

@app.route('/')
def index():
    """Render the main ATM UI page."""
    return render_template('index.html')

@app.route('/api/verify_account', methods=['POST'])
def verify_account():
    """Verify if account number exists."""
    data = request.json
    account_number = data.get('account_number')
    
    if not account_number:
        return jsonify({'success': False, 'message': 'Account number required'}), 400
    
    exists = atm_logic.account_exists(account_number)
    
    if exists:
        session['account_number'] = account_number
        return jsonify({'success': True, 'message': 'Account verified'})
    else:
        return jsonify({'success': False, 'message': 'Account not found'}), 404

@app.route('/api/verify_pin', methods=['POST'])
def verify_pin():
    """
    Verify user PIN.
    Note: In production, this would use proper encryption and secure channels.
    """
    data = request.json
    account_number = session.get('account_number') or data.get('account_number')
    pin = data.get('pin')
    
    if not account_number or not pin:
        return jsonify({'success': False, 'message': 'Account number and PIN required'}), 400
    
    is_valid = atm_logic.verify_pin(account_number, pin)
    
    if is_valid:
        session['account_number'] = account_number
        session['authenticated'] = True
        return jsonify({'success': True, 'message': 'PIN verified'})
    else:
        return jsonify({'success': False, 'message': 'Invalid PIN'}), 401

@app.route('/api/check_balance', methods=['POST'])
def check_balance():
    """Check account balance for authenticated user."""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    account_number = session.get('account_number')
    balance = atm_logic.get_balance(account_number)
    
    if balance is not None:
        # Log transaction
        tx_logger.log_transaction(account_number, 'CHECK_BALANCE', {'balance': balance})
        return jsonify({'success': True, 'balance': balance})
    else:
        return jsonify({'success': False, 'message': 'Account not found'}), 404

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    """Process cash withdrawal for authenticated user."""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    amount = data.get('amount')
    
    if not amount or amount <= 0:
        return jsonify({'success': False, 'message': 'Invalid amount'}), 400
    
    account_number = session.get('account_number')
    result = atm_logic.withdraw(account_number, amount)
    
    if result['success']:
        # Log transaction with blockchain-style hashing
        tx_logger.log_transaction(account_number, 'WITHDRAW', {
            'amount': amount,
            'new_balance': result['new_balance']
        })
        return jsonify({
            'success': True,
            'message': f'Withdrawal successful. New balance: ${result["new_balance"]:.2f}',
            'new_balance': result['new_balance']
        })
    else:
        return jsonify({'success': False, 'message': result['message']}), 400

@app.route('/api/get_voice_instructions', methods=['POST'])
def get_voice_instructions():
    """
    Get step-by-step voice instructions for ATM actions using OpenAI API.
    Falls back to predefined instructions if OpenAI is not available.
    """
    data = request.json
    action = data.get('action')
    language = data.get('language', 'en')
    step = data.get('step', 1)
    context = data.get('context', {})  # Additional context about current state
    get_all = data.get('get_all', False)  # If True, return all steps
    
    # If get_all is True, return all steps
    if get_all:
        all_steps = atm_logic.get_all_steps(action, language)
        return jsonify({'success': True, 'instructions': all_steps, 'total_steps': len(all_steps)})
    
    # Try to use OpenAI API if available
    if openai_client:
        try:
            instruction = get_openai_instruction(action, language, step, context)
            return jsonify({'success': True, 'instruction': instruction, 'source': 'openai'})
        except Exception as e:
            print(f"OpenAI API error: {e}. Falling back to predefined instructions.")
    
    # Fallback to predefined instructions
    instructions = atm_logic.get_voice_instructions(action, language, step)
    return jsonify({'success': True, 'instruction': instructions, 'source': 'fallback'})

def get_openai_instruction(action, language, step, context):
    """
    Generate instruction using OpenAI API in the selected language.
    """
    language_names = {
        'en': 'English',
        'ur': 'Urdu',
        'pa': 'Punjabi',
        'ps': 'Pashto',
        'sd': 'Sindhi',
        'ar': 'Arabic'
    }
    
    # Update language name for Pakistani Punjabi
    if language == 'pa':
        lang_name = 'Pakistani Punjabi (written in Urdu script, not Hindi)'
    else:
        lang_name = language_names.get(language, 'English')
    
    # Build context message
    action_descriptions = {
        'withdraw': 'withdrawing cash from the ATM',
        'check_balance': 'checking account balance',
        'enter_pin': 'entering PIN to login'
    }
    
    action_desc = action_descriptions.get(action, 'using the ATM')
    
    # Create prompt for OpenAI
    system_prompt = f"""You are a helpful ATM voice assistant guiding an elderly user through ATM operations in Pakistan. 
You speak in {lang_name}. Be clear, simple, and encouraging. Keep instructions short (one sentence).
All amounts are in Pakistani Rupees (PKR)."""
    
    user_prompt = f"""The user is {action_desc}. This is step {step}. 
Provide a clear, simple instruction in {lang_name} for what they should do next. 
Be friendly and use simple language suitable for elderly users.
Only provide the instruction text, no explanations."""
    
    if context:
        user_prompt += f"\nContext: {context}"
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",  # Using cost-effective model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

@app.route('/api/generate_voice_audio', methods=['POST'])
def generate_voice_audio():
    """
    Generate audio using OpenAI TTS API for the given text in the selected language.
    Returns the audio URL or base64 data.
    """
    if not openai_client:
        return jsonify({'success': False, 'message': 'OpenAI API not configured'}), 503
    
    data = request.json
    text = data.get('text')
    language = data.get('language', 'en')
    
    if not text:
        return jsonify({'success': False, 'message': 'Text is required'}), 400
    
    try:
        # Map languages to OpenAI TTS voices
        voice_map = {
            'en': 'alloy',
            'ur': 'nova',  # OpenAI TTS supports multiple languages with same voices
            'pa': 'echo',
            'ps': 'fable',
            'sd': 'onyx',
            'ar': 'shimmer'
        }
        
        voice = voice_map.get(language, 'alloy')
        
        # Generate speech using OpenAI TTS
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=0.9  # Slightly slower for clarity
        )
        
        # Convert to base64 for frontend
        import base64
        audio_data = response.content
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio_base64': audio_base64,
            'format': 'mp3'
        })
        
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/get_transactions', methods=['GET'])
def get_transactions():
    """Get transaction history for authenticated user (for demonstration)."""
    if not session.get('authenticated'):
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    account_number = session.get('account_number')
    transactions = tx_logger.get_transactions(account_number)
    return jsonify({'success': True, 'transactions': transactions})

@app.route('/api/logout', methods=['POST'])
def logout():
    """Clear session and logout user."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})

if __name__ == '__main__':
    # Initialize database with sample data
    db.initialize_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
