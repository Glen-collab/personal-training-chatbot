import streamlit as st
import json
import re
from typing import List, Dict, Any
import base64
from pathlib import Path
import random

# Page config
st.set_page_config(
    page_title="Glen Intelligence - Your Personal Fitness Coach",
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
    
    /* Program stats */
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
    
    /* Glen's personality indicators */
    .glen-response {
        border-left: 4px solid #FF6B6B;
        padding-left: 1rem;
        margin: 1rem 0;
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
        <h1>💪 GLEN INTELLIGENCE</h1>
        <p>Your Personal Fitness, Nutrition & Psychology Coach</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and display logo
    logo_base64, logo_filename = load_logo_from_github()
    if logo_base64:
        file_extension = logo_filename.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg']:
            mime_type = 'image/jpeg'
        elif file_extension == 'png':
            mime_type = 'image/png'
        elif file_extension == 'gif':
            mime_type = 'image/gif'
        else:
            mime_type = 'image/png'
        
        st.markdown(f'''
        <div class="logo-container">
            <img src="data:{mime_type};base64,{logo_base64}" class="logo" alt="Glen's Logo">
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("💡 To add your logo, upload an image file named 'logo.png' to your repository")

def display_program_stats():
    """Display program statistics and achievements"""
    st.markdown("""
    <div class="program-stats">
        <div class="stat-item">🏆 17+ Years Training Experience</div>
        <div class="stat-item">📚 Multiple Expert Certifications</div>
        <div class="stat-item">💪 Thousands Transformed</div>
        <div class="stat-item">🧠 25+ Years Client Experience</div>
        <div class="stat-item">🥇 Former Powerlifter/Strongman</div>
        <div class="stat-item">🏢 Wisconsin Barbell Gym Owner</div>
    </div>
    """, unsafe_allow_html=True)

def display_glen_quote():
    """Display inspirational quotes from Glen"""
    quotes = [
        "If you're five minutes early, you're 10 minutes late. - Marine Corps wisdom that drives my training",
        "Consistency beats perfection every time. After 17 years, I've learned this is the key to lasting transformation.",
        "Protein is king for muscle repair and metabolism. My blood tests prove it's safe and effective.",
        "Small goals prevent burnout and build momentum. I learned this from my powerlifting days.",
        "Food is fuel, not comfort. This mindset shift changed everything for my clients.",
        "I train at 3:30am because consistency builds habits, and habits build character.",
        "Your mind is your most powerful muscle. That's what 25 years of client work has taught me."
    ]
    quote = random.choice(quotes)
    
    st.markdown(f"""
    <div class="glen-quote">
        "{quote}"
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_all_knowledge_data():
    """Load ALL knowledge bases from JSON files"""
    all_data = {}
    
    # Try to load the main fitness file
    try:
        with open('strong_again_complete.json', 'r') as f:
            fitness_data = json.load(f)
            all_data.update(fitness_data)
    except FileNotFoundError:
        st.warning("Main fitness JSON file not found.")
    
    # Try to load additional knowledge bases
    additional_files = [
        'behavioral_psychology_converted.json',
        'nutrition_health_converted.json', 
        'weight_loss_barriers_converted.json',
        'health_nutrition_converted.json'
    ]
    
    for filename in additional_files:
        try:
            with open(filename, 'r') as f:
                additional_data = json.load(f)
                all_data.update(additional_data)
                st.success(f"✅ Loaded {filename}")
        except FileNotFoundError:
            continue  # Skip files that don't exist yet
    
    return all_data

def search_all_knowledge_bases(query: str, data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Search through ALL knowledge bases for relevant content"""
    if not data:
        return []
    
    query_lower = query.lower()
    results = []
    
    # Search through all book categories
    for book_category, book_data in data.items():
        if not isinstance(book_data, dict) or 'content' not in str(book_data):
            continue
            
        # Skip metadata
        if book_category in ['source', 'author_context']:
            continue
        
        # Search through all sections in this book
        for section_name, section_data in book_data.items():
            if section_name in ['source', 'author_context'] or not isinstance(section_data, dict):
                continue
                
            tags = section_data.get('tags', [])
            keywords = section_data.get('keywords', [])
            
            # Check for tag and keyword matches
            tag_match = any(tag.lower() in query_lower or query_lower in tag.lower() for tag in tags)
            keyword_match = any(keyword.lower() in query_lower or query_lower in keyword.lower() for keyword in keywords)
            
            # Search through content items
            content_items = section_data.get('content', [])
            for item in content_items:
                topic = item.get('topic', '')
                response = item.get('response', '')
                
                # Calculate relevance
                topic_match = query_lower in topic.lower() or any(word in topic.lower() for word in query_lower.split())
                response_match = query_lower in response.lower() or any(word in response.lower() for word in query_lower.split())
                
                if tag_match or keyword_match or topic_match or response_match:
                    results.append({
                        'book_category': book_category.replace('_book_data', '').replace('_', ' ').title(),
                        'section': section_name.replace('_', ' ').title(),
                        'topic': topic,
                        'response': response,
                        'relevance_score': calculate_relevance(query_lower, topic, response, tags, keywords)
                    })
    
    # Sort by relevance and return top results
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results[:5]  # Return top 5 results from across all books

def calculate_relevance(query: str, topic: str, response: str, tags: List[str], keywords: List[str]) -> float:
    """Enhanced relevance calculation"""
    score = 0.0
    query_words = query.split()
    
    # Exact matches get highest scores
    if query in topic.lower():
        score += 15
    if query in response.lower():
        score += 10
    
    # Word matches
    for word in query_words:
        if word in topic.lower():
            score += 5
        if word in response.lower():
            score += 2
        if any(word in tag.lower() for tag in tags):
            score += 3
        if any(word in keyword.lower() for keyword in keywords):
            score += 3
    
    # Bonus for psychology-related queries
    psych_terms = ['motivation', 'mindset', 'psychology', 'behavior', 'stress', 'mental']
    if any(term in query.lower() for term in psych_terms):
        if any(term in ' '.join(tags).lower() for term in psych_terms):
            score += 5
    
    return score

def add_glen_personality(response_text: str) -> str:
    """Add Glen's personal touch to responses"""
    personal_intros = [
        "In my 17 years as a trainer and gym owner, ",
        "From my experience coaching thousands of clients, ",
        "As a former powerlifter and strongman competitor, ",
        "At Wisconsin Barbell Gym, I've learned that ",
        "After 25 years of working with clients, I've learned that ",
        "From my experience understanding what motivates people, "
    ]
    
    personal_connectors = [
        "\n\nI've seen this pattern with many of my clients at the gym. ",
        "\n\nThis reminds me of when I was competing - ",
        "\n\nI always tell my clients: ",
        "\n\nFrom my psychology studies, I know that ",
        "\n\nOne thing I've learned after all these years: "
    ]
    
    # Add personality based on content
    if "protein" in response_text.lower():
        response_text += "\n\n*I've personally tested this approach and even had blood work done to verify it's safe and effective.*"
    
    if any(word in response_text.lower() for word in ["stress", "motivation", "mindset"]):
        response_text += "\n\n*This is where my 25+ years of client experience really helps people break through mental barriers.*"
    
    if "training" in response_text.lower() or "exercise" in response_text.lower():
        response_text += "\n\n*Remember, I train at 3:30am because consistency builds habits, and habits build character. Find what works for YOUR schedule.*"
    
    return response_text

def format_glen_response(results: List[Dict[str, str]]) -> str:
    """Format the search results as if Glen is personally responding"""
    if not results:
        no_answer_responses = [
            "I don't have specific information about that in my knowledge base right now, but I'd love to help! As someone with 17+ years in this field, I'm always learning too.",
            "That's not something I've covered in my current materials, but it's a great question! With my background in fitness, nutrition, and psychology, I might be able to point you in the right direction.",
            "Hmm, I don't see that topic in my current resources. But hey, after coaching thousands of clients, I've learned there's always more to discover!"
        ]
        base_response = random.choice(no_answer_responses)
        
        return f"{base_response}\n\nTry asking me about:\n• **Fitness & Training** (my powerlifting background)\n• **Nutrition & Weight Loss** (evidence-based approaches)\n• **Psychology & Motivation** (behavioral science)\n• **My 12-Week Program** (proven transformation system)\n\n*Feel free to contact me directly at Wisconsin Barbell Gym for personalized coaching!*"
    
    # Start with a personal greeting
    personal_openings = [
        "Great question! Let me share what I know about this...",
        "I'm glad you asked about this - it's something I work with clients on regularly.",
        "This is exactly the kind of thing I help people with at the gym. Here's my take:",
        "Perfect timing on this question! This comes up a lot in my coaching practice.",
        "I love talking about this topic - it's core to what I do. Let me break it down:"
    ]
    
    response = f"**{random.choice(personal_openings)}**\n\n"
    
    # Add the main content
    main_result = results[0]
    enhanced_response = add_glen_personality(main_result['response'])
    
    response += f"### 🎯 {main_result['topic']}\n\n{enhanced_response}\n\n"
    
    # Add related insights if available
    if len(results) > 1:
        response += "### 📌 Related Insights:\n\n"
        for result in results[1:3]:  # Show up to 2 more related results
            category_emoji = "🧠" if "psychology" in result['book_category'].lower() else "💪" if "fitness" in result['book_category'].lower() else "🥗"
            enhanced_related = add_glen_personality(result['response'])
            response += f"**{category_emoji} {result['topic']}**\n\n{enhanced_related}\n\n"
    
    # Add personal signature
    signatures = [
        "---\n*This comes from my 17+ years as a gym owner, personal trainer, and former competitive lifter. Every piece of advice is battle-tested with real clients.*",
        "---\n*Hope this helps! This approach has worked for thousands of my clients at Wisconsin Barbell Gym.*",
        "---\n*These insights combine my competition experience, training expertise, and 25+ years of understanding what motivates people.*"
    ]
    
    response += random.choice(signatures)
    
    return response

def main():
    # Load custom CSS
    load_custom_css()
    
    # Display header with logo
    display_header_with_logo()
    
    # Load all knowledge data
    data = load_all_knowledge_data()
    
    if not data:
        st.error("❌ No knowledge base files found. Please upload your JSON files.")
        st.stop()
    
    # Show what knowledge bases are loaded
    categories = [key.replace('_book_data', '').replace('_', ' ').title() for key in data.keys() if key.endswith('_book_data')]
    if categories:
        st.success(f"🧠 **Glen Intelligence Active:** {', '.join(categories)}")
    
    # Sidebar with enhanced program info
    with st.sidebar:
        st.markdown("## 🏋️ About Glen")
        
        # Program stats
        display_program_stats()
        
        st.markdown("### 🎯 Ask Me About:")
        topics = [
            "🍖 Protein and nutrition science",
            "🏋️ Training methodology", 
            "📋 Meal planning strategies",
            "🧠 Understanding client motivation",
            "⏰ Time management for busy people",
            "🎯 SMART goal setting",
            "💧 Hydration protocols",
            "📈 Progress tracking systems",
            "🔄 Carb cycling approaches",
            "💊 Supplement strategies",
            "😰 Overcoming barriers & excuses",
            "🧘 Stress management techniques"
        ]
        for topic in topics:
            st.markdown(f"• {topic}")
        
        # Glen's quote
        display_glen_quote()
        
        st.markdown("---")
        st.markdown("### 📞 Connect with Glen")
        st.markdown("🏢 **Wisconsin Barbell Gym**")
        st.markdown("📧 Personal training & coaching")
        st.markdown("🎓 **25+ years client experience**")
    
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
        if prompt := st.chat_input("💬 Ask Glen anything about fitness, nutrition, psychology, or motivation..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🧠 Glen is thinking..."):
                    results = search_all_knowledge_bases(prompt, data)
                    response = format_glen_response(results)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.markdown("### 🚀 Quick Start")
        st.markdown("**New here? Try these:**")
        
        quick_buttons = [
            ("💪 Master Plan", "Tell me about the 12-week master plan"),
            ("🧠 Psychology", "How does psychology help with fitness goals?"),
            ("🥗 Nutrition", "What should I know about protein and nutrition?"),
            ("😤 Motivation", "I'm struggling with motivation - help!")
        ]
        
        for label, query in quick_buttons:
            if st.button(label, key=f"quick_{label}"):
                st.session_state.messages.append({"role": "user", "content": query})
                results = search_all_knowledge_bases(query, data)
                response = format_glen_response(results)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Example questions section
    st.markdown("### 💡 Popular Questions")
    example_questions = [
        "How much protein should I eat daily?",
        "How do I connect and thrive in my fitness journey?", 
        "How do I overcome weight loss barriers?",
        "What's your training philosophy?",
        "How do I stay motivated for 12 weeks?",
        "Tell me about stress and weight loss"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        col = cols[i % 3]
        if col.button(question, key=f"example_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            results = search_all_knowledge_bases(question, data)
            response = format_glen_response(results)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
