import os
from flask import Flask, request, render_template_string, session
import re
import difflib
import json

app = Flask(__name__)
app.secret_key = 'aerofuel-assistant-secret-key'

qa_pairs = {
    r"what is aircraft refueling supervision": "Aircraft refueling supervision involves overseeing the safe and efficient refueling of aircraft. Supervisors ensure compliance with safety protocols, verify fuel types and quantities, and coordinate with ground crews to prevent accidents.",
    r"what does an aircraft refueling supervisor do": "An aircraft refueling supervisor monitors the refueling process, checks equipment, ensures proper grounding of the aircraft, verifies fuel quality, and maintains safety standards to prevent fires or explosions.",
    r"what are the safety procedures": "Safety procedures include grounding the aircraft, prohibiting smoking and open flames, wearing appropriate PPE, checking for fuel leaks, and ensuring proper ventilation. Supervisors must also be aware of weather conditions and emergency protocols.",
    r"what fuel is used": "Aircraft typically use Jet A or Jet A-1 fuel, which are kerosene-based. Supervisors must ensure the correct fuel type is used for the specific aircraft model.",
    r"how is refueling done": "Refueling is done through designated ports on the aircraft wings or fuselage. Supervisors oversee the connection of hoses, monitor fuel flow, and ensure the correct amount is dispensed without overfilling.",
    r"what qualifications are needed": "Qualifications include training in aviation safety, fuel handling, emergency response, and often certifications from aviation authorities. Experience in ground operations is beneficial.",
    r"what are common risks": "Common risks include fuel spills, electrostatic discharge, contamination, and human error. Supervisors mitigate these through strict adherence to procedures and regular equipment checks.",
    r"tell me about your profession": "As an aircraft refueling supervisor, my role is critical in aviation operations. I ensure that aircraft are safely fueled, maintaining the highest safety standards to protect lives and equipment.",
    r"what is the process": "The process involves pre-refueling checks, connecting fuel lines, monitoring the transfer, post-refueling inspections, and documentation. Everything is done under supervision to ensure accuracy and safety.",
    r"why is supervision important": "Supervision is important to prevent accidents, ensure regulatory compliance, and maintain operational efficiency. It protects the aircraft, crew, and ground personnel from hazards associated with fuel handling."
}

suggestions = [
    "What is aircraft refueling supervision?",
    "What does an aircraft refueling supervisor do?",
    "What are the safety procedures?",
    "What fuel is used?",
    "How is refueling done?",
    "What qualifications are needed?",
    "What are common risks?",
    "Tell me about your profession?",
    "What is the process?",
    "Why is supervision important?"
]

question_map = {question.lower(): response for question, response in zip(suggestions, qa_pairs.values())}


def get_response(user_input):
    user_input = user_input.lower().strip()
    for pattern, response in qa_pairs.items():
        if re.search(pattern, user_input):
            return response
    close_matches = difflib.get_close_matches(user_input, list(question_map.keys()), n=1, cutoff=0.5)
    if close_matches:
        return question_map[close_matches[0]]
    return "I'm sorry, I don't have information on that. Please try one of the suggestions or ask about aircraft refueling supervision."

