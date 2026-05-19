import streamlit as st
import re
import difflib

st.set_page_config(page_title="AeroFuel Assistant", layout="wide")

# QA pairs database
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

suggestions_list = [
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

question_map = {q.lower(): resp for q, resp in zip(suggestions_list, qa_pairs.values())}

def get_response(user_input):
    """Get response using regex matching and fallback to fuzzy matching"""
    user_input = user_input.lower().strip()
    for pattern, response in qa_pairs.items():
        if re.search(pattern, user_input):
            return response
    close_matches = difflib.get_close_matches(user_input, list(question_map.keys()), n=1, cutoff=0.5)
    if close_matches:
        return question_map[close_matches[0]]
    return "I'm sorry, I don't have information on that. Please try one of the suggestions or ask about aircraft refueling supervision."

# Initialize session state
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "current_conv" not in st.session_state:
    st.session_state.current_conv = None

# Sidebar for chat history
with st.sidebar:
    st.markdown("### 📚 Chat History")
    
    if st.session_state.conversations:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.conversations = []
                st.session_state.current_conv = None
                st.rerun()
        
        st.divider()
        
        for idx, conv in enumerate(st.session_state.conversations):
            if conv:
                # Show first 50 chars of first message
                snippet = conv[0]["text"][:50] + ("..." if len(conv[0]["text"]) > 50 else "")
                if st.button(f"**Conv {idx + 1}**\n_{snippet}_", use_container_width=True, key=f"conv_{idx}"):
                    st.session_state.current_conv = idx
                    st.rerun()
    else:
        st.info("📭 No saved conversations yet.\nAsk a question to begin.")

# Main content area
st.markdown("# 🛩️ AeroFuel Assistant")
st.markdown("Ask a single question at a time and view your chat below.")

# Display current conversation
if st.session_state.current_conv is not None and st.session_state.current_conv < len(st.session_state.conversations):
    messages = st.session_state.conversations[st.session_state.current_conv]
    
    if messages:
        for msg in messages:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["text"])
            else:
                st.chat_message("assistant").write(msg["text"])
    else:
        st.info("Start a new conversation by asking a question.")
else:
    if st.session_state.conversations:
        st.info("Select a conversation from the sidebar to view.")
    else:
        st.info("👋 Start a new conversation by typing your question below.")

# Input section
st.divider()

col1, col2, col3 = st.columns([3, 0.5, 0.5])

with col1:
    user_input = st.text_input(
        "Your question:",
        placeholder="Type your question here...",
        label_visibility="collapsed"
    )

with col2:
    # Voice input button (simplified - would need st-audiorec package)
    st.markdown("🎤 Voice support available with `st-audiorec`")

with col3:
    send_btn = st.button("📤 Send", use_container_width=True)

# Process user input
if send_btn and user_input:
    # Start new conversation if needed
    if st.session_state.current_conv is None or st.session_state.current_conv >= len(st.session_state.conversations):
        st.session_state.conversations.append([])
        st.session_state.current_conv = len(st.session_state.conversations) - 1
    
    # Get response
    response = get_response(user_input)
    
    # Add messages to conversation
    st.session_state.conversations[st.session_state.current_conv].append({
        "role": "user",
        "text": user_input
    })
    st.session_state.conversations[st.session_state.current_conv].append({
        "role": "assistant",
        "text": response
    })
    
    st.rerun()

# Display suggestions
st.divider()
st.markdown("### 💡 Common Questions")
cols = st.columns(2)
for idx, suggestion in enumerate(suggestions_list[:4]):
    with cols[idx % 2]:
        if st.button(suggestion, use_container_width=True, key=f"sugg_{idx}"):
            st.session_state.text_input = suggestion
            # Trigger input processing
            if st.session_state.current_conv is None:
                st.session_state.conversations.append([])
                st.session_state.current_conv = 0
            response = get_response(suggestion)
            st.session_state.conversations[st.session_state.current_conv].append({
                "role": "user",
                "text": suggestion
            })
            st.session_state.conversations[st.session_state.current_conv].append({
                "role": "assistant",
                "text": response
            })
            st.rerun()

# Footer with styling
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8em;">
    <p>AeroFuel Assistant v1.0 | Aircraft Refueling Supervision Guide</p>
</div>
""", unsafe_allow_html=True)
