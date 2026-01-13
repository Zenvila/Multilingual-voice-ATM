/**
 * Multilingual ATM - Main JavaScript
 * Handles UI interactions, API calls, and voice assistant integration
 */

// Global state
let currentLanguage = 'en';
let voiceAssistantActive = false;
let currentStep = 1;
let currentAction = null;
let openaiClient = null;

// DOM Elements
const helpBtn = document.getElementById('helpBtn');
const languageModal = document.getElementById('languageModal');
const closeModal = document.getElementById('closeModal');
const langButtons = document.querySelectorAll('.lang-btn');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const withdrawBtn = document.getElementById('withdrawBtn');
const balanceBtn = document.getElementById('balanceBtn');
const confirmWithdrawBtn = document.getElementById('confirmWithdrawBtn');
const cancelWithdrawBtn = document.getElementById('cancelWithdrawBtn');
const backToActionsBtn = document.getElementById('backToActionsBtn');
const stopVoiceBtn = document.getElementById('stopVoiceBtn');
const voiceAssistantStatus = document.getElementById('voiceAssistantStatus');
const voiceInstruction = document.getElementById('voiceInstruction');
const statusMessage = document.getElementById('statusMessage');

// Sections
const loginSection = document.getElementById('loginSection');
const actionsSection = document.getElementById('actionsSection');
const withdrawSection = document.getElementById('withdrawSection');
const balanceSection = document.getElementById('balanceSection');

// Quick amount buttons
const quickAmountBtns = document.querySelectorAll('.quick-amount-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkForOpenAIKey();
});

function initializeEventListeners() {
    // Help button
    helpBtn.addEventListener('click', showLanguageModal);
    
    // Modal controls
    closeModal.addEventListener('click', hideLanguageModal);
    languageModal.addEventListener('click', (e) => {
        if (e.target === languageModal) {
            hideLanguageModal();
        }
    });
    
    // Language selection
    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            currentLanguage = btn.dataset.lang;
            hideLanguageModal();
            startVoiceAssistant();
        });
    });
    
    // Login
    loginBtn.addEventListener('click', handleLogin);
    
    // ATM Actions
    logoutBtn.addEventListener('click', handleLogout);
    withdrawBtn.addEventListener('click', async () => {
        if (voiceAssistantActive) {
            await speakInstruction('withdraw', 1);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        showWithdrawSection();
    });
    balanceBtn.addEventListener('click', handleCheckBalance);
    
    // Withdraw actions
    confirmWithdrawBtn.addEventListener('click', handleWithdraw);
    cancelWithdrawBtn.addEventListener('click', () => showActionsSection());
    
    // Balance actions
    backToActionsBtn.addEventListener('click', () => showActionsSection());
    
    // Quick amount buttons
    quickAmountBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('amount').value = btn.dataset.amount;
        });
    });
    
    // Stop voice
    stopVoiceBtn.addEventListener('click', stopVoiceAssistant);
    
    // Enter key support
    document.getElementById('accountNumber').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') document.getElementById('pin').focus();
    });
    
    document.getElementById('pin').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    
    document.getElementById('amount').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleWithdraw();
    });
}

function showLanguageModal() {
    languageModal.classList.add('show');
}

function hideLanguageModal() {
    languageModal.classList.remove('show');
}

function showStatusMessage(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    setTimeout(() => {
        statusMessage.textContent = '';
        statusMessage.className = 'status-message';
    }, 5000);
}

async function handleLogin() {
    const accountNumber = document.getElementById('accountNumber').value;
    const pin = document.getElementById('pin').value;
    
    if (!accountNumber || !pin) {
        showStatusMessage('Please enter account number and PIN', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/verify_pin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ account_number: accountNumber, pin: pin })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatusMessage('Login successful!', 'success');
            document.getElementById('accountNumber').value = '';
            document.getElementById('pin').value = '';
            showActionsSection();
            
            // If voice assistant is active, provide instruction
            if (voiceAssistantActive) {
                await speakInstruction('enter_pin', 2);
            }
        } else {
            showStatusMessage(data.message || 'Invalid credentials', 'error');
        }
    } catch (error) {
        showStatusMessage('Error connecting to server', 'error');
        console.error('Login error:', error);
    }
}

function showActionsSection() {
    loginSection.style.display = 'none';
    withdrawSection.style.display = 'none';
    balanceSection.style.display = 'none';
    actionsSection.style.display = 'block';
    currentAction = null;
    currentStep = 1;
    
    // Speak action selection instructions if voice assistant is active
    if (voiceAssistantActive) {
        speakInstruction('select_action', 1);
    }
}

function showWithdrawSection() {
    actionsSection.style.display = 'none';
    withdrawSection.style.display = 'block';
    currentAction = 'withdraw';
    currentStep = 1;
    
    // Focus on amount input
    setTimeout(() => {
        document.getElementById('amount').focus();
    }, 500);
}

async function handleCheckBalance() {
    try {
        // Speak instruction when button is clicked
        if (voiceAssistantActive) {
            await speakInstruction('check_balance', 1);
        }
        
        const response = await fetch('/api/check_balance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            actionsSection.style.display = 'none';
            balanceSection.style.display = 'block';
            document.getElementById('balanceAmount').textContent = `Rs. ${data.balance.toLocaleString('en-PK', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            
            if (voiceAssistantActive) {
                await new Promise(resolve => setTimeout(resolve, 3000));
                await speakInstruction('check_balance', 2);
            }
        } else {
            showStatusMessage(data.message || 'Error checking balance', 'error');
        }
    } catch (error) {
        showStatusMessage('Error connecting to server', 'error');
        console.error('Balance check error:', error);
    }
}

async function handleWithdraw() {
    const amount = parseFloat(document.getElementById('amount').value);
    
    if (!amount || amount <= 0) {
        showStatusMessage('Please enter a valid amount', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/withdraw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: amount })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatusMessage(data.message, 'success');
            document.getElementById('amount').value = '';
            
            if (voiceAssistantActive) {
                await speakInstruction('withdraw', 3);
                await new Promise(resolve => setTimeout(resolve, 2000));
                await speakInstruction('withdraw', 4);
            }
            
            setTimeout(() => {
                showActionsSection();
            }, 3000);
        } else {
            showStatusMessage(data.message || 'Withdrawal failed', 'error');
        }
    } catch (error) {
        showStatusMessage('Error connecting to server', 'error');
        console.error('Withdraw error:', error);
    }
}

async function handleLogout() {
    try {
        await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        showActionsSection();
        loginSection.style.display = 'block';
        actionsSection.style.display = 'none';
        showStatusMessage('Logged out successfully', 'info');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Voice Assistant Functions
async function checkForOpenAIKey() {
    // Check if OpenAI is available on backend
    try {
        const response = await fetch('/api/get_voice_instructions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'enter_pin',
                language: 'en',
                step: 1
            })
        });
        const data = await response.json();
        if (data.source === 'openai') {
            console.log('OpenAI API is available and active');
            return true;
        }
    } catch (error) {
        console.log('OpenAI API not available, using fallback');
    }
    return false;
}

async function startVoiceAssistant() {
    voiceAssistantActive = true;
    voiceAssistantStatus.style.display = 'block';
    
    // Check if OpenAI is available
    const hasOpenAI = await checkForOpenAIKey();
    const assistantType = hasOpenAI ? 'OpenAI' : 'Browser';
    
    showStatusMessage(
        `${assistantType} Voice Assistant activated in ${getLanguageName(currentLanguage)}`, 
        'success'
    );
    
    // Start conversational flow
    await startConversationalFlow();
}

async function startConversationalFlow() {
    // Step 1: Welcome message
    await speakInstruction('welcome', 1);
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Step 2: Ask for account number
    await speakInstruction('enter_account', 1);
    
    // Focus on account number input and wait for user
    document.getElementById('accountNumber').focus();
    
    // Listen for account number entry
    const accountInput = document.getElementById('accountNumber');
    const checkAccount = async () => {
        if (accountInput.value.length >= 10) {
            // Verify account
            await verifyAccountNumber(accountInput.value);
        } else {
            setTimeout(checkAccount, 500);
        }
    };
    checkAccount();
}

async function verifyAccountNumber(accountNumber) {
    try {
        const response = await fetch('/api/verify_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ account_number: accountNumber })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await speakInstruction('account_verified', 1);
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Ask for PIN
            await speakInstruction('enter_pin', 1);
            document.getElementById('pin').focus();
            
            // Listen for PIN entry
            const pinInput = document.getElementById('pin');
            const checkPin = async () => {
                if (pinInput.value.length >= 4) {
                    await verifyPIN(accountNumber, pinInput.value);
                } else {
                    setTimeout(checkPin, 500);
                }
            };
            checkPin();
        } else {
            await speakInstruction('account_invalid', 1);
            document.getElementById('accountNumber').value = '';
            document.getElementById('accountNumber').focus();
            // Restart flow
            setTimeout(() => startConversationalFlow(), 3000);
        }
    } catch (error) {
        console.error('Account verification error:', error);
    }
}

async function verifyPIN(accountNumber, pin) {
    try {
        const response = await fetch('/api/verify_pin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ account_number: accountNumber, pin: pin })
        });
        
        const data = await response.json();
        
        if (data.success) {
            await speakInstruction('pin_verified', 1);
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Show actions and guide user
            showActionsSection();
            await speakInstruction('select_action', 1);
        } else {
            await speakInstruction('pin_invalid', 1);
            document.getElementById('pin').value = '';
            document.getElementById('pin').focus();
            // Wait and ask for PIN again
            setTimeout(async () => {
                await speakInstruction('enter_pin', 1);
            }, 2000);
        }
    } catch (error) {
        console.error('PIN verification error:', error);
    }
}

function stopVoiceAssistant() {
    voiceAssistantActive = false;
    voiceAssistantStatus.style.display = 'none';
    voiceInstruction.textContent = '';
    showStatusMessage('Voice Assistant stopped', 'info');
}

async function speakInstruction(action, step, context = {}) {
    try {
        // Get instruction from backend (OpenAI or fallback)
        const response = await fetch('/api/get_voice_instructions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: action,
                language: currentLanguage,
                step: step,
                context: context
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.instruction) {
            // Display instruction text
            voiceInstruction.textContent = data.instruction;
            
            // Try OpenAI TTS first if available
            if (data.source === 'openai') {
                try {
                    await speakWithOpenAI(data.instruction);
                    return data.instruction;
                } catch (error) {
                    console.log('OpenAI TTS failed, falling back to browser TTS:', error);
                }
            }
            
            // Fallback to browser's speech synthesis API
            await speakWithBrowserTTS(data.instruction);
            return data.instruction;
        }
    } catch (error) {
        console.error('Error getting voice instruction:', error);
    }
}

async function speakWithOpenAI(text) {
    try {
        const response = await fetch('/api/generate_voice_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: currentLanguage
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.audio_base64) {
            // Create audio element and play
            const audio = new Audio(`data:audio/${data.format};base64,${data.audio_base64}`);
            await new Promise((resolve, reject) => {
                audio.onended = resolve;
                audio.onerror = reject;
                audio.play();
            });
        } else {
            throw new Error('Failed to generate audio');
        }
    } catch (error) {
        console.error('OpenAI TTS error:', error);
        throw error;
    }
}

function getLanguageName(code) {
    const names = {
        'en': 'English',
        'ur': 'Urdu',
        'pa': 'Punjabi',
        'ps': 'Pashto',
        'sd': 'Sindhi',
        'ar': 'Arabic'
    };
    return names[code] || 'English';
}

// Speak all steps sequentially
async function speakAllSteps(action) {
    try {
        // Get all steps at once
        const response = await fetch('/api/get_voice_instructions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: action,
                language: currentLanguage,
                get_all: true
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.instructions && data.instructions.length > 0) {
            // Speak each step with a delay between them
            for (let i = 0; i < data.instructions.length; i++) {
                const instruction = data.instructions[i];
                voiceInstruction.textContent = `Step ${i + 1} of ${data.instructions.length}: ${instruction}`;
                
                // Try OpenAI TTS first if available, otherwise use browser TTS
                try {
                    await speakWithOpenAI(instruction);
                } catch (error) {
                    // Fallback to browser TTS
                    await speakWithBrowserTTS(instruction);
                }
                
                // Wait before next step (except for last step)
                if (i < data.instructions.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 2500));
                }
            }
        } else {
            // Fallback: speak steps one by one
            let step = 1;
            while (true) {
                const instruction = await speakInstruction(action, step);
                if (!instruction || instruction === "Please proceed with the next step.") {
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 2500));
                step++;
            }
        }
    } catch (error) {
        console.error('Error speaking all steps:', error);
    }
}

async function speakWithBrowserTTS(text) {
    return new Promise((resolve, reject) => {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            
            const langMap = {
                'en': 'en-US',
                'ur': 'ur-PK',
                'pa': 'ur-PK',  // Pakistani Punjabi uses Urdu script
                'ps': 'ps-AF',
                'sd': 'sd-PK',
                'ar': 'ar-SA'
            };
            
            utterance.lang = langMap[currentLanguage] || 'en-US';
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            utterance.onend = resolve;
            utterance.onerror = reject;
            
            window.speechSynthesis.speak(utterance);
        } else {
            resolve();
        }
    });
}

// Auto-advance steps for voice assistant (legacy function)
function advanceStep() {
    if (voiceAssistantActive && currentAction) {
        currentStep++;
        speakInstruction(currentAction, currentStep);
    }
}
