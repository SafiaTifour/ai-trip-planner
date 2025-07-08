import streamlit as st
import requests
from datetime import datetime

# Replace with the actual address if deploying (e.g., "https://your-backend.com")
API_URL = "http://localhost:8000/chat"

# Page configuration
st.set_page_config(
    page_title="🧳 Travel Agent AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-height: 60vh;
        overflow-y: auto;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 18px 18px 5px 18px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .assistant-message {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem;
        border-radius: 18px 18px 18px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Input styling */
    .stChatInput {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Stats container */
    .stats-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-item {
        display: inline-block;
        margin: 0 1rem;
        padding: 0.5rem;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header section
st.markdown("""
<div class="main-header">
    <div class="main-title">✈️ AI Travel Planner</div>
    <div class="subtitle">Your intelligent companion for seamless travel planning</div>
    <div style="margin-top: 1rem;">
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem;">
            🌍 Powered by Advanced AI • 🚀 Real-time Assistance • 🎯 Personalized Recommendations
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature cards section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏖️</div>
        <div class="feature-title">Destinations</div>
        <div class="feature-desc">Discover amazing places worldwide</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💰</div>
        <div class="feature-title">Budget Planning</div>
        <div class="feature-desc">Smart cost optimization</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌤️</div>
        <div class="feature-title">Weather Info</div>
        <div class="feature-desc">Real-time weather updates</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎭</div>
        <div class="feature-title">Activities</div>
        <div class="feature-desc">Curated experiences</div>
    </div>
    """, unsafe_allow_html=True)

# Stats section
message_count = len(st.session_state.chat_history)
current_time = datetime.now().strftime("%H:%M")

st.markdown(f"""
<div class="stats-container">
    <div class="stat-item">
        <div class="stat-number">{message_count}</div>
        <div class="stat-label">Messages</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">{current_time}</div>
        <div class="stat-label">Current Time</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">🟢</div>
        <div class="stat-label">AI Status</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-message">👤 {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">🤖 {msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything about your travel plans... 🌟", key="travel_input")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    
    # Show user message immediately
    st.markdown(f'<div class="user-message">👤 {user_input}</div>', unsafe_allow_html=True)
    
    # Process AI response
    with st.spinner("🤖 AI is thinking..."):
        try:
            response = requests.post(API_URL, json={"message": user_input})
            response.raise_for_status()
            agent_reply = response.json().get("response", "No response.")
        except Exception as e:
            agent_reply = f"❌ Connection Error: {str(e)}"
        
        st.session_state.chat_history.append(("assistant", agent_reply))
        
        # Show AI response
        st.markdown(f'<div class="assistant-message">🤖 {agent_reply}</div>', unsafe_allow_html=True)
    
    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.1); border-radius: 10px;">
    <p style="color: rgba(255, 255, 255, 0.8); margin: 0;">
        Made with ❤️ for travelers worldwide • 
        <span style="color: #FFD700;">⭐</span> AI-Powered • 
        <span style="color: #98FB98;">🌿</span> Sustainable Travel
    </p>
</div>
""", unsafe_allow_html=True)