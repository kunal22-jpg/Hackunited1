from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# User Models
class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    age: int
    gender: str
    height: float
    weight: float
    allergies: List[str] = []
    chronic_conditions: List[str] = []
    goals: List[str] = []
    fitness_level: str
    diet_type: str
    skin_type: str
    smart_cart_enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProfileCreate(BaseModel):
    name: str
    email: str
    age: int
    gender: str
    height: float
    weight: float
    allergies: List[str] = []
    chronic_conditions: List[str] = []
    goals: List[str] = []
    fitness_level: str
    diet_type: str
    skin_type: str
    smart_cart_enabled: bool = True

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatMessageCreate(BaseModel):
    user_id: str
    message: str

class WorkoutPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    muscle_groups: List[str]
    equipment: List[str]
    duration: int
    difficulty: str
    video_url: str
    instructions: List[str]

class SkincareRoutine(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    skin_type: str
    time_of_day: str
    steps: List[str]
    products: List[str]
    video_url: str

class MealPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    diet_type: str
    calories: int
    macros: dict
    ingredients: List[str]
    instructions: List[str]
    prep_time: int

class HealthConditionPlan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    condition: str
    title: str
    description: str
    daily_routine: List[str]
    lifestyle_tips: List[str]
    video_url: str

# Sample data initialization
@api_router.on_event("startup")
async def init_sample_data():
    # Check if sample data exists
    existing_workouts = await db.workouts.count_documents({})
    if existing_workouts == 0:
        # Initialize sample workouts
        sample_workouts = [
            {
                "id": str(uuid.uuid4()),
                "title": "Upper Body Blast",
                "description": "Intense upper body workout targeting chest, back, and arms",
                "muscle_groups": ["chest", "back", "arms"],
                "equipment": ["dumbbells", "bench"],
                "duration": 45,
                "difficulty": "intermediate",
                "video_url": "https://www.youtube.com/watch?v=sample1",
                "instructions": ["Warm up for 5 minutes", "3 sets of push-ups", "3 sets of rows", "Cool down"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Core Strength",
                "description": "Build a strong core with targeted exercises",
                "muscle_groups": ["core", "abs"],
                "equipment": ["mat"],
                "duration": 30,
                "difficulty": "beginner",
                "video_url": "https://www.youtube.com/watch?v=sample2",
                "instructions": ["Warm up", "Planks 3x60s", "Crunches 3x20", "Mountain climbers 3x15"]
            },
            {
                "id": str(uuid.uuid4()),
                "title": "HIIT Cardio",
                "description": "High-intensity interval training for fat burn",
                "muscle_groups": ["full body"],
                "equipment": ["none"],
                "duration": 25,
                "difficulty": "advanced",
                "video_url": "https://www.youtube.com/watch?v=sample3",
                "instructions": ["5 min warm up", "20s work/10s rest intervals", "Cool down stretches"]
            }
        ]
        await db.workouts.insert_many(sample_workouts)

        # Initialize sample skincare routines
        sample_skincare = [
            {
                "id": str(uuid.uuid4()),
                "title": "Morning Glow Routine",
                "description": "Start your day with radiant skin",
                "skin_type": "normal",
                "time_of_day": "morning",
                "steps": ["Gentle cleanser", "Vitamin C serum", "Moisturizer", "SPF 30+"],
                "products": ["CeraVe Foaming Cleanser", "The Ordinary Vitamin C", "Neutrogena Hydro Boost"],
                "video_url": "https://www.youtube.com/watch?v=skincare1"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Acne-Fighting Routine",
                "description": "Combat breakouts with targeted treatment",
                "skin_type": "acne-prone",
                "time_of_day": "evening",
                "steps": ["Salicylic acid cleanser", "Niacinamide serum", "Benzoyl peroxide spot treatment", "Light moisturizer"],
                "products": ["Paula's Choice BHA", "The Ordinary Niacinamide", "La Roche-Posay Effaclar"],
                "video_url": "https://www.youtube.com/watch?v=skincare2"
            }
        ]
        await db.skincare.insert_many(sample_skincare)

        # Initialize sample meal plans
        sample_meals = [
            {
                "id": str(uuid.uuid4()),
                "title": "High Protein Power Bowl",
                "description": "Muscle-building meal with complete nutrition",
                "diet_type": "high-protein",
                "calories": 650,
                "macros": {"protein": 45, "carbs": 35, "fat": 25},
                "ingredients": ["chicken breast", "quinoa", "black beans", "avocado", "vegetables"],
                "instructions": ["Grill chicken", "Cook quinoa", "Assemble bowl", "Add dressing"],
                "prep_time": 25
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Keto Fat Bomb Salad",
                "description": "Low-carb, high-fat satisfying meal",
                "diet_type": "keto",
                "calories": 580,
                "macros": {"protein": 25, "carbs": 5, "fat": 70},
                "ingredients": ["salmon", "avocado", "olive oil", "nuts", "leafy greens"],
                "instructions": ["Prepare salmon", "Mix salad", "Add healthy fats", "Serve immediately"],
                "prep_time": 15
            }
        ]
        await db.meals.insert_many(sample_meals)

        # Initialize health condition plans
        sample_health = [
            {
                "id": str(uuid.uuid4()),
                "condition": "PCOS",
                "title": "PCOS Management Plan",
                "description": "Holistic approach to managing PCOS symptoms",
                "daily_routine": ["30 min moderate exercise", "Balanced low-GI meals", "Stress management", "Quality sleep"],
                "lifestyle_tips": ["Limit processed foods", "Include omega-3s", "Regular meal timing", "Mindfulness practice"],
                "video_url": "https://www.youtube.com/watch?v=pcos1"
            },
            {
                "id": str(uuid.uuid4()),
                "condition": "Diabetes",
                "title": "Diabetes Wellness Plan",
                "description": "Daily routine for blood sugar management",
                "daily_routine": ["Check blood glucose", "Balanced meals", "Regular exercise", "Medication adherence"],
                "lifestyle_tips": ["Carb counting", "Regular doctor visits", "Foot care", "Stay hydrated"],
                "video_url": "https://www.youtube.com/watch?v=diabetes1"
            }
        ]
        await db.health_conditions.insert_many(sample_health)

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Nutracía AI Wellness API is running"}

@api_router.post("/users", response_model=UserProfile)
async def create_user(user_data: UserProfileCreate):
    user_dict = user_data.dict()
    user_obj = UserProfile(**user_dict)
    await db.users.insert_one(user_obj.dict())
    return user_obj

@api_router.get("/users/{user_id}", response_model=UserProfile)
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)

@api_router.get("/workouts", response_model=List[WorkoutPlan])
async def get_workouts():
    workouts = await db.workouts.find().to_list(1000)
    return [WorkoutPlan(**workout) for workout in workouts]

@api_router.get("/skincare", response_model=List[SkincareRoutine])
async def get_skincare():
    routines = await db.skincare.find().to_list(1000)
    return [SkincareRoutine(**routine) for routine in routines]

@api_router.get("/meals", response_model=List[MealPlan])
async def get_meals():
    meals = await db.meals.find().to_list(1000)
    return [MealPlan(**meal) for meal in meals]

@api_router.get("/health-conditions", response_model=List[HealthConditionPlan])
async def get_health_conditions():
    conditions = await db.health_conditions.find().to_list(1000)
    return [HealthConditionPlan(**condition) for condition in conditions]

# Enhanced Health Chatbot Models
class HealthChatRequest(BaseModel):
    user_id: str
    message: str
    user_profile: Optional[dict] = None  # Contains weight, allergies, skin_concern, etc.

class HealthChatResponse(BaseModel):
    response: str
    message_id: str
    requires_profile: bool = False
    profile_fields: List[str] = []

# Health Knowledge Base
HEALTH_KNOWLEDGE_BASE = """
You are Nutracía AI Health Coach, an expert in fitness, nutrition, and skincare. You provide personalized recommendations based on:

WORKOUT EXPERTISE:
- Custom exercises, sets, reps, and weekly schedules
- Strength training, cardio, HIIT, flexibility
- Equipment-based and bodyweight workouts
- Progress tracking and goal setting

SKINCARE EXPERTISE:
- Morning and evening routines
- Product recommendations for different skin types
- Acne, anti-aging, tanning, dry skin solutions
- Ingredient knowledge and sun protection

NUTRITION EXPERTISE:
- Meal planning and diet recommendations
- Allergy-conscious nutrition advice
- Weight management strategies
- Macronutrient balance and hydration

Always ask for user details (weight, allergies, skin concerns) when providing personalized advice.
Keep responses conversational, encouraging, and practical.
"""

@api_router.post("/chat", response_model=HealthChatResponse)
async def health_chat_ai(chat_data: HealthChatRequest):
    """Enhanced AI health chatbot with intelligent health responses"""
    try:
        # Check if we need user profile for personalized advice
        needs_personal_info = any(keyword in chat_data.message.lower() for keyword in [
            'workout', 'exercise', 'diet', 'nutrition', 'skincare', 'routine', 
            'recommend', 'plan', 'personalized', 'custom', 'my', 'help me'
        ])
        
        if needs_personal_info and not chat_data.user_profile:
            return HealthChatResponse(
                response="I'd love to help you with personalized health advice! To give you the best recommendations, I need to know a bit about you. Could you please share your weight, any allergies you have, and your main skin concern?",
                message_id=str(uuid.uuid4()),
                requires_profile=True,
                profile_fields=["weight", "allergies", "skin_concern"]
            )
        
        # Generate intelligent health responses based on message content and profile
        response_text = generate_health_response(chat_data.message, chat_data.user_profile)
        
        # Store chat history
        chat_obj = ChatMessage(
            user_id=chat_data.user_id,
            message=chat_data.message,
            response=response_text
        )
        await db.chat_history.insert_one(chat_obj.dict())
        
        return HealthChatResponse(
            response=response_text,
            message_id=chat_obj.id,
            requires_profile=False,
            profile_fields=[]
        )
        
    except Exception as e:
        print(f"Error in health chat: {str(e)}")
        # Fallback response
        fallback_response = "I'm here to help with your health and wellness journey! I can provide advice on workouts, nutrition, and skincare. What would you like to know?"
        
        chat_obj = ChatMessage(
            user_id=chat_data.user_id,
            message=chat_data.message,
            response=fallback_response
        )
        await db.chat_history.insert_one(chat_obj.dict())
        
        return HealthChatResponse(
            response=fallback_response, 
            message_id=chat_obj.id
        )

def generate_health_response(message: str, user_profile: Optional[dict] = None):
    """Generate intelligent health responses based on keywords and user profile"""
    message_lower = message.lower()
    
    # Extract user profile info if available
    weight = user_profile.get('weight', 'not specified') if user_profile else 'not specified'
    allergies = user_profile.get('allergies', 'none') if user_profile else 'none'
    skin_concern = user_profile.get('skin_concern', 'general care') if user_profile else 'general care'
    
    # Workout/Exercise responses
    if any(word in message_lower for word in ['workout', 'exercise', 'muscle', 'fitness', 'training', 'gym']):
        if 'muscle' in message_lower or 'strength' in message_lower:
            return f"""💪 **Muscle Building Workout Plan** (Weight: {weight})

**Recommended Routine:**
• **Compound Exercises:** Squats, deadlifts, bench press, pull-ups
• **Sets & Reps:** 3-4 sets of 8-12 reps
• **Frequency:** 3-4 times per week
• **Rest:** 48-72 hours between sessions

**For your weight ({weight}):**
- Start with bodyweight or light weights
- Focus on proper form before increasing weight
- Progressive overload is key

**Nutrition tip:** Ensure adequate protein intake (0.8-1g per kg body weight) and avoid {allergies} allergens.

Would you like a specific workout plan or have questions about nutrition?"""

        elif 'cardio' in message_lower or 'running' in message_lower:
            return f"""🏃‍♂️ **Cardio Training Plan** (Weight: {weight})

**Beginner Program:**
• **Week 1-2:** 20-30 min walking/light jogging
• **Week 3-4:** 30-40 min moderate pace
• **Week 5+:** Add interval training

**HIIT Option:**
- 5 min warm-up
- 30 sec high intensity / 90 sec recovery (repeat 8-10 times)
- 5 min cool-down

**Safety Note:** Start gradually and listen to your body. Stay hydrated!

Need help with nutrition for cardio performance?"""

        else:
            return f"""🏋️‍♀️ **General Fitness Plan** (Weight: {weight})

**Weekly Schedule:**
• **Monday:** Upper body strength
• **Tuesday:** Cardio (30 min)
• **Wednesday:** Lower body strength  
• **Thursday:** Rest or yoga
• **Friday:** Full body workout
• **Weekend:** Active recovery (walking, swimming)

**Key Principles:**
- Progressive overload
- Proper nutrition (avoiding {allergies})
- Adequate sleep (7-9 hours)
- Stay consistent!

What specific fitness goals would you like to work on?"""

    # Skincare responses
    elif any(word in message_lower for word in ['skincare', 'skin', 'acne', 'routine', 'face', 'moisturizer']):
        if skin_concern.lower() == 'acne':
            return f"""✨ **Acne-Fighting Skincare Routine** (Concern: {skin_concern})

**Morning Routine:**
1. Gentle foaming cleanser (salicylic acid)
2. Niacinamide serum
3. Light, oil-free moisturizer
4. SPF 30+ sunscreen

**Evening Routine:**
1. Double cleanse (oil cleanser + foaming cleanser)
2. BHA treatment (2-3x/week)
3. Hydrating serum
4. Night moisturizer

**Key Ingredients:** Salicylic acid, niacinamide, retinoids, hyaluronic acid

**Avoid:** Over-cleansing, harsh scrubs, picking at skin

Need product recommendations or have questions about specific ingredients?"""

        elif 'dry' in skin_concern.lower():
            return f"""💧 **Dry Skin Care Routine** (Concern: {skin_concern})

**Morning:**
1. Gentle cream cleanser
2. Hyaluronic acid serum
3. Rich moisturizer
4. SPF 30+

**Evening:**
1. Oil cleanser
2. Gentle cream cleanser
3. Retinol (2-3x/week)
4. Heavy night cream

**Weekly Treats:**
- Hydrating face mask (2x/week)
- Gentle exfoliation (1x/week)

**Tips:** Use a humidifier, drink plenty of water, avoid hot showers!

Want specific product recommendations for your skin type?"""

        else:
            return f"""✨ **General Skincare Routine** (Concern: {skin_concern})

**Basic 4-Step Routine:**
1. **Cleanse:** Morning & evening
2. **Treat:** Serums for specific concerns
3. **Moisturize:** Hydrate your skin
4. **Protect:** SPF during the day

**For {skin_concern}:**
- Use gentle, fragrance-free products
- Introduce new products slowly
- Consistency is key!

**Universal Tips:**
- Always patch test new products
- SPF is non-negotiable
- Listen to your skin

What specific skin concerns would you like to address?"""

    # Nutrition/Diet responses
    elif any(word in message_lower for word in ['diet', 'nutrition', 'food', 'eat', 'meal', 'protein', 'calories']):
        allergy_note = f" (avoiding {allergies})" if allergies != 'none' else ""
        
        if 'muscle' in message_lower or 'protein' in message_lower:
            return f"""🥗 **Muscle Building Nutrition** (Weight: {weight}){allergy_note}

**Daily Protein Target:** 1.6-2.2g per kg body weight

**Best Protein Sources:**
• Lean meats (chicken, turkey, lean beef)
• Fish and seafood
• Eggs and dairy
• Legumes and beans
• Protein powder (whey/plant-based)

**Sample Meal Plan:**
- **Breakfast:** Greek yogurt with berries and granola
- **Lunch:** Grilled chicken salad with quinoa
- **Snack:** Protein shake with banana
- **Dinner:** Salmon with sweet potato and vegetables

**Timing:** Eat protein within 30 minutes post-workout for optimal recovery.

{f'**Allergy Note:** Avoid {allergies} in all meal planning.' if allergies != 'none' else ''}

Need help creating a specific meal plan?"""

        elif 'weight' in message_lower and 'loss' in message_lower:
            return f"""⚖️ **Healthy Weight Management** (Current: {weight}){allergy_note}

**Key Principles:**
• Create a moderate caloric deficit (300-500 calories)
• Focus on whole, unprocessed foods
• Stay hydrated (8-10 glasses water/day)
• Regular physical activity

**Balanced Plate Method:**
- 1/2 plate: Non-starchy vegetables
- 1/4 plate: Lean protein
- 1/4 plate: Complex carbohydrates
- Healthy fats in moderation

**Foods to Emphasize:**
- Vegetables and fruits
- Lean proteins
- Whole grains
- Healthy fats (avocado, nuts, olive oil)

{f'**Important:** Avoid {allergies} in all food choices.' if allergies != 'none' else ''}

Want a personalized meal plan or calorie calculation?"""

        else:
            return f"""🍎 **Healthy Nutrition Guidelines** (Weight: {weight}){allergy_note}

**Balanced Diet Basics:**
• **Protein:** 20-30% of calories
• **Carbohydrates:** 45-65% of calories  
• **Fats:** 20-35% of calories

**Daily Essentials:**
- 5-9 servings fruits & vegetables
- 8 glasses of water
- Lean protein with every meal
- Healthy fats (omega-3s)

**Meal Timing:**
- Eat every 3-4 hours
- Don't skip breakfast
- Light dinner 2-3 hours before bed

{f'**Allergy Management:** Carefully avoid {allergies} and read all food labels.' if allergies != 'none' else ''}

What specific nutritional goals are you working toward?"""

    # General health responses
    elif any(word in message_lower for word in ['health', 'wellness', 'sleep', 'stress', 'energy', 'tired']):
        return f"""🌟 **Holistic Wellness Plan** (Profile: {weight}, {skin_concern}){' (Allergies: ' + allergies + ')' if allergies != 'none' else ''}

**5 Pillars of Health:**

1. **Physical Activity** 🏃‍♂️
   - 150 min moderate cardio/week
   - 2-3 strength training sessions
   - Daily movement and stretching

2. **Nutrition** 🥗
   - Balanced macronutrients
   - Plenty of water
   - Limit processed foods

3. **Sleep** 😴
   - 7-9 hours nightly
   - Consistent sleep schedule
   - Screen-free hour before bed

4. **Stress Management** 🧘‍♀️
   - Meditation or mindfulness
   - Regular breaks
   - Hobbies and social connection

5. **Preventive Care** 🩺
   - Regular check-ups
   - Skincare routine for {skin_concern}
   - Mental health awareness

**Daily Habits:**
- Morning sunlight exposure
- Healthy breakfast
- Movement breaks
- Evening wind-down routine

What area of wellness would you like to focus on first?"""

    # Default response for general questions
    else:
        return f"""👋 **Welcome to Your Health Journey!** 

I'm your personal health coach, and I'm here to help you with:

🏋️‍♀️ **Fitness & Workouts**
- Custom exercise plans
- Strength training guidance
- Cardio routines

✨ **Skincare & Beauty**
- Routines for {skin_concern}
- Product recommendations
- Skin health tips

🥗 **Nutrition & Diet**
- Meal planning {f'(avoiding {allergies})' if allergies != 'none' else ''}
- Healthy recipes
- Nutritional guidance

🌟 **Overall Wellness**
- Sleep optimization
- Stress management
- Healthy lifestyle tips

**Your Profile:** Weight: {weight} | Skin: {skin_concern} | Allergies: {allergies}

What would you like to know about? Just ask me about workouts, skincare, nutrition, or general health tips!"""

# Enhanced Grocery Agent - AI-Powered Shopping Assistant
import sys
import os
from typing import List
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config.settings import GEMINI_API_KEY
    from modules.user_preferences import get_user_preferences
    from modules.prompt_builder import build_recommendation_prompt
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    # Fallback if grocery agent modules are not available
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

class ShoppingRequest(BaseModel):
    query: str
    budget: Optional[int] = 500
    preferred_brands: Optional[List[str]] = ["MuscleBlaze", "Organic India"]
    diet: Optional[str] = "high protein"

class ProductRecommendation(BaseModel):
    name: str
    price: str
    description: str
    protein: Optional[str] = None
    rating: str
    platform: str
    selected: bool = False

@api_router.post("/grocery/recommendations")
async def get_grocery_recommendations(request: ShoppingRequest):
    """AI-powered grocery recommendations using Google Gemini"""
    try:
        try:
            # Get user preferences (fallback if module not available)
            user_prefs = get_user_preferences(
                query=request.query,
                budget=request.budget,
                preferred_brands=request.preferred_brands,
                diet=request.diet
            )
            
            # Build AI prompt
            prompt = build_recommendation_prompt(
                request.query, 
                request.diet, 
                request.budget, 
                request.preferred_brands
            )
            
            # Initialize AI
            llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash-exp',
                api_key=GEMINI_API_KEY
            )
            
            # Get AI recommendations
            response = await llm.ainvoke(prompt)
            ai_text = response.content
        except ImportError:
            # Fallback without external modules
            ai_text = f"AI recommendations for: {request.query} within budget ₹{request.budget}"
        
        # Parse AI response into structured recommendations
        recommendations = []
        products = ai_text.split("Product ")
        
        for i, product_text in enumerate(products[1:6], 1):  # Skip first empty split, take 5 products
            try:
                lines = product_text.strip().split('\n')
                product_data = {}
                
                for line in lines:
                    if line.strip():
                        if line.startswith('Name:'):
                            product_data['name'] = line.replace('Name:', '').strip()
                        elif line.startswith('Price:'):
                            product_data['price'] = line.replace('Price:', '').strip()
                        elif line.startswith('Description:'):
                            product_data['description'] = line.replace('Description:', '').strip()
                        elif line.startswith('Protein:'):
                            protein = line.replace('Protein:', '').strip()
                            product_data['protein'] = protein if protein != "N/A" else None
                        elif line.startswith('Rating:'):
                            product_data['rating'] = line.replace('Rating:', '').strip()
                        elif line.startswith('Platform:'):
                            product_data['platform'] = line.replace('Platform:', '').strip()
                
                # Add default values if missing
                if 'name' in product_data:
                    recommendations.append({
                        "name": product_data.get('name', f'Product {i}'),
                        "price": product_data.get('price', '₹299'),
                        "description": product_data.get('description', 'Great product for your needs'),
                        "protein": product_data.get('protein'),
                        "rating": product_data.get('rating', '4.2/5'),
                        "platform": product_data.get('platform', 'Amazon Fresh'),
                        "selected": False
                    })
            except Exception as parse_error:
                print(f"Error parsing product {i}: {parse_error}")
                continue
        
        # Fallback if parsing failed - create dynamic recommendations based on query
        if len(recommendations) < 3:
            query_lower = request.query.lower()
            
            if "protein" in query_lower or "workout" in query_lower or "muscle" in query_lower:
                recommendations = [
                    {
                        "name": "MuscleBlaze Whey Protein Gold",
                        "price": f"₹{min(1999, request.budget)}",
                        "description": f"High-quality whey protein perfect for: {request.query}",
                        "protein": "25g per serving",
                        "rating": "4.4/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    },
                    {
                        "name": "Organic India Protein Powder",
                        "price": f"₹{min(899, request.budget)}",
                        "description": f"Plant-based protein ideal for: {request.query}",
                        "protein": "20g per serving",
                        "rating": "4.3/5",
                        "platform": "Flipkart Minutes",
                        "selected": False
                    },
                    {
                        "name": "MuscleBlaze Creatine Monohydrate",
                        "price": f"₹{min(699, request.budget)}",
                        "description": f"Pure creatine for muscle building: {request.query}",
                        "protein": "N/A",
                        "rating": "4.5/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    }
                ]
            elif "vegetable" in query_lower or "organic" in query_lower:
                recommendations = [
                    {
                        "name": "Organic Mixed Vegetables Pack",
                        "price": f"₹{min(250, request.budget)}",
                        "description": f"Fresh organic vegetables for: {request.query}",
                        "protein": None,
                        "rating": "4.5/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    },
                    {
                        "name": "Seasonal Organic Greens",
                        "price": f"₹{min(180, request.budget)}",
                        "description": f"Leafy greens perfect for: {request.query}",
                        "protein": None,
                        "rating": "4.2/5",
                        "platform": "Flipkart Minutes",
                        "selected": False
                    },
                    {
                        "name": "Organic Fruit Basket",
                        "price": f"₹{min(320, request.budget)}",
                        "description": f"Fresh seasonal fruits for: {request.query}",
                        "protein": None,
                        "rating": "4.3/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    }
                ]
            elif "snack" in query_lower:
                recommendations = [
                    {
                        "name": "Healthy Trail Mix",
                        "price": f"₹{min(299, request.budget)}",
                        "description": f"Nutritious snacks for: {request.query}",
                        "protein": "8g per serving",
                        "rating": "4.1/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    },
                    {
                        "name": "Protein Energy Bars Pack",
                        "price": f"₹{min(150, request.budget)}",
                        "description": f"Convenient protein bars for: {request.query}",
                        "protein": "12g per bar",
                        "rating": "4.3/5",
                        "platform": "Flipkart Minutes",
                        "selected": False
                    },
                    {
                        "name": "Mixed Nuts & Seeds",
                        "price": f"₹{min(399, request.budget)}",
                        "description": f"Premium nuts and seeds for: {request.query}",
                        "protein": "15g per serving",
                        "rating": "4.4/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    }
                ]
            else:
                # Generic recommendations based on query
                recommendations = [
                    {
                        "name": f"Premium Product for {request.query[:30]}",
                        "price": f"₹{min(499, request.budget)}",
                        "description": f"High-quality option specifically for: {request.query}",
                        "protein": "15g" if "protein" in request.query.lower() else None,
                        "rating": "4.3/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    },
                    {
                        "name": f"Budget-Friendly {request.query[:30]}",
                        "price": f"₹{min(299, request.budget)}",
                        "description": f"Affordable solution for: {request.query}",
                        "protein": None,
                        "rating": "4.1/5",
                        "platform": "Flipkart Minutes",
                        "selected": False
                    },
                    {
                        "name": f"Premium Choice {request.query[:20]}",
                        "price": f"₹{min(799, request.budget)}",
                        "description": f"Top-tier option for: {request.query}",
                        "protein": "20g" if "protein" in request.query.lower() else None,
                        "rating": "4.6/5",
                        "platform": "Amazon Fresh",
                        "selected": False
                    }
                ]
        
        return {
            "status": "success",
            "user_preferences": user_prefs,
            "ai_response": ai_text,
            "recommendations": recommendations[:5],  # Limit to 5 products
            "total_budget": request.budget
        }
        
    except Exception as e:
        print(f"Error in get_grocery_recommendations: {str(e)}")
        # Return fallback recommendations if AI fails
        return {
            "status": "fallback",
            "recommendations": [
                {
                    "name": "MuscleBlaze Whey Protein",
                    "price": "₹1,999",
                    "description": "High-quality whey protein for muscle building",
                    "protein": "25g per serving",
                    "rating": "4.4/5",
                    "platform": "Amazon Fresh",
                    "selected": False
                },
                {
                    "name": "Organic Trail Mix",
                    "price": "₹299",
                    "description": "Healthy snack mix with nuts and dried fruits",
                    "protein": "8g per serving",
                    "rating": "4.2/5",
                    "platform": "Flipkart Minutes",
                    "selected": False
                }
            ]
        }

@api_router.post("/grocery/create-cart")
async def create_grocery_cart(selected_products: List[dict]):
    """Create cart with selected products"""
    try:
        total_cost = 0
        cart_items = []
        
        for product in selected_products:
            if product.get('selected', False):
                # Clean price string and convert to number
                price_str = product.get('price', '₹0')
                price_num = int(price_str.replace('₹', '').replace(',', ''))
                total_cost += price_num
                cart_items.append(product)
        
        cart_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "cart_items": cart_items,
            "total_cost": total_cost,
            "item_count": len(cart_items),
            "status": "cart_created"
        }
        
        return cart_data
        
    except Exception as e:
        print(f"Error creating cart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating cart: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()