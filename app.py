import streamlit as st
import json
import re
import base64
from pathlib import Path
import random
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        <p>Your Personal Fitness, Nutrition & Motivational Coach</p>
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
        with open('strong_again_complete_clean.json', 'r', encoding='utf-8') as f:
            fitness_data = json.load(f)
            all_data.update(fitness_data)
            logger.debug(f"Loaded sections: {list(fitness_data.get('fitness_book_data', {}).keys())}")
            logger.debug("Successfully loaded strong_again_complete_clean.json")
    except FileNotFoundError:
        st.warning("Main fitness JSON file not found.")
        logger.error("FileNotFoundError: strong_again_complete_clean.json not found")
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        logger.error(f"JSONDecodeError: {e}")
    except UnicodeDecodeError as e:
        st.error(f"Unicode error in JSON file: {e}")
        logger.error(f"UnicodeDecodeError: {e}")
    
    # Try to load additional knowledge bases
    additional_files = [
        'behavioral_psychology_converted.json',
        'nutrition_health_converted.json', 
        'weight_loss_barriers_converted.json',
        'health_nutrition_converted.json'
    ]
    
    for filename in additional_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                additional_data = json.load(f)
                all_data.update(additional_data)
                st.success(f"✅ Loaded {filename}")
                logger.debug(f"Loaded sections: {list(additional_data.keys())}")
        except FileNotFoundError:
            logger.debug(f"File {filename} not found, skipping")
            continue
    
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
        weight = st.number_input("Weight (pounds)", min_value=80, max_value=400, value=180, step=5, format="%d")
        
        # Separate feet and inches for height
        height_ft = st.number_input("Height - Feet", min_value=4, max_value=7, value=5, step=1, format="%d")
        height_in = st.number_input("Height - Inches", min_value=0, max_value=11, value=10, step=1, format="%d")
        
        st.info(f"Your height: {height_ft}'{height_in}\"")
        
    with col2:
        st.markdown("#### 👤 **Personal Info**")
        age = st.number_input("Age", min_value=18, max_value=80, value=35, step=1, format="%d")
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
        
        # Store results in session state for sticky display
        st.session_state.calculated_results = {
            'bmr': results['bmr'],
            'tdee': results['tdee'],
            'weight_loss': results['weight_loss'],
            'aggressive_loss': results['aggressive_loss'],
            'protein_grams': results['protein_grams'],
            'weight': weight,
            'height_ft': height_ft,
            'height_in': height_in,
            'age': age,
            'gender': gender,
            'activity': activity.split('(')[0].strip()
        }
        
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
        
        # Hide calculator after calculation
        st.session_state.show_calculator = False

def get_quick_answer(query: str) -> str:
    """Handle common softball questions with direct, practical answers"""
    query_lower = query.lower()
    
    # Carbohydrate questions
    if any(word in query_lower for word in ["carb", "carbs", "carbohydrates", "how many carbs", "how much carbs"]):
        # Check if calculator results exist for personalized response
        if st.session_state.get('calculated_results'):
            results = st.session_state.calculated_results
            carb_grams = round(results['protein_grams'] * 1.2)  # From calculator: 1.2x protein grams
            weight = results['weight']
            activity = results['activity']
            tdee = results['tdee']
            return f"""**My carb rule: Aim for 1.2g per pound of body weight for balanced energy, adjusted to your goals.**

**For you ({weight} lbs, {activity}):**
• **{carb_grams}g carbs daily** (based on your {results['protein_grams']}g protein target)
• **Roughly {round(carb_grams * 4 / tdee * 100)}% of your {tdee:,} calorie TDEE**

**Why this works:**
• **Carbs fuel performance**: They power your workouts and recovery.
• **1.2g/lb is sustainable**: Enough for energy, not so much you store fat.
• **Adjust based on goals**:
  - **Weight loss**: Stick to {carb_grams - 20}-{carb_grams}g, prioritize veggies.
  - **Muscle gain**: Bump to {carb_grams + 20}-{carb_grams + 50}g, add starches.
  - **Maintenance**: Stay at {carb_grams}g.

**Best carb sources:**
• **Oats**: 25g carbs per 1/2 cup (pre-workout energy)
• **Sweet potatoes**: 26g per medium potato (steady energy)
• **Brown rice**: 45g per cup (post-workout recovery)
• **Vegetables**: 5-10g per cup (micronutrients, low calorie)
• **Fruit**: 15-20g per piece (natural sugars, vitamins)

**My experience:** After 25+ years, I’ve seen clients thrive on this carb range. It’s enough to crush workouts without feeling sluggish or bloated. Low-carb fads can tank your energy—don’t fall for it!

**Pro tip:** Time carbs around workouts—50% of daily carbs pre/post-workout for max performance.

**Let me ask you:** Are you struggling with energy crashes, or is carb confusion (what to eat, when) your biggest issue? I’ve got strategies for both!

*Run the calorie calculator again for updated numbers if your weight or activity changes!*"""
        else:
            # Fallback if no calculator results
            st.session_state.show_calculator = True
            return """**Carbs depend on your body and goals, so let’s get specific!**

**My general rule:** Aim for 1-1.5g carbs per pound of body weight daily.
• **Example**: 180 lbs = 180-270g carbs
• **Weight loss**: Lean toward 1g/lb, mostly veggies.
• **Muscle gain**: Push toward 1.5g/lb, include starches.
• **Active folks**: Adjust up for intense training days.

**Why carbs matter:**
• Fuel workouts and recovery.
• Prevent energy crashes.
• Support muscle retention.

**Best sources:**
• Oats, sweet potatoes, brown rice (complex carbs).
• Vegetables like broccoli, spinach (low-calorie, nutrient-dense).
• Fruits like bananas, apples (natural sugars).

**Glen’s take:** I’ve coached thousands to balance carbs for energy without fat gain. Low-carb diets can work short-term but often leave you drained. Timing matters—eat most carbs around workouts.

**Next step:** Use my **Calorie Calculator** below to get your exact carb target based on your weight and activity level. It’ll give you a precise number!

**Quick question:** Are you cutting carbs too low and feeling tired, or overwhelmed by carb choices? Let me know what’s tripping you up!"""

    # Calorie/eating questions - broader detection
    if any(word in query_lower for word in ["calories", "calorie", "how much eat", "how many eat", "how much should i eat", "what should i eat", "bmr", "tdee", "how much food"]):
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

