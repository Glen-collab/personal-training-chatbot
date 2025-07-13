import streamlit as st
import json
import re
from typing import List, Dict, Any
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Strong Again Fitness Chatbot",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding and styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Main background and theme */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    
    .logo {
        max-width: 200px;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .logo:hover {
        transform: scale(1.05);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2C3E50, #34495E);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Progress indicators */
    .program-stats {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .stat-item {
        margin: 0.5rem 0;
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    /* Quote section */
    .glen-quote {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-left: 5px solid #FF6B6B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        color: white;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
        .logo {
            max-width: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def load_logo_from_github():
    """Load logo from GitHub repository"""
    # Common logo filenames to check
    logo_files = [
        "logo.png", "logo.jpg", "logo.jpeg", "logo.gif",
        "Logo.png", "Logo.jpg", "Logo.jpeg", "Logo.gif",
        "strong_again_logo.png", "strong_again_logo.jpg",
        "gym_logo.png", "gym_logo.jpg"
    ]
    
    for filename in logo_files:
        if Path(filename).exists():
            try:
                with open(filename, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    return encoded_string, filename
            except Exception as e:
                st.error(f"Error loading {filename}: {e}")
                continue
    
    return None, None

def display_header_with_logo():
    """Display custom header with logo"""
    st.markdown("""
    <div class="main-header">
        <h1>💪 STRONG AGAIN</h1>
        <p>Glen's Proven 12-Week Transformation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and display logo
    logo_base64, logo_filename = load_logo_from_github()
    if logo_base64:
        # Determine image type from filename
        file_extension = logo_filename.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg']:
            mime_type = 'image/jpeg'
        elif file_extension == 'png':
            mime_type = 'image/png'
        elif file_extension == 'gif':
            mime_type = 'image/gif'
        else:
            mime_type = 'image/png'  # default
        
        st.markdown(f'''
        <div class="logo-container">
            <img src="data:{mime_type};base64,{logo_base64}" class="logo" alt="Strong Again Logo">
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Display message about logo
        st.info("💡 To add your logo, upload an image file named 'logo.png', 'logo.jpg', or 'strong_again_logo.png' to your repository")

def display_program_stats():
    """Display program statistics and achievements"""
    st.markdown("""
    <div class="program-stats">
        <div class="stat-item">🏆 17+ Years Training Experience</div>
        <div class="stat-item">📚 Proven 12-Week System</div>
        <div class="stat-item">💪 Thousands Transformed</div>
        <div class="stat-item">🎯 Master Plan Approach</div>
    </div>
    """, unsafe_allow_html=True)

def display_glen_quote():
    """Display inspirational quote from Glen"""
    quotes = [
        "If you're five minutes early, you're 10 minutes late. - Marine Corps wisdom",
        "Consistency beats perfection every time. - Glen",
        "Protein is king for muscle repair and metabolism. - Glen's Program",
        "Small goals prevent burnout and build momentum. - Strong Again Method"
    ]
    import random
    quote = random.choice(quotes)
    
    st.markdown(f"""
    <div class="glen-quote">
        "{quote}"
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_fitness_data():
    """Load the fitness knowledge base from JSON"""
    try:
        with open('strong_again_complete.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("JSON data file not found. Please upload 'strong_again_complete.json' to your repository.")
        return None
    except json.JSONDecodeError:
        st.error("Error reading JSON file. Please check the file format.")
        return None

def search_knowledge_base(query: str, data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Search through the knowledge base for relevant content"""
    if not data:
        return []
    
    query_lower = query.lower()
    results = []
    
    fitness_data = data.get('fitness_book_data', {})
    
    for section_name, section_data in fitness_data.items():
        if section_name in ['source', 'author_context']:
            continue
            
        tags = section_data.get('tags', [])
        keywords = section_data.get('keywords', [])
        
        tag_match = any(tag.lower() in query_lower or query_lower in tag.lower() for tag in tags)
        keyword_match = any(keyword.lower() in query_lower or query_lower in keyword.lower() for keyword in keywords)
        
        content_items = section_data.get('content', [])
        for item in content_items:
            topic = item.get('topic', '')
            response = item.get('response', '')
            
            topic_match = query_lower in topic.lower() or any(word in topic.lower() for word in query_lower.split())
            response_match = query_lower in response.lower() or any(word in response.lower() for word in query_lower.split())
            
            if tag_match or keyword_match or topic_match or response_match:
                results.append({
                    'section': section_name.replace('_', ' ').title(),
                    'topic': topic,
                    'response': response,
                    'relevance_score': calculate_relevance(query_lower, topic, response, tags, keywords)
                })
    
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results[:3]

def calculate_relevance(query: str, topic: str, response: str, tags: List[str], keywords: List[str]) -> float:
    """Calculate relevance score for search results"""
    score = 0.0
    query_words = query.split()
    
    if query in topic.lower():
        score += 10
    if query in response.lower():
        score += 5
    
    for word in query_words:
        if word in topic.lower():
            score += 3
        if word in response.lower():
            score += 1
        if any(word in tag.lower() for tag in tags):
            score += 2
        if any(word in keyword.lower() for keyword in keywords):
            score += 2
    
    return score

def format_response(results: List[Dict[str, str]]) -> str:
    """Format the search results into a coherent response"""
    if not results:
        return "I don't have specific information about that topic in Glen's program right now. Could you try asking about nutrition, workouts, meal planning, motivation, or the 12-week transformation program?"
    
    response = "**Based on Glen's 'Strong Again' program:**\n\n"
    
    for i, result in enumerate(results, 1):
        if i == 1:
            response += f"### 🎯 {result['topic']}\n\n{result['response']}\n\n"
        else:
            response += f"### 📌 Related: {result['topic']}\n{result['response']}\n\n"
    
    response += "---\n*💪 This advice comes from Glen's 17+ years as a gym owner, personal trainer, and former powerlifter/strongman competitor.*"
    
    return response

def main():
    # Load custom CSS
    load_custom_css()
    
    # Display header with logo
    display_header_with_logo()
    
    # Load data
    data = load_fitness_data()
    
    if not data:
        st.stop()
    
    # Sidebar with enhanced program info
    with st.sidebar:
        st.markdown("## 🏋️ About Glen's Program")
        
        # Program stats
        display_program_stats()
        
        st.markdown("### 🎯 Ask About:")
        topics = [
            "🍖 Protein and nutrition",
            "🏋️ Weight training tips", 
            "📋 Meal planning & prep",
            "💭 Motivation & mindset",
            "⏰ Time management",
            "🎯 Goal setting (SMART)",
            "💧 Hydration strategy",
            "📈 Progress tracking",
            "🔄 Carb cycling",
            "💊 Supplements & TRT"
        ]
        for topic in topics:
            st.markdown(f"• {topic}")
        
        # Glen's quote
        display_glen_quote()
        
        st.markdown("---")
        st.markdown("### 📞 Connect with Glen")
        st.markdown("🏢 Wisconsin Barbell Gym")
        st.markdown("📧 Contact for personal training")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("💬 Ask Glen about fitness, nutrition, or his 12-week program..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🔍 Searching Glen's program..."):
                    results = search_knowledge_base(prompt, data)
                    response = format_response(results)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.markdown("### 🚀 Quick Start")
        st.markdown("**New to the program?**")
        if st.button("📋 Get the Master Plan"):
            st.session_state.messages.append({"role": "user", "content": "What's the master plan approach?"})
            results = search_knowledge_base("master plan approach", data)
            response = format_response(results)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Example questions section
    st.markdown("### 💡 Popular Questions")
    example_questions = [
        "How much protein should I eat daily?",
        "What's the 12-week program structure?", 
        "How do I stay motivated for 12 weeks?",
        "What should I eat for breakfast?",
        "How do I manage time for workouts?",
        "Tell me about carb cycling"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        col = cols[i % 3]
        if col.button(question, key=f"example_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            results = search_knowledge_base(question, data)
            response = format_response(results)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