@app.route('/', methods=['GET', 'POST'])
def chat():
    conversations = session.get('conversations', [])
    current_conv = session.get('current_conv', 0)

    if request.method == 'POST':
        if request.form.get('clear_history'):
            conversations = []
            current_conv = 0
        elif request.form.get('view_conv') is not None:
            try:
                current_conv = int(request.form.get('view_conv'))
            except ValueError:
                pass
        else:
            user_input = request.form.get('question', '').strip()
            if user_input:
                response = get_response(user_input)
                if current_conv >= len(conversations):
                    conversations.append([])
                conversations[current_conv].append({'role': 'user', 'text': user_input})
                conversations[current_conv].append({'role': 'assistant', 'text': response})

    if current_conv >= len(conversations):
        current_messages = []
    else:
        current_messages = conversations[current_conv]

    session['conversations'] = conversations
    session['current_conv'] = current_conv

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AeroFuel Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: radial-gradient(circle at top left, #162d53, transparent 35%),
                            radial-gradient(circle at bottom right, #0a1c35, transparent 30%),
                            linear-gradient(135deg, #06101f 0%, #11233b 55%, #162c45 100%);
                color: #eef4ff;
                padding: 20px;
            }
            .container {
                width: 100%;
                max-width: 1400px;
                height: 90vh;
                background: rgba(12, 20, 38, 0.96);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 32px;
                box-shadow: 0 28px 80px rgba(0, 0, 0, 0.30);
                display: grid;
                grid-template-columns: 1fr 380px;
                overflow: hidden;
            }
            .left-panel {
                display: flex;
                flex-direction: column;
                gap: 24px;
                padding: 36px;
                overflow-y: auto;
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }
            .hero {
                display: grid;
                gap: 12px;
            }
            h1 {
                font-size: 2.7rem;
                letter-spacing: 0.04em;
            }
            p.subtitle {
                color: #a8c8ff;
                font-size: 0.95rem;
                line-height: 1.6;
            }
            .conversation-display {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 14px;
                overflow-y: auto;
                padding-right: 6px;
                min-height: 220px;
            }
            .message {
                padding: 18px 20px;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.10);
                background: rgba(255, 255, 255, 0.04);
                animation: popIn 0.2s ease;
            }
            .message.user {
                background: rgba(33, 84, 162, 0.18);
                border-color: rgba(74, 140, 255, 0.2);
            }
            .message.assistant {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(255, 255, 255, 0.14);
            }
            .message .role {
                display: block;
                margin-bottom: 10px;
                font-size: 0.75rem;
                color: #b7cdff;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                font-weight: 700;
            }
            .message p {
                margin: 0;
                line-height: 1.65;
                color: #f0f6ff;
                font-size: 0.95rem;
            }
            .input-section {
                display: grid;
                gap: 12px;
            }
            .input-group {
                display: grid;
                grid-template-columns: 1fr auto auto;
                gap: 10px;
            }
            input[type="text"] {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                background: rgba(255, 255, 255, 0.05);
                color: #eef4ff;
                font-size: 0.95rem;
                outline: none;
            }
            input[type="text"]:focus {
                border-color: #5da7ff;
                box-shadow: 0 0 0 3px rgba(93, 167, 255, 0.12);
            }
            input[type="submit"], .btn {
                padding: 0 24px;
                border-radius: 16px;
                border: none;
                background: linear-gradient(135deg, #4a8cff, #1f6dff);
                color: white;
                font-weight: 700;
                cursor: pointer;
                transition: transform 0.2s ease;
                height: 48px;
                font-size: 0.95rem;
            }
            input[type="submit"]:hover, .btn:hover {
                transform: translateY(-2px);
            }
            .mic-btn {
                width: 48px;
                height: 48px;
                padding: 0;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 16px;
                background: linear-gradient(135deg, #ff6b6b, #ff3b3b);
                box-shadow: none;
            }
            .mic-btn.active {
                box-shadow: 0 6px 18px rgba(255, 59, 59, 0.28);
                transform: translateY(-2px) scale(1.02);
            }
            .suggestions {
                position: relative;
            }
            .suggestion-box {
                position: absolute;
                top: calc(100% + 8px);
                left: 0;
                right: 0;
                background: rgba(4, 14, 34, 0.98);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 18px 35px rgba(0, 0, 0, 0.3);
                z-index: 5;
            }
            .suggestion-item {
                padding: 14px 16px;
                cursor: pointer;
                color: #d8e7ff;
                font-size: 0.95rem;
                transition: background 0.2s ease;
            }
            .suggestion-item:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            .right-panel {
                display: flex;
                flex-direction: column;
                gap: 16px;
                padding: 22px;
                overflow: hidden;
                background: rgba(0, 0, 0, 0.28);
            }
            .history-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            .history-header h2 {
                font-size: 1.1rem;
                color: #eef4ff;
            }
            .clear-btn {
                padding: 0 14px;
                height: 36px;
                border-radius: 14px;
                border: none;
                background: rgba(255,255,255,0.08);
                color: #eef4ff;
                font-size: 0.84rem;
                cursor: pointer;
            }
            .clear-btn:hover {
                background: rgba(255,255,255,0.12);
            }
            .conversations-list {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 10px;
                overflow-y: auto;
                padding-right: 4px;
            }
            .conversation-item {
                width: 100%;
                padding: 14px 16px;
                text-align: left;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                background: rgba(255, 255, 255, 0.05);
                color: #d8e7ff;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            .conversation-item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            .conversation-item.active {
                background: rgba(74, 140, 255, 0.22);
                border-color: rgba(74, 140, 255, 0.3);
                color: #fff;
            }
            .conversation-title {
                font-weight: 700;
                margin-bottom: 6px;
            }
            .conversation-snippet {
                opacity: 0.85;
            }
            .empty-state {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                text-align: center;
                color: #7a92b8;
                font-size: 0.95rem;
                padding: 20px;
            }
            @media (max-width: 960px) {
                .container { grid-template-columns: 1fr; height: auto; }
                .left-panel { border-right: none; border-bottom: 1px solid rgba(255,255,255,0.08); }
                .right-panel { border-left: none; padding-left: 20px; padding-top: 24px; }
            }
            @keyframes popIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="left-panel">
                <div class="hero">
                    <h1>AeroFuel Assistant</h1>
                    <p class="subtitle">Ask a single question at a time and view your chat below.</p>
                </div>
                <div class="conversation-display">
                    {% if current_messages %}
                        {% for message in current_messages %}
                            <div class="message {{ message.role }}">
                                <span class="role">{{ 'You' if message.role == 'user' else 'Assistant' }}</span>
                                <p>{{ message.text }}</p>
                            </div>
                        {% endfor %}
                    {% else %}
                        <div class="empty-state">
                            <p>Start a new conversation by asking a question.</p>
                        </div>
                    {% endif %}
                </div>
                <div class="input-section">
                    <form method="post" autocomplete="off">
                        <div class="input-group suggestions">
                                    <input id="question-input" type="text" name="question" placeholder="Type your question here..." required autofocus autocomplete="off">
                                    <div id="suggestion-box" class="suggestion-box" style="display:none;"></div>
                                    <button type="button" id="voice-btn" class="btn mic-btn" title="Voice input (English)">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3z" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M19 11v1a7 7 0 0 1-14 0v-1" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M12 19v3" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </button>
                                    <input type="submit" value="Send">
                                </div>
                    </form>
                </div>
            </div>
            <div class="right-panel">
                <div class="history-header">
                    <h2>Chat History</h2>
                    {% if conversations %}
                        <form method="post" style="margin:0;">
                            <button type="submit" name="clear_history" value="1" class="clear-btn">Clear All</button>
                        </form>
                    {% endif %}
                </div>
                {% if conversations %}
                    <div class="conversations-list">
                        {% for idx, conv in conversations %}
                            <form method="post" style="width:100%; margin:0;">
                                <button type="submit" name="view_conv" value="{{ idx }}" class="conversation-item {% if idx == current_idx %}active{% endif %}">
                                    <div class="conversation-title">Conversation {{ idx + 1 }}</div>
                                    <div class="conversation-snippet">{{ conv[0].text[:50] }}{% if conv[0].text|length > 50 %}...{% endif %}</div>
                                </button>
                            </form>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="empty-state">
                        <p>No saved conversations yet.<br>Ask a question to begin.</p>
                    </div>
                {% endif %}
            </div>
        </div>
        <script>
            // Ensure suggestions is an array (handle stringified JSON or direct array)
            let __s = {{ suggestions_json | safe }};
            if (typeof __s === 'string') {
                try { __s = JSON.parse(__s); } catch(e) { __s = []; }
            }
            const suggestions = Array.isArray(__s) ? __s : [];
            const input = document.getElementById('question-input');
            const box = document.getElementById('suggestion-box');

            function updateSuggestions(value) {
                const query = value.trim().toLowerCase();
                if (!query) {
                    box.style.display = 'none';
                    box.innerHTML = '';
                    return;
                }
                const filtered = suggestions.filter(item => item.toLowerCase().includes(query)).slice(0, 4);
                if (!filtered.length) {
                    box.style.display = 'none';
                    box.innerHTML = '';
                    return;
                }
                box.innerHTML = filtered.map(item => `<div class="suggestion-item">${item}</div>`).join('');
                box.style.display = 'block';
                document.querySelectorAll('.suggestion-item').forEach(el => {
                    el.addEventListener('click', () => {
                        input.value = el.textContent;
                        box.style.display = 'none';
                        input.focus();
                    });
                });
            }

            input.addEventListener('input', (event) => updateSuggestions(event.target.value));
            input.addEventListener('focus', (event) => updateSuggestions(event.target.value));
            document.addEventListener('click', (event) => {
                if (!event.target.closest('.suggestions')) {
                    box.style.display = 'none';
                }
            });
            // Voice input (Web Speech API) - toggles recognition and fills the input
            const voiceBtn = document.getElementById('voice-btn');
            if (voiceBtn) {
                try {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    if (SpeechRecognition) {
                        const recognition = new SpeechRecognition();
                        recognition.lang = 'en-US';
                        recognition.interimResults = false;
                        recognition.maxAlternatives = 1;

                        recognition.addEventListener('start', () => {
                            voiceBtn.classList.add('active');
                            voiceBtn.title = 'Listening... click to stop';
                        });
                        recognition.addEventListener('end', () => {
                            voiceBtn.classList.remove('active');
                            voiceBtn.title = 'Voice input (English)';
                        });
                        recognition.addEventListener('result', (e) => {
                            const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
                            input.value = transcript;
                            updateSuggestions(transcript);
                            input.focus();
                        });

                        let listening = false;
                        voiceBtn.addEventListener('click', () => {
                            if (listening) {
                                recognition.stop();
                                listening = false;
                            } else {
                                try { recognition.start(); listening = true; } catch(err) { console.warn(err); }
                            }
                        });
                    } else {
                        voiceBtn.disabled = true;
                        voiceBtn.title = 'Voice input not supported in this browser';
                        voiceBtn.style.opacity = 0.6;
                    }
                } catch (e) {
                    console.warn('Speech recognition setup failed', e);
                    voiceBtn.disabled = true;
                    voiceBtn.style.opacity = 0.6;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, current_messages=current_messages, conversations=list(enumerate(conversations)), current_idx=current_conv, suggestions_json=json.dumps(suggestions))

if __name__ == '__main__'
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
