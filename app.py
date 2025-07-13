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

def calculate_bmr_tdee(weight_lbs: float, height_inches: float, age: int, gender: str, activity_level: str) -> dict:
    """Calculate BMR and TDEE using Mifflin-St Jeor equation"""
    # Convert to metric
    weight_kg = weight_lbs * 0.453592
    height_cm = height_inches * 2.54
    
    # Calculate BMR
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.375)
    
    # Weight loss calories (deficit of 500-750 for 1-1.5 lbs/week)
    weight_loss_calories = tdee - 500
    aggressive_loss_calories = tdee - 750
    
    return {
        'bmr': round(bmr),
        'tdee': round(tdee),
        'weight_loss': round(weight_loss_calories),
        'aggressive_loss': round(aggressive_loss_calories),
        'protein_grams': round(weight_lbs * 1.0)  # 1g per lb
    }

def show_calorie_calculator():
    """Display interactive calorie calculator with Glen's explanations"""
    st.markdown("### 🧮 **Glen's Personal Calorie Calculator**")
    
    # Add Glen's explanations for BMR and TDEE
    with st.expander("📚 **What are BMR and TDEE? (Click to learn)**", expanded=False):
        st.markdown("""
        ### 🔥 **BMR (Basal Metabolic Rate)**
        Your BMR is the number of calories your body burns just to stay alive - breathing, heart beating, brain functioning, cell repair. Think of it as your body's "idle speed."
        
        **Glen's take:** "Even if you laid in bed all day, you'd still burn your BMR calories. It's usually 60-70% of your total daily burn. This is why crash diets are stupid - you can't go below your BMR for long without your body fighting back."
        
        ### ⚡ **TDEE (Total Daily Energy Expenditure)**
        Your TDEE is your BMR PLUS all the calories you burn through activity - walking, working out, even fidgeting. This is your true daily calorie burn.
        
        **Glen's experience:** "After 25+ years of coaching, I've learned that most people underestimate their activity level. Be honest about your real lifestyle, not what you wish it was. That's how you get accurate numbers that actually work."
        
        ### 🎯 **Why This Matters for Weight Loss**
        - **Eat above TDEE = Weight gain**
        - **Eat at TDEE = Weight maintenance** 
        - **Eat below TDEE = Weight loss**
        
        **My recommendation:** Start 500 calories below your TDEE for steady 1 lb/week loss. It's sustainable and you won't feel like you're starving.
        """)
    
    st.markdown("*Get your exact numbers based on your stats!*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📏 **Physical Stats**")
        weight = st.number_input("Weight (pounds)", min_value=80, max_value=400, value=180, step=1)
        
        # Separate feet and inches for height
        height_ft = st.number_input("Height - Feet", min_value=4, max_value=7, value=5, step=1)
        height_in = st.number_input("Height - Inches", min_value=0, max_value=11, value=10, step=1)
        
        st.info(f"Your height: {height_ft}'{height_in}\"")
        
    with col2:
        st.markdown("#### 👤 **Personal Info**")
        age = st.number_input("Age", min_value=18, max_value=80, value=35, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        st.markdown("#### 🏃 **Activity Level**")
        activity = st.selectbox("Choose your HONEST activity level:", [
            "Sedentary (desk job, no exercise)",
            "Lightly Active (light exercise 1-3 days/week)", 
            "Moderately Active (moderate exercise 3-5 days/week)",
            "Very Active (hard exercise 6-7 days/week)",
            "Extra Active (very hard exercise + physical job)"
        ])
    
    # Map activity selection to key
    activity_map = {
        "Sedentary (desk job, no exercise)": "sedentary",
        "Lightly Active (light exercise 1-3 days/week)": "lightly_active",
        "Moderately Active (moderate exercise 3-5 days/week)": "moderately_active", 
        "Very Active (hard exercise 6-7 days/week)": "very_active",
        "Extra Active (very hard exercise + physical job)": "extra_active"
    }
    
    if st.button("🔥 Calculate My Numbers", type="primary", use_container_width=True):
        total_height = (height_ft * 12) + height_in
        results = calculate_bmr_tdee(weight, total_height, age, gender, activity_map[activity])
        
        st.markdown("---")
        st.markdown("### 🎯 **Your Personal Numbers:**")
        st.markdown(f"*Based on: {weight} lbs, {height_ft}'{height_in}\", {age} years old, {gender.lower()}, {activity.split('(')[0].strip()}*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔥 BMR", f"{results['bmr']:,} cal/day", 
                     help="Calories burned just staying alive")
            
        with col2:
            st.metric("⚡ TDEE", f"{results['tdee']:,} cal/day",
                     help="Total calories burned daily with activity")
            
        with col3:
            st.metric("🍖 Protein Target", f"{results['protein_grams']}g/day",
                     help="Glen's rule: 1g per pound bodyweight")
        
        st.markdown("---")
        st.markdown("### 📊 **Glen's Weight Loss Plan for You:**")
        
        loss_col1, loss_col2 = st.columns(2)
        
        with loss_col1:
            st.success(f"""
            #### 🎯 **Recommended: Steady Loss**
            
            **{results['weight_loss']:,} calories per day**
            
            *500 calorie deficit = 1 lb/week*
            
            **Glen says:** "This is my sweet spot. You'll lose weight consistently without feeling deprived. Most of my successful clients start here."
            """)
            
        with loss_col2:
            st.warning(f"""
            #### 🚀 **Aggressive: Fast Loss**
            
            **{results['aggressive_loss']:,} calories per day**
            
            *750 calorie deficit = 1.5 lbs/week*
            
            **Glen's warning:** "Only do this if you're highly motivated and can stick to it. Most people burn out on aggressive cuts."
            """)
        
        st.markdown("---")
        st.info(f"""
        ### 💪 **Glen's Complete Plan for You:**
        
        **🥘 Daily Targets:**
        • **{results['weight_loss']:,} calories** (for steady 1 lb/week loss)
        • **{results['protein_grams']}g protein** (non-negotiable!)
        • **{round(results['protein_grams'] * 1.2)}g carbs** (for energy)
        • **{round(results['weight_loss'] * 0.25 / 9)}g healthy fats** (for hormones)
        
        **📈 Tracking Tips:**
        • Weigh yourself same day/time weekly
        • Take progress photos every 2 weeks
        • Track food for first 2 weeks to learn portions
        • Adjust calories if no progress after 3 weeks
        
        **Glen's reality check:** "These numbers are your starting point. Every body responds differently. Give it 2-3 weeks, then adjust based on your results. I've been doing this for 25+ years - trust the process!"
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 🗓️ **Ready for Your Complete Transformation Plan?**
        
        These numbers are just the foundation. Get your personalized meal plans, workout schedules, and shopping lists:
        
        👉 **[Visit bestrongagain.com/plan-my-week/](https://bestrongagain.com/plan-my-week/)**
        
        *Turn these calories into a complete 12-week transformation system!*
        """)

def get_quick_answer(query: str) -> str:
    """Handle common softball questions with direct, practical answers"""
    query_lower = query.lower()
    
    # Calorie questions - now with calculator
    if any(word in query_lower for word in ["calories", "calorie", "how much eat", "how many eat", "bmr", "tdee"]):
        # Set a flag to show calculator
        st.session_state.show_calculator = True
        
        return """**Let me give you YOUR exact calorie numbers!**

Instead of generic advice, let's calculate your personal BMR and TDEE based on your stats. Check out my **Calorie Calculator** below - it'll give you precise numbers for your body and activity level.

**My quick guidelines while you calculate:**
• **Men:** Usually 2,200-2,800 calories for weight loss
• **Women:** Usually 1,800-2,200 calories for weight loss  
• **Protein:** Always 1g per pound bodyweight

**But your EXACT numbers matter more than averages!**

Use the calculator below, then visit **[bestrongagain.com/plan-my-week/](https://bestrongagain.com/plan-my-week/)** for a complete meal plan built around your specific calorie target.

*After 25+ years of coaching, I've learned that personalized numbers get personalized results!*

**👇 Use the calculator below to get your exact numbers! 👇**"""

    # Protein questions
    if any(word in query_lower for word in ["protein", "how much protein"]):
        return """**My protein rule is simple: 1 gram per pound of body weight.**

**So if you weigh 180 pounds = 180g protein daily**

**Why protein is king:**
• Builds and maintains muscle
• Boosts metabolism (burns calories to digest)
• Keeps you full longer
• Prevents blood sugar crashes

**Easy protein sources:**
• **Chicken breast:** 25g per 4oz
• **Eggs:** 6g per egg
• **Greek yogurt:** 15-20g per cup
• **Protein powder:** 20-30g per scoop
• **Ground turkey:** 22g per 4oz

**My personal take:** I've had blood work done multiple times - high protein is safe and effective. Don't let anyone scare you away from adequate protein!

*This approach has worked for thousands of my clients over 25+ years.*"""

    # Water/hydration questions
    if any(word in query_lower for word in ["water", "hydration", "drink", "fluid"]):
        return """**My hydration formula: Half your body weight in ounces, minimum.**

**If you weigh 200 pounds = 100 ounces (about 12 cups) daily**

**Simple hydration tips:**
• **Start your day** with 16-20oz of water
• **Drink before you're thirsty**
• **More if you're active** or it's hot
• **Monitor your urine** - light yellow is perfect

**What counts toward hydration:**
• Plain water (best choice)
• Herbal tea
• Coffee (in moderation)
• Water-rich foods (fruits, veggies)

**What doesn't help:**
• Alcohol (actually dehydrates you)
• High-sugar drinks
• Excessive caffeine

*Good hydration supports everything - energy, recovery, fat loss, and performance!*"""

    # Exercise/workout frequency
    if any(word in query_lower for word in ["exercise", "workout", "train", "how often", "how many times"]):
        return """**My training philosophy: 3-4 days per week, consistently.**

**For beginners:**
• **3 days/week** - Perfect starting point
• **Every other day** - Allows recovery
• **Full body workouts** - Hit everything

**For experienced:**
• **4-5 days/week** - Upper/lower splits work great
• **Listen to your body** - Recovery is when you grow
• **Quality over quantity** - 45 minutes beats 2 hours

**What matters most:**
• **Show up consistently** (I train at 3:30am!)
• **Progressive overload** - Gradually increase difficulty
• **Compound movements** - Squats, deadlifts, rows
• **Find exercises you enjoy** - You'll stick with them

**My reality check:** The best workout is the one you'll actually do. Start where you are, be consistent, and build from there.

*Consistency beats perfection every single time.*"""

    # Weight loss timeline
    if any(word in query_lower for word in ["lose weight", "weight loss", "how long", "how fast"]):
        return """**Realistic weight loss: 1-2 pounds per week.**

**My timeline expectations:**
• **Week 1-2:** 3-5 pounds (mostly water weight)
• **Week 3-12:** 1-2 pounds consistently
• **12 weeks total:** 15-25 pounds realistically

**What affects your rate:**
• **Starting weight** - Heavier people lose faster initially
• **Age and gender** - Men typically lose faster
• **Activity level** - More movement = faster results
• **Consistency** - This is the biggest factor

**Glen's reality check:**
Don't chase the scale daily. Focus on:
• **How your clothes fit**
• **Energy levels**
• **Strength improvements**
• **Progress photos**

**Remember:** You didn't gain it overnight, you won't lose it overnight. But stick with my system for 12 weeks and you'll be amazed at the transformation!

*I've seen this work for thousands of people over 25+ years.*"""

    # Meal timing
    if any(word in query_lower for word in ["when to eat", "meal timing", "how often eat"]):
        return """**My meal timing approach: Eat every 3-4 hours.**

**Simple schedule that works:**
• **Breakfast:** Within 1 hour of waking
• **Lunch:** 4-5 hours later
• **Dinner:** 4-5 hours after lunch
• **Snacks:** If needed between meals

**What matters most:**
• **Protein at every meal** - Non-negotiable
• **Don't skip meals** - Leads to overeating later
• **Last meal 2-3 hours before bed** - Better sleep
• **Listen to your hunger** - Don't eat just because it's "time"

**My personal approach:**
I eat 3 main meals + 1-2 protein snacks. Keeps my energy steady and prevents those blood sugar crashes that lead to poor food choices.

**Bottom line:** Consistency with meal timing helps regulate your metabolism and prevents impulsive eating decisions.

*Find a schedule that fits your life and stick with it!*"""

    return None  # No quick answer found

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

def format_glen_response(results: List[Dict[str, str]], query: str = "") -> str:
    """Format the search results as if Glen is personally responding"""
    
    # First check for quick answers to common questions
    quick_answer = get_quick_answer(query)
    if quick_answer:
        return quick_answer
    
    # If no quick answer, proceed with knowledge base search results
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
    
    # Initialize session state early
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_calculator" not in st.session_state:
        st.session_state.show_calculator = False
    
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
        # Show calorie calculator if triggered
        if st.session_state.show_calculator:
            show_calorie_calculator()
            st.markdown("---")
        
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
                    response = format_glen_response(results, prompt)
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
                response = format_glen_response(results, query)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Example questions section
    st.markdown("### 💡 Popular Questions")
    example_questions = [
        "How many calories should I eat daily?",
        "How much protein do I need?", 
        "How often should I exercise?",
        "How much water should I drink?",
        "How fast can I lose weight?",
        "When should I eat my meals?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        col = cols[i % 3]
        if col.button(question, key=f"example_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            results = search_all_knowledge_bases(question, data)
            response = format_glen_response(results, question)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