**👇 Use the calculator below to get your exact numbers! 👇**

**One more thing:** Are you dealing with any specific challenges like busy work schedules, family stress, or past diet failures? I've got targeted solutions for real-life obstacles!"""

# Protein questions
if any(word in query_lower for word in ["protein", "how much protein", "best protein", "high protein", "what protein", "good protein"]):
    if not st.session_state.get("protein_strikes"):
        st.session_state["protein_strikes"] = 0

    responses = [
        """**My protein rule is simple: 1g per pound of body weight.**  
That means if you weigh 180 lbs → you need about **180g protein/day**.

**Top protein sources I recommend:**  
• Chicken breast (25g per 4oz)  
• Greek yogurt (15–20g per cup)  
• Protein powder (20–30g per scoop)  
• Eggs (6g each)  
• Ground turkey (22g per 4oz)  
• Cottage cheese, tuna, lean beef, shrimp — take your pick.

**Why it matters:**  
• Builds and maintains lean muscle  
• Keeps you full  
• Boosts your metabolism  
• Supports recovery

**Glen’s personal take:** I rotate between grilled chicken, 93% lean ground turkey, protein shakes, and eggs. Simple, clean, and works like a charm.

Let me ask — do you already eat any of those, or do we need to customize based on your preferences?""",

        """Got it — not a fan of chicken or turkey? Totally fine.  
Let’s try some alternatives:

• Greek yogurt (plain or flavored)  
• Whey or plant-based protein shakes  
• Lean beef (90%+ lean)  
• Eggs and egg whites  
• Seafood — salmon, tuna, shrimp  
• Tempeh or tofu if you’re plant-based

Protein isn’t one-size-fits-all. We’ve got options.  
What *do* you like? Or are we playing the "No, not that either" game? 😉""",

        """Okay, let’s be honest — you don’t like chicken, turkey, eggs, yogurt, fish, beef, or tofu?  
At this point, I have to ask... do you like *any* food that isn’t bread or cereal?

Let’s try this:  
**Make a list of 3 foods you DO like**, and I’ll tell you how to make them higher in protein.

And remember — **variety is the spice of life**, but **discipline is what gets you results**. When I’m focused on a goal, I rotate between:

• Grilled chicken  
• Ground turkey  
• Egg whites  
• Lean steak  
• Vanilla whey isolate shakes (easy, zero prep)

It’s not about loving every meal. It’s about getting results. 💪""",

        """Alright, we’ve played the protein elimination game long enough 😂  
You don’t like anything I’ve listed — so let me flip it:

**What *do* you like that has more than 10g of protein per serving?**  
No, cereal and peanut butter don’t count.

Here’s the deal:  
• If you're serious about your goals, you'll find 2–3 protein sources and lock in.  
• If you're just window shopping fitness, keep playing the "not that one" game. 😏

**Choose results, not excuses.** I'm here to help when you're ready to commit.""",
    ]

    strike = st.session_state["protein_strikes"]
    st.session_state["protein_strikes"] += 1

    if strike >= len(responses):
        strike = len(responses) - 1  # cap at final snarky response

    return responses[strike]

