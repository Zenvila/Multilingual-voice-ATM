# Setup Guide - OpenAI API Integration

## Quick Setup

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy your API key (you'll only see it once!)

### Step 2: Configure the Application

1. Create a `.env` file in the project root directory
2. Add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### Step 3: Run the Application

```bash
python app.py
```

The application will automatically detect if OpenAI is configured and use it for voice instructions.

## How It Works

When you select a language and click Help:

1. **OpenAI GPT** generates step-by-step instructions in your selected language
2. **OpenAI TTS** converts the text to natural-sounding speech
3. Instructions are displayed on screen and spoken aloud
4. The assistant guides you through each step of the ATM operation

## Without OpenAI API

If you don't set up the OpenAI API key, the application will:
- Still work perfectly!
- Use predefined instructions in all 6 languages
- Use browser's built-in Text-to-Speech (may have limited language support)

## Testing

1. Start the application
2. Click the red "HELP" button
3. Select a language (e.g., Urdu, Arabic, Punjabi)
4. You should see "OpenAI Voice Assistant activated" message
5. The assistant will guide you through ATM operations in your selected language

## Troubleshooting

**Issue**: "OpenAI API not configured" message
- **Solution**: Make sure your `.env` file exists and contains `OPENAI_API_KEY=your_key`

**Issue**: API errors
- **Solution**: Check that your API key is valid and has credits

**Issue**: Voice not working
- **Solution**: The app will automatically fall back to browser TTS if OpenAI TTS fails