# Water/hydration questions - simplified
if any(word in query_lower for word in ["water", "hydration", "drink", "fluid", "how much water"]):
    return """**My simple hydration rule: At least 1 gallon of water daily.**

**Easy to remember:**
• **1 gallon = 128 ounces = 16 cups**
• **Or aim for 8-10 glasses of 16oz each**
• **Start with 16-20oz when you wake up**

**Simple hydration tips:**
• **Drink before you're thirsty**
• **More if you're active** or it's hot outside
• **Light yellow urine = you're good**
• **Clear urine = you're drinking too much**

**What counts:**
• Plain water (best choice)
• Herbal tea
• Coffee (in moderation)

**What doesn't help:**
• Alcohol (actually dehydrates you)
• High-sugar drinks

**Glen's reality check:** Don't overthink it. A gallon sounds like a lot, but spread it throughout the day and you'll feel amazing!

*Good hydration supports everything - energy, recovery, fat loss, and performance!*

**Follow-up question for you:** Are you currently trying to lose weight, or are you more focused on building muscle and strength? I can give you more specific advice based on your goals!"""

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

*Consistency beats perfection every single time.*

**Tell me:** What's your biggest obstacle to working out consistently - time, motivation, or not knowing what to do? I've helped thousands overcome each of these!"""

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

*I've seen this work for thousands of people over 25+ years.*

**I'm curious:** What's been your biggest struggle with weight loss in the past - staying motivated, finding time, or dealing with stress eating? I've got specific strategies for each challenge!"""

    # Meal timing
    if any(word in query_lower for word in ["when to eat", "meal timing", "how often eat", "when should i eat"]):
        return """**My meal timing and planning approach: Eat every 3-4 hours with strategic planning.**

**Simple weekly schedule that works:**
• **Breakfast:** Within 1 hour of waking (7-8am)
• **Lunch:** 4-5 hours later (12-1pm)
• **Dinner:** 4-5 hours after lunch (5-6pm)
• **Snacks:** Protein-based between meals if needed

**Weekly meal planning strategy:**
• **Sunday prep:** Plan and prep for the entire week
• **Batch cook proteins:** Chicken, turkey, eggs for multiple meals
• **Pre-cut vegetables:** Ready to grab throughout the week
• **Plan around your schedule:** Know your busy days ahead of time

**What matters most:**
• **Protein at every meal** - Non-negotiable foundation
• **Don't skip meals** - Leads to overeating and poor choices later
• **Last meal 2-3 hours before bed** - Better sleep and recovery
• **Consistency over perfection** - Same eating windows daily

**My personal approach:**
I eat 3 main meals + 1-2 protein snacks. This keeps my energy steady and prevents those blood sugar crashes that lead to grabbing whatever's convenient (usually junk).

**Weekly planning prevents disaster:** When you fail to plan your meals, you plan to fail. I've seen this pattern thousands of times - successful people plan their week on Sunday.

**Let me ask you this:** Do you struggle more with planning your meals for the week, or actually sticking to the plan once you make it? I've got specific solutions for both challenges!"""

    return None  # No quick answer found
    
    # Calorie/eating questions - broader detection
    if any(word in query_lower for word in ["calories", "calorie", "how much eat", "how many eat", "how much should i eat", "what should i eat", "bmr", "tdee", "how much food"]):
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

**👇 Use the calculator below to get your exact numbers! 👇**

**One more thing:** Are you dealing with any specific challenges like busy work schedules, family stress, or past diet failures? I've got targeted solutions for real-life obstacles!"""

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

*This approach has worked for thousands of my clients over 25+ years.*

**Quick question for you:** What's your biggest challenge with getting enough protein - is it meal prep time, cost, or just not knowing what to eat? I've got specific solutions for each!"""

    # Water/hydration questions - simplified
    if any(word in query_lower for word in ["water", "hydration", "drink", "fluid", "how much water"]):
        return """**My simple hydration rule: At least 1 gallon of water daily.**

**Easy to remember:**
• **1 gallon = 128 ounces = 16 cups**
• **Or aim for 8-10 glasses of 16oz each**
• **Start with 16-20oz when you wake up**

**Simple hydration tips:**
• **Drink before you're thirsty**
• **More if you're active** or it's hot outside
• **Light yellow urine = you're good**
• **Clear urine = you're drinking too much**

**What counts:**
• Plain water (best choice)
• Herbal tea
• Coffee (in moderation)

**What doesn't help:**
• Alcohol (actually dehydrates you)
• High-sugar drinks

**Glen's reality check:** Don't overthink it. A gallon sounds like a lot, but spread it throughout the day and you'll feel amazing!

*Good hydration supports everything - energy, recovery, fat loss, and performance!*

**Follow-up question for you:** Are you currently trying to lose weight, or are you more focused on building muscle and strength? I can give you more specific advice based on your goals!"""

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

*Consistency beats perfection every single time.*

**Tell me:** What's your biggest obstacle to working out consistently - time, motivation, or not knowing what to do? I've helped thousands overcome each of these!"""

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

*I've seen this work for thousands of people over 25+ years.*

**I'm curious:** What's been your biggest struggle with weight loss in the past - staying motivated, finding time, or dealing with stress eating? I've got specific strategies for each challenge!"""

    # Meal timing
    if any(word in query_lower for word in ["when to eat", "meal timing", "how often eat", "when should i eat"]):
        return """**My meal timing and planning approach: Eat every 3-4 hours with strategic planning.**

**Simple weekly schedule that works:**
• **Breakfast:** Within 1 hour of waking (7-8am)
• **Lunch:** 4-5 hours later (12-1pm)
• **Dinner:** 4-5 hours after lunch (5-6pm)
• **Snacks:** Protein-based between meals if needed

**Weekly meal planning strategy:**
• **Sunday prep:** Plan and prep for the entire week
• **Batch cook proteins:** Chicken, turkey, eggs for multiple meals
• **Pre-cut vegetables:** Ready to grab throughout the week
• **Plan around your schedule:** Know your busy days ahead of time

**What matters most:**
• **Protein at every meal** - Non-negotiable foundation
• **Don't skip meals** - Leads to overeating and poor choices later
• **Last meal 2-3 hours before bed** - Better sleep and recovery
• **Consistency over perfection** - Same eating windows daily

**My personal approach:**
I eat 3 main meals + 1-2 protein snacks. This keeps my energy steady and prevents those blood sugar crashes that lead to grabbing whatever's convenient (usually junk).

**Weekly planning prevents disaster:** When you fail to plan your meals, you plan to fail. I've seen this pattern thousands of times - successful people plan their week on Sunday.

**Let me ask you this:** Do you struggle more with planning your meals for the week, or actually sticking to the plan once you make it? I've got specific solutions for both challenges!"""

    return None  # No quick answer found

def analyze_query_intent(query: str) -> dict:
    """Analyze query intent for better routing"""
    query_lower = query.lower()
    
    # Analyze "how old" questions with context
    if "how old" in query_lower:
        if any(word in query_lower for word in ["you", "glen", "your"]):
            # About Glen's age/background
            return {"type": "personal_glen", "confidence": 0.9}
        elif any(word in query_lower for word in ["i", "me", "my", "can i", "should i", "someone", "person", "people", "start", "begin"]):
            # About age to start fitness
            return {"type": "age_fitness", "confidence": 0.8}
        else:
            # General age question - default to fitness
            return {"type": "age_fitness", "confidence": 0.6}
    
    # Age-related fitness questions
    age_fitness_patterns = [
        "what age", "too old", "getting older", "older adults", "start at", "begin at",
        "metabolism slow", "slow metabolism", "age 40", "age 50", "age 60", "after 40",
        "can someone", "can people", "never too late", "starting late"
    ]
    if any(pattern in query_lower for pattern in age_fitness_patterns):
        return {"type": "age_fitness", "confidence": 0.8}
    
    # Personal Glen questions
    personal_patterns = [
        "who are you", "tell me about you", "your story", "your background", 
        "what do you bench", "what do you squat", "your records", "your fighting",
        "your hobbies", "for fun", "your family", "moose", "your dog"
    ]
    if any(pattern in query_lower for pattern in personal_patterns):
        return {"type": "personal_glen", "confidence": 0.9}
    
    # Motivation/mentor questions
    motivation_patterns = [
        "who motivates you", "your motivation", "who inspires you", "mentor", "role model",
        "inspirational", "who taught you", "learned from", "influenced you"
    ]
    if any(pattern in query_lower for pattern in motivation_patterns):
        return {"type": "motivation_mentors", "confidence": 0.9}
    
    # Default to general search
    return {"type": "general", "confidence": 0.3}

def calculate_relevance(query: str, topic: str, response: str, tags: List[str], keywords: List[str]) -> float:
    """Enhanced relevance calculation"""
    score = 0.0
    query_words = query.split()
    
    # Exact matches get highest scores
    if query.lower() in topic.lower():
        score += 15
    if query.lower() in response.lower():
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

def search_all_knowledge_bases(query: str, data: Dict[str, Any], click_counter: int = 0) -> List[Dict[str, Any]]:
    """Search through ALL knowledge bases with improved keyword matching and response tracking"""
    logger.debug(f"Processing query: {query}, click_counter: {click_counter}")
    if not data:
        logger.warning("No data found in knowledge bases")
        return []
    
    query_lower = query.lower()
    all_results = []
    
    # Better keyword detection for specific topics
    motivation_keywords = ['motivation', 'motivate', 'inspire', 'mentor', 'who is your motivation', 'who motivates you', 'inspirational', 'role model']
    age_keywords = ['age', 'old', 'older', 'aging', 'what age', 'how old', 'getting older', 'metabolism', 'slow metabolism']
    personal_keywords = ['you', 'your', 'yourself', 'tell me about', 'background', 'story', 'personal', 'who are you']
    
    is_motivation_query = any(keyword in query_lower for keyword in motivation_keywords)
    is_age_query = any(keyword in query_lower for keyword in age_keywords)
    is_personal_query = any(keyword in query_lower for keyword in personal_keywords)
    
    # Create a more specific topic key
    if is_motivation_query:
        topic_key = f"motivation_and_mindset_{click_counter}"
    elif is_age_query:
        topic_key = f"age_metabolism_{click_counter}"
    elif is_personal_query:
        topic_key = f"personal_glen_{click_counter}"
    else:
        topic_key = f"{query_lower.strip()}_{click_counter}"
    
    logger.debug(f"Generated topic_key: {topic_key}")
    
    # Search through all book categories
    for book_category, book_data in data.items():
        if not isinstance(book_data, dict) or 'content' not in str(book_data):
            logger.debug(f"Skipping invalid book category: {book_category}")
            continue
            
        # Skip metadata
        if book_category in ['source', 'author_context']:
            continue
        
        # Search through all sections in this book
        for section_name, section_data in book_data.items():
            if section_name in ['source', 'author_context'] or not isinstance(section_data, dict):
                logger.debug(f"Skipping invalid section: {section_name}")
                continue
                
            tags = section_data.get('tags', [])
            keywords = section_data.get('keywords', [])
            content_items = section_data.get('content', [])
            
            # Enhanced matching logic
            tag_match = any(tag.lower() in query_lower or query_lower in tag.lower() for tag in tags)
            keyword_match = any(keyword.lower() in query_lower or query_lower in keyword.lower() for keyword in keywords)
            
            # Special handling for specific query types
            section_match = False
            if is_motivation_query and section_name == 'motivation_and_mindset':
                section_match = True
                logger.debug(f"Section match for motivation_and_mindset")
            elif is_age_query and section_name == 'age_and_metabolism':
                section_match = True
                logger.debug(f"Section match for age_and_metabolism")
            elif is_personal_query and section_name == 'personal_glen_stories':
                section_match = True
                logger.debug(f"Section match for personal_glen_stories")
            
            # Search through content items
            for item in content_items:
                topic = item.get('topic', '')
                response = item.get('response', '')
                
                # Calculate relevance with better scoring
                topic_match = query_lower in topic.lower() or any(word in topic.lower() for word in query_lower.split())
                response_match = query_lower in response.lower() or any(word in response.lower() for word in query_lower.split())
                
                relevance_score = calculate_relevance(query_lower, topic, response, tags, keywords)
                
                # Boost relevance for section matches
                if section_match:
                    relevance_score += 20
                
                if tag_match or keyword_match or topic_match or response_match or section_match:
                    response_id = f"{section_name}_{topic.replace(' ', '_')}"
                    all_results.append({
                        'book_category': book_category.replace('_book_data', '').replace('_', ' ').title(),
                        'section': section_name.replace('_', ' ').title(),
                        'topic': topic,
                        'response': response,
                        'relevance_score': relevance_score,
                        'is_personal_story': section_name == 'personal_journey_lessons',
                        'response_id': response_id,
                        'topic_key': topic_key
                    })
    
    # Sort by relevance
    all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    logger.debug(f"Found {len(all_results)} total results")
    logger.debug(f"All response IDs: {[r['response_id'] for r in all_results]}")
    
    # Smart response filtering based on session state
    topic_responses_key = f"used_responses_{topic_key}"
    if topic_responses_key not in st.session_state:
        st.session_state[topic_responses_key] = set()
    
    # Filter out already used responses for this specific topic
    used_response_ids = st.session_state[topic_responses_key]
    unused_results = [r for r in all_results if r['response_id'] not in used_response_ids]
    logger.debug(f"Unused results: {len(unused_results)}, Used response IDs: {used_response_ids}")
    
    # Reset used responses if all are exhausted
    if not unused_results:
        logger.info(f"All responses used for topic_key: {topic_key}, resetting used responses")
        st.session_state[topic_responses_key] = set()
        unused_results = all_results
    
    # Randomize for motivation queries
    if is_motivation_query:
        random.shuffle(unused_results)
        logger.debug("Shuffled results for motivation query")
    
    # Return top result (or empty list if none)
    if unused_results:
        selected_result = unused_results[0]
        st.session_state[topic_responses_key].add(selected_result['response_id'])
        logger.debug(f"Selected response: {selected_result['topic']} (ID: {selected_result['response_id']})")
        return [selected_result]
    
    logger.warning("No matching results found")
    return []

def add_strategic_followup(response_text: str, query: str) -> str:
    """Add strategic follow-up questions to keep the conversation flowing"""
    query_lower = query.lower()
    
    # Don't add follow-ups to responses that already have questions
    if "?" in response_text[-100:]:  # Check last 100 characters
        return response_text
    
    # Topic-specific follow-up questions
    followup_questions = []
    
    # Nutrition/Diet related
    if any(word in query_lower for word in ["eat", "food", "nutrition", "diet", "meal", "calories", "protein"]):
        followup_questions = [
            "What's your biggest nutrition challenge right now - meal prep, eating out too much, or late-night snacking?",
            "Are you dealing with stress eating, or do you struggle more with finding time to cook healthy meals?",
            "What's been your biggest obstacle to eating consistently - busy schedule, family preferences, or knowing what to cook?",
            "Do you find it harder to stick to your nutrition on weekdays with work stress, or weekends with social events?",
            "What derails your healthy eating most - work deadlines, family chaos, or just getting bored with the same foods?"
        ]
    
    # Exercise/Training related
    elif any(word in query_lower for word in ["workout", "exercise", "train", "gym", "fitness", "muscle", "strength"]):
        followup_questions = [
            "What's your biggest barrier to consistent workouts - time constraints, motivation, or not knowing what to do?",
            "Do you struggle more with finding time to exercise, or staying motivated when you do have time?",
            "What's been your biggest challenge with fitness - sticking to a routine, seeing results, or dealing with injuries?",
            "Are you more frustrated by lack of progress, or by not being able to stay consistent with your workouts?",
            "What stops you from working out most often - energy levels, time management, or just not enjoying it?"
        ]
    
    # Weight loss related
    elif any(word in query_lower for word in ["weight", "lose", "fat", "pounds", "scale"]):
        followup_questions = [
            "What's been your biggest weight loss obstacle - staying motivated, dealing with plateaus, or managing stress eating?",
            "Do you struggle more with the diet side or the exercise side of weight loss?",
            "What derails your weight loss efforts most - social situations, work stress, or family responsibilities?",
            "Are you dealing with emotional eating, or do you struggle more with consistency and routine?",
            "What's your biggest frustration - slow progress, lack of energy, or feeling overwhelmed by all the conflicting advice?"
        ]
    
    # Motivation/Psychology related
    elif any(word in query_lower for word in ["motivation", "mindset", "stress", "habit", "goal", "struggle"]):
        followup_questions = [
            "What's the biggest thing that kills your motivation - setbacks, comparing yourself to others, or feeling overwhelmed?",
            "Do you struggle more with starting new habits, or maintaining them once you get going?",
            "What's your biggest source of stress that impacts your health goals - work, family, or financial pressures?",
            "Are you dealing with perfectionism that holds you back, or more with inconsistency and starting over?",
            "What's been your pattern with past goals - starting strong then fading, or never quite getting started?"
        ]
    
    # Hydration/Water related
    elif any(word in query_lower for word in ["water", "drink", "hydration"]):
        followup_questions = [
            "What's your biggest hydration challenge - remembering to drink water, or just not liking the taste of plain water?",
            "Do you struggle more with drinking enough during busy workdays, or maintaining hydration during workouts?",
            "Are you trying to lose weight, build muscle, or just feel more energetic throughout the day?"
        ]
    
    # General/Other topics
    else:
        followup_questions = [
            "What's your main health and fitness goal right now - losing weight, building strength, or just feeling better overall?",
            "What's been your biggest challenge in reaching your fitness goals - time, motivation, or knowing what to do?",
            "Are you dealing more with nutrition struggles, workout consistency, or motivation and mindset issues?",
            "What aspect of your health journey frustrates you most - slow progress, lack of time, or conflicting information?",
            "Do you struggle more with getting started on healthy habits, or maintaining them once you begin?"
        ]
    
    # Select a random follow-up question
    followup = random.choice(followup_questions)
    
    # Add the follow-up in Glen's conversational style
    return f"{response_text}\n\n**Let me ask you this:** {followup} I've got specific strategies for whatever you're dealing with!"

def add_glen_personality(response_text: str) -> str:
    """Add Glen's personal touch to responses - but avoid repetition"""
    
    # Only add personality if response doesn't already have Glen's voice
    if "glen" in response_text.lower() or "my" in response_text.lower() or "i've" in response_text.lower():
        return response_text  # Already has personality, don't add more
    
    # Add personality based on content - but keep it unique
    if "protein" in response_text.lower() and "blood work" not in response_text.lower():
        response_text += "\n\n*In my experience, this protein approach has been safe and effective for thousands of clients.*"
    
    elif any(word in response_text.lower() for word in ["stress", "motivation", "mindset"]) and "client experience" not in response_text.lower():
        response_text += "\n\n*From my 25+ years of working with people, I've learned that mindset is often the missing piece.*"
    
    elif "training" in response_text.lower() or "exercise" in response_text.lower():
        if "3:30am" not in response_text.lower():
            response_text += "\n\n*The key is finding a routine that works for YOUR life and schedule.*"
    
    return response_text

def format_glen_response(results: List[Dict[str, Any]], query: str = "") -> str:
    """Format the search results as if Glen is personally responding"""
    
    # First check for quick answers to common questions
    quick_answer = get_quick_answer(query)
    if quick_answer:
        return quick_answer
    
    # Check if topic is exhausted
    intent = analyze_query_intent(query)
    topic_key = intent["type"]
    exhausted_key = f"exhausted_{topic_key}"
    
    if st.session_state.get(exhausted_key, False):
        # Topic exhausted - give Glen's "enough already" message
        exhausted_responses = [
            "Alright, alright! I think you've gotten all my wisdom on this topic. Time to shit or get off the pot - pick a different question or actually DO something with what I've told you!",
            "Hey, we've covered this ground pretty thoroughly! How about we talk about something else, or better yet, go apply what you've learned? Action beats analysis paralysis every time!",
            "I've given you everything I've got on this one! Time to stop clicking buttons and start lifting weights. What else can I help you with?",
            "You've officially exhausted my knowledge bank on this topic! That means it's time to stop researching and start doing. What's your next move going to be?",
            "Okay, you've definitely gotten your money's worth on this subject! Time to take action instead of asking the same question fifty different ways. What else is on your mind?"
        ]
        
        return f"{random.choice(exhausted_responses)}\n\n**Let me ask you this:** What's holding you back from actually implementing what you've learned? I've got strategies to get you moving!"
    
    # If no results, proceed with encouraging response
    if not results:
        encouraging_responses = [
            "Let's tackle this together! Even if that specific topic isn't in my current materials, I've helped thousands of people with similar challenges.",
            "Great question! While I might not have that exact info loaded right now, my 25+ years of experience tells me we can definitely figure this out.",
            "I love that you're asking the tough questions! That's exactly the mindset that leads to real transformation.",
            "You know what? That's the kind of question that shows you're ready to make real changes. Let's dive deeper into what's really going on."
        ]
        
        solution_focused_options = [
            "Here's what I always tell my clients: the best answers come from understanding YOUR specific situation.",
            "After 25+ years of coaching, I've learned that every person's journey is unique - let's figure out yours.",
            "The fact that you're asking shows you're ready to take action. That's half the battle right there!",
            "I've seen this pattern before - when someone asks questions like this, they're usually closer to a breakthrough than they think."
        ]
        
        action_oriented_closers = [
            "Let's start with what's working and what's not working for you right now.",
            "Tell me more about your specific situation and I'll give you a roadmap.",
            "What's your biggest frustration with your current approach? I've got solutions.",
            "Let's get specific about your goals and obstacles - that's where the magic happens."
        ]
        
        base_response = f"{random.choice(encouraging_responses)} {random.choice(solution_focused_options)}"
        
        actionable_topics = [
            "**🎯 Your Weight Loss Goals** - What's your target and timeline?",
            "**💪 Your Current Routine** - What's working and what's not?", 
            "**🍖 Your Nutrition Approach** - Are you tracking anything right now?",
            "**⚡ Your Energy Levels** - How do you feel throughout the day?",
            "**🧠 Your Motivation** - What gets you fired up vs what drains you?",
            "**⏰ Your Schedule** - What does a typical day look like for you?"
        ]
        
        response = f"{base_response}\n\n**Let's dig into what matters most:**\n"
        for topic in actionable_topics:
            response += f"• {topic}\n"
        
        response += f"\n**Here's what I know for sure:** Every successful transformation starts with understanding where you are right now. {random.choice(action_oriented_closers)}"
        
        # Add strategic follow-up
        response = add_strategic_followup(response, query)
        
        return response
    
    # We have results - format them properly with rotating openings
    personal_openings = [
        "In my experience working with thousands of clients...",
        "From my 25+ years in this field, here's what I know...",
        "Based on my background as a trainer and former competitor...",
        "After helping people transform for over two decades...",
        "From my time owning Wisconsin Barbell Gym, I've learned..."
    ]
    
    response = f"**{random.choice(personal_openings)}**\n\n"
    
    # Add the MAIN content
    main_result = results[0]
    enhanced_response = add_glen_personality(main_result['response'])
    
    response += f"### 🎯 {main_result['topic']}\n\n{enhanced_response}\n\n"
    
    # Add personal signature
    signatures = [
        "---\n*This comes from my 17+ years as a gym owner, personal trainer, and former competitive lifter. Every piece of advice is battle-tested with real clients.*",
        "---\n*Hope this helps! This approach has worked for thousands of my clients at Wisconsin Barbell Gym.*",
        "---\n*These insights combine my competition experience, training expertise, and 25+ years of understanding what motivates people.*"
    ]
    
    response += random.choice(signatures)
    
    # Add strategic follow-up
    response = add_strategic_followup(response, query)
    
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
    if "calculated_results" not in st.session_state:
        st.session_state.calculated_results = None
    if "used_responses" not in st.session_state:
        st.session_state.used_responses = set()
    if "exhausted_topics" not in st.session_state:
        st.session_state.exhausted_topics = set()
    
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
        # Show calorie calculator first if needed
        if st.session_state.show_calculator:
            show_calorie_calculator()
            st.markdown("---")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input at the bottom
        prompt = st.chat_input("💬 Ask Glen anything about fitness, nutrition, or motivation...")
        
        if prompt:
            # Clear previous messages for fresh start
            st.session_state.messages = []
            st.session_state.show_calculator = False
            
            # Add new user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Process the response
            with st.spinner("🧠 Glen is thinking..."):
                results = search_all_knowledge_bases(prompt, data)
                response = format_glen_response(results, prompt)
                
                # Check if response mentions calculator and set flag
                if "calculator below" in response.lower() or "use the calculator" in response.lower():
                    st.session_state.show_calculator = True
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Use rerun
            st.rerun()
    
    with col2:
        # Show sticky calculator results if available
        if st.session_state.calculated_results:
            results = st.session_state.calculated_results
            
            st.markdown("### 📊 **Your Numbers**")
            st.markdown(f"*{results['weight']} lbs, {results['height_ft']}'{results['height_in']}\", {results['age']}yr, {results['gender'].lower()}*")
            
            # Compact metrics in sidebar
            st.metric("🔥 BMR", f"{results['bmr']:,}")
            st.metric("⚡ TDEE", f"{results['tdee']:,}")
            st.metric("🎯 Target", f"{results['weight_loss']:,}")
            st.metric("🍖 Protein", f"{results['protein_grams']}g")
            
            if st.button("🗑️ Clear Results", key="clear_calc"):
                st.session_state.calculated_results = None
                st.rerun()
            
            st.markdown("---")
        
        st.markdown("### 🚀 Quick Start")
        st.markdown("**New here? Try these:**")
        
        quick_buttons = [
            ("💪 Master Plan", "Tell me about the 12-week master plan"),
            ("🧠 Motivation", "How can you help me stay motivated?"),
            ("🥗 Nutrition", "What should I know about protein and nutrition?"),
            ("🔥 Get Moving", "I need to stop analyzing and start doing!")
        ]
        
        for label, query in quick_buttons:
            if st.button(label, key=f"quick_{label}"):
                # Clear previous messages for fresh start
                st.session_state.messages = []
                st.session_state.show_calculator = False
                
                # Simple counter for this specific button
                counter_key = f"button_clicks_{label}"
                if counter_key not in st.session_state:
                    st.session_state[counter_key] = 0
                st.session_state[counter_key] += 1
                click_number = st.session_state[counter_key]
                
                # Log button click
                logger.debug(f"Button clicked: {label}, Query: {query}, Click number: {click_number}")
                
                # Get content using search_all_knowledge_bases
                results = search_all_knowledge_bases(query, data, click_number)
                
                if results:
                    logger.debug(f"Found content - Topic: {results[0].get('topic', 'NONE')}, Section: {results[0].get('section', 'NONE')}, Response ID: {results[0].get('response_id', 'NONE')}")
                else:
                    logger.debug("NO CONTENT RETURNED!")
                
                response = format_glen_response(results, query)
                
                # Check if response mentions calculator
                if "calculator below" in response.lower() or "use the calculator" in response.lower():
                    st.session_state.show_calculator = True
                
                # Add to messages
                st.session_state.messages.append({"role": "user", "content": query})
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
        "When should I eat and plan my meals?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        col = cols[i % 3]
        if col.button(question, key=f"example_{i}"):
            # Clear previous messages for fresh start
            st.session_state.messages = []
            
            # Reset calculator for new topics
            st.session_state.show_calculator = False
            
            st.session_state.messages.append({"role": "user", "content": question})
            results = search_all_knowledge_bases(question, data)
            response = format_glen_response(results, question)
            
            # Check if response mentions calculator and set flag
            if "calculator below" in response.lower() or "use the calculator" in response.lower():
                st.session_state.show_calculator = True
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
