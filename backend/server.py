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
import openai
import json
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# OpenAI client initialization
openai_client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Authentication Models
class SignupRequest(BaseModel):
    # Basic Credentials
    name: str
    email: str
    password: str
    confirmPassword: str
    agreeTerms: bool
    # Vital Stats  
    age: int
    gender: str
    height: float
    heightUnit: str = "cm"
    weight: float
    weightUnit: str = "kg"
    # Allergies & Medical
    allergies: List[str] = []
    chronicConditions: List[str] = []
    # Wellness Goals
    wellnessGoals: List[str] = []
    # Lifestyle & Preferences
    fitnessLevel: str
    dietPreference: str
    skinType: str
    smartCartOptIn: bool = False

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None

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

# Personalized Wellness Models
class PersonalizedWellnessRequest(BaseModel):
    user_id: str
    weight: str
    allergies: str
    wellness_goals: List[str]
    health_conditions: List[str]
    age: int
    gender: str
    fitness_level: str

class WellnessRecommendation(BaseModel):
    category: str  # workout, diet, skincare, health
    title: str
    description: str
    duration: str
    level: str  # Beginner to Advanced
    requirements: List[str]
    steps: List[str]
    youtube_video: str
    product_links: List[str]
    image_url: str
    motivational_quote: Optional[str] = None  # for health category

class PersonalizedWellnessResponse(BaseModel):
    success: bool
    message: str
    recommendations: Dict[str, List[WellnessRecommendation]]

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

# Authentication Routes
@api_router.post("/auth/signup", response_model=AuthResponse)
async def signup_user(signup_data: SignupRequest):
    """Register a new user with complete profile data"""
    try:
        # Validate password confirmation
        if signup_data.password != signup_data.confirmPassword:
            return AuthResponse(
                success=False,
                message="Passwords do not match"
            )
        
        # Check if email already exists
        existing_user = await db.users.find_one({"email": signup_data.email})
        if existing_user:
            return AuthResponse(
                success=False,
                message="Email already registered. Please use a different email or login."
            )
        
        # Hash the password
        hashed_password = hash_password(signup_data.password)
        
        # Prepare user document with all signup data
        user_doc = {
            "id": str(uuid.uuid4()),
            "name": signup_data.name,
            "email": signup_data.email,
            "password": hashed_password,
            "age": signup_data.age,
            "gender": signup_data.gender,
            "height": signup_data.height,
            "height_unit": signup_data.heightUnit,
            "weight": signup_data.weight,
            "weight_unit": signup_data.weightUnit,
            "allergies": signup_data.allergies,
            "chronic_conditions": signup_data.chronicConditions,
            "goals": signup_data.wellnessGoals,
            "fitness_level": signup_data.fitnessLevel,
            "diet_type": signup_data.dietPreference,
            "skin_type": signup_data.skinType,
            "smart_cart_enabled": signup_data.smartCartOptIn,
            "created_at": datetime.utcnow()
        }
        
        # Insert user into database
        result = await db.users.insert_one(user_doc)
        
        # Return user data without password
        user_response = user_doc.copy()
        user_response.pop("password")
        user_response["_id"] = str(result.inserted_id)
        
        return AuthResponse(
            success=True,
            message="Registration successful! Welcome to Nutracía!",
            user=user_response,
            user_id=user_doc["id"]
        )
        
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Registration failed: {str(e)}"
        )

@api_router.post("/auth/login", response_model=AuthResponse)
async def login_user(login_data: LoginRequest):
    """Authenticate user and return profile data"""
    try:
        # Find user by email
        user = await db.users.find_one({"email": login_data.email})
        if not user:
            return AuthResponse(
                success=False,
                message="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user["password"]):
            return AuthResponse(
                success=False,
                message="Invalid email or password"
            )
        
        # Return user data without password
        user_response = user.copy()
        user_response.pop("password")
        if "_id" in user_response:
            user_response["_id"] = str(user_response["_id"])
        
        return AuthResponse(
            success=True,
            message="Login successful! Welcome back to Nutracía!",
            user=user_response,
            user_id=user.get("id", str(user.get("_id", "")))
        )
        
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Login failed: {str(e)}"
        )

@api_router.get("/auth/user/{user_id}", response_model=AuthResponse)
async def get_user_profile(user_id: str):
    """Retrieve user profile by ID"""
    try:
        # Try to find by custom id first, then by MongoDB _id
        user = await db.users.find_one({"id": user_id})
        if not user:
            # Try finding by MongoDB _id if it's a valid ObjectId format
            try:
                from bson import ObjectId
                if ObjectId.is_valid(user_id):
                    user = await db.users.find_one({"_id": ObjectId(user_id)})
            except:
                pass
        
        if not user:
            return AuthResponse(
                success=False,
                message="User not found"
            )
        
        # Return user data without password
        user_response = user.copy()
        user_response.pop("password", None)  # Remove password if it exists
        if "_id" in user_response:
            user_response["_id"] = str(user_response["_id"])
        
        return AuthResponse(
            success=True,
            message="User profile retrieved successfully",
            user=user_response,
            user_id=user.get("id", str(user.get("_id", "")))
        )
        
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Failed to retrieve user profile: {str(e)}"
        )

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

# Symptom Checker Models
class SymptomCheckRequest(BaseModel):
    symptoms: List[str]  # Selected predefined symptoms
    custom_symptoms: str = ""  # Custom symptoms text
    body_parts: List[str] = []  # Affected body parts
    duration: str  # Duration of symptoms
    severity: str  # mild, moderate, severe
    additional_info: str = ""
    age: Optional[int] = None
    gender: Optional[str] = None

class SymptomCheckResponse(BaseModel):
    analysis_id: str
    urgency_level: str  # Low, Medium, High
    possible_conditions: List[Dict[str, Any]]
    recommendations: List[str]
    when_to_seek_care: str
    disclaimer: str
    follow_up_questions: List[str] = []

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

# Symptom Checker API Endpoint
@api_router.post("/symptoms/analyze", response_model=SymptomCheckResponse)
async def analyze_symptoms(request: SymptomCheckRequest):
    """AI-powered symptom analysis with intelligent health recommendations"""
    try:
        # Combine predefined and custom symptoms
        all_symptoms = request.symptoms.copy()
        if request.custom_symptoms.strip():
            all_symptoms.append(request.custom_symptoms)
        
        # Determine urgency level based on symptoms and severity
        urgency_level = determine_urgency_level(all_symptoms, request.severity, request.duration)
        
        # Generate possible conditions based on symptoms
        possible_conditions = generate_possible_conditions(all_symptoms, request.body_parts, request.age, request.gender)
        
        # Generate recommendations
        recommendations = generate_health_recommendations(all_symptoms, request.severity, urgency_level)
        
        # Determine when to seek care
        when_to_seek_care = get_care_guidance(urgency_level, request.severity, request.duration)
        
        # Generate follow-up questions
        follow_up_questions = generate_follow_up_questions(all_symptoms, request.body_parts)
        
        analysis_id = str(uuid.uuid4())
        
        # Store analysis in database
        analysis_obj = {
            "id": analysis_id,
            "symptoms": all_symptoms,
            "body_parts": request.body_parts,
            "duration": request.duration,
            "severity": request.severity,
            "urgency_level": urgency_level,
            "possible_conditions": possible_conditions,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow()
        }
        await db.symptom_analyses.insert_one(analysis_obj)
        
        return SymptomCheckResponse(
            analysis_id=analysis_id,
            urgency_level=urgency_level,
            possible_conditions=possible_conditions,
            recommendations=recommendations,
            when_to_seek_care=when_to_seek_care,
            disclaimer="This analysis is for informational purposes only and should not replace professional medical advice. Consult a healthcare provider for proper diagnosis and treatment.",
            follow_up_questions=follow_up_questions
        )
        
    except Exception as e:
        print(f"Error in symptom analysis: {str(e)}")
        # Fallback response
        return SymptomCheckResponse(
            analysis_id=str(uuid.uuid4()),
            urgency_level="Medium",
            possible_conditions=[
                {"name": "General Health Concern", "probability": "Unknown", "description": "Unable to analyze symptoms at this time"}
            ],
            recommendations=[
                "Stay hydrated and get adequate rest",
                "Monitor symptoms closely",
                "Consult a healthcare provider if symptoms persist or worsen"
            ],
            when_to_seek_care="Consult a healthcare provider if symptoms persist beyond 2-3 days or worsen",
            disclaimer="This analysis is for informational purposes only. Please consult a healthcare provider for proper medical advice."
        )

def determine_urgency_level(symptoms: List[str], severity: str, duration: str) -> str:
    """Determine urgency level based on symptoms, severity, and duration"""
    high_urgency_symptoms = [
        "chest pain", "difficulty breathing", "severe headache", "high fever", 
        "severe abdominal pain", "loss of consciousness", "severe allergic reaction",
        "severe bleeding", "severe burns", "severe injury"
    ]
    
    # Check for high urgency symptoms
    if any(symptom.lower() in ' '.join(symptoms).lower() for symptom in high_urgency_symptoms):
        return "High"
    
    # Check severity and duration
    if severity == "severe":
        return "High"
    elif severity == "moderate" and duration in ["more-than-week", "chronic"]:
        return "Medium"
    elif severity == "mild" and duration in ["less-than-1-day", "1-3-days"]:
        return "Low"
    else:
        return "Medium"

def generate_possible_conditions(symptoms: List[str], body_parts: List[str], age: int = None, gender: str = None) -> List[Dict[str, Any]]:
    """Generate possible conditions based on symptoms and patient info"""
    symptom_text = ' '.join(symptoms).lower()
    
    conditions = []
    
    # Common conditions based on symptoms
    if any(word in symptom_text for word in ["fever", "cough", "runny nose", "sore throat"]):
        conditions.append({
            "name": "Upper Respiratory Infection",
            "probability": "65%",
            "description": "Common cold or viral infection affecting nose, throat, and sinuses"
        })
        conditions.append({
            "name": "Flu (Influenza)",
            "probability": "25%", 
            "description": "Viral infection affecting respiratory system with systemic symptoms"
        })
    
    if any(word in symptom_text for word in ["headache", "head"]):
        conditions.append({
            "name": "Tension Headache",
            "probability": "50%",
            "description": "Most common type of headache, often stress-related"
        })
        conditions.append({
            "name": "Migraine",
            "probability": "30%",
            "description": "Severe headache often accompanied by nausea and light sensitivity"
        })
    
    if any(word in symptom_text for word in ["stomach", "abdominal", "nausea", "vomiting"]):
        conditions.append({
            "name": "Gastroenteritis",
            "probability": "45%",
            "description": "Inflammation of stomach and intestines, often viral or bacterial"
        })
        conditions.append({
            "name": "Food Poisoning",
            "probability": "35%",
            "description": "Illness caused by contaminated food or drink"
        })
    
    if any(word in symptom_text for word in ["fatigue", "tired", "exhausted"]):
        conditions.append({
            "name": "Viral Syndrome",
            "probability": "40%",
            "description": "General viral infection causing fatigue and malaise"
        })
        conditions.append({
            "name": "Sleep Deprivation",
            "probability": "30%",
            "description": "Insufficient or poor quality sleep affecting daily function"
        })
    
    # Default condition if no specific match
    if not conditions:
        conditions.append({
            "name": "General Health Concern",
            "probability": "Unknown",
            "description": "Symptoms require professional medical evaluation for proper diagnosis"
        })
    
    return conditions[:3]  # Return top 3 conditions

def generate_health_recommendations(symptoms: List[str], severity: str, urgency_level: str) -> List[str]:
    """Generate health recommendations based on symptoms and urgency"""
    recommendations = []
    
    # General recommendations
    recommendations.extend([
        "Stay well hydrated by drinking plenty of fluids",
        "Get adequate rest and sleep (7-9 hours per night)",
        "Monitor your symptoms and note any changes"
    ])
    
    # Severity-based recommendations
    if severity == "severe" or urgency_level == "High":
        recommendations.extend([
            "Seek immediate medical attention",
            "Consider visiting an emergency room or urgent care",
            "Have someone stay with you if possible"
        ])
    elif severity == "moderate":
        recommendations.extend([
            "Consider over-the-counter remedies if appropriate",
            "Contact your healthcare provider if symptoms worsen",
            "Avoid strenuous activities until symptoms improve"
        ])
    else:  # mild symptoms
        recommendations.extend([
            "Try home remedies and self-care measures",
            "Continue normal activities if you feel up to it",
            "Watch for symptom progression over the next 24-48 hours"
        ])
    
    # Symptom-specific recommendations
    symptom_text = ' '.join(symptoms).lower()
    
    if any(word in symptom_text for word in ["fever", "temperature"]):
        recommendations.append("Use fever-reducing medication if needed (follow package instructions)")
    
    if any(word in symptom_text for word in ["cough"]):
        recommendations.append("Use honey or throat lozenges to soothe throat irritation")
    
    if any(word in symptom_text for word in ["headache", "head pain"]):
        recommendations.append("Try relaxation techniques and ensure you're in a quiet, dark environment")
    
    return recommendations[:6]  # Return top 6 recommendations

def get_care_guidance(urgency_level: str, severity: str, duration: str) -> str:
    """Provide guidance on when to seek medical care"""
    if urgency_level == "High":
        return "Seek immediate medical attention. Visit the emergency room or call emergency services if symptoms are life-threatening."
    elif urgency_level == "Medium":
        return "Schedule an appointment with your healthcare provider within 24-48 hours, or sooner if symptoms worsen."
    else:
        return "Monitor symptoms for 2-3 days. Consult a healthcare provider if symptoms persist, worsen, or new concerning symptoms develop."

def generate_follow_up_questions(symptoms: List[str], body_parts: List[str]) -> List[str]:
    """Generate relevant follow-up questions based on symptoms"""
    questions = []
    
    # General follow-up questions
    questions.extend([
        "Have you experienced these symptoms before?",
        "Are you currently taking any medications?",
        "Have you been in contact with anyone who was sick recently?"
    ])
    
    # Symptom-specific follow-up questions
    symptom_text = ' '.join(symptoms).lower()
    
    if any(word in symptom_text for word in ["fever"]):
        questions.append("What is your current temperature?")
    
    if any(word in symptom_text for word in ["pain"]):
        questions.append("On a scale of 1-10, how would you rate your pain?")
    
    if any(word in symptom_text for word in ["headache"]):
        questions.append("Do you experience sensitivity to light or sound?")
    
    return questions[:4]  # Return top 4 questions

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

# Personalized Wellness Recommendation System
@api_router.post("/wellness/personalized-recommendations", response_model=PersonalizedWellnessResponse)
async def generate_personalized_wellness_recommendations(request: PersonalizedWellnessRequest):
    """Generate AI-powered personalized recommendations for all wellness categories"""
    try:
        # Prepare user profile summary
        profile_summary = f"""
        Weight: {request.weight}
        Allergies: {request.allergies}
        Wellness Goals: {', '.join(request.wellness_goals)}
        Health Conditions: {', '.join(request.health_conditions)}
        Age: {request.age}
        Gender: {request.gender}
        Fitness Level: {request.fitness_level}
        """
        
        # Generate recommendations for all categories
        recommendations = {}
        
        # 1. WORKOUT RECOMMENDATIONS
        workout_prompt = f"""
        Based on user profile: {profile_summary}
        
        Generate 3 personalized workout recommendations in this EXACT JSON format (array of objects):
        [
          {{
            "title": "Progressive Strength Building",
            "description": "Build lean muscle mass and increase strength with progressive overload training designed for {request.fitness_level} level.",
            "duration": "45-60 min",
            "level": "Beginner to Advanced",
            "requirements": ["Dumbbells or resistance bands", "Bench or sturdy chair", "Proper form guidance"],
            "steps": ["5 min dynamic warm-up", "Compound movements: 3 sets x 8-12 reps", "Progressive overload each week", "Cool down stretches: 5 min"],
            "youtube_video": "https://www.youtube.com/results?search_query=strength+training+{request.fitness_level}+workout",
            "product_links": ["https://amazon.com/s?k=adjustable+dumbbells+home+gym", "https://flipkart.com/search?q=resistance+bands+fitness"],
            "image_url": "workout_strength_building.jpg"
          }}
        ]
        
        IMPORTANT: Return ONLY the JSON array, no other text.
        """
        
        # 2. DIET RECOMMENDATIONS  
        diet_prompt = f"""
        Based on user profile: {profile_summary}
        AVOID these allergies: {request.allergies}
        
        Generate 3 personalized diet recommendations in this EXACT JSON format (array of objects):
        [
          {{
            "title": "High Protein Power Bowl",
            "description": "Muscle-building meal with complete nutrition designed for {request.weight} weight goals, avoiding {request.allergies}.",
            "duration": "25 min prep",
            "level": "Easy to Prepare",
            "requirements": ["Fresh ingredients (avoiding {request.allergies})", "Cooking utensils", "15-20 minutes prep time"],
            "steps": ["Prep vegetables: 5 min", "Cook protein source: 10 min", "Assemble bowl with healthy fats", "Add seasonings and serve"],
            "youtube_video": "https://www.youtube.com/results?search_query=healthy+protein+bowl+recipe+{'+'.join(request.wellness_goals)}",
            "product_links": ["https://amazon.com/s?k=organic+vegetables+fresh", "https://flipkart.com/search?q=lean+protein+sources"],
            "image_url": "diet_power_bowl.jpg"
          }}
        ]
        
        IMPORTANT: Return ONLY the JSON array, no other text.
        """
        
        # 3. SKINCARE RECOMMENDATIONS
        skincare_prompt = f"""
        Based on user profile: {profile_summary}
        
        Generate 3 personalized skincare recommendations in this EXACT JSON format (array of objects):
        [
          {{
            "title": "Morning Glow Routine",
            "description": "Start your day with radiant skin using this science-backed routine tailored for {request.age} year old {request.gender}.",
            "duration": "10-15 min",
            "level": "Suitable for All Skin Types",
            "requirements": ["Gentle cleanser", "Vitamin C serum", "Moisturizer with SPF", "Clean hands"],
            "steps": ["Cleanse with lukewarm water: 2 min", "Apply vitamin C serum: 1 min", "Moisturize evenly: 2 min", "Apply SPF 30+ sunscreen: 2 min"],
            "youtube_video": "https://www.youtube.com/results?search_query=morning+skincare+routine+{request.gender}+{request.age}",
            "product_links": ["https://amazon.com/s?k=morning+skincare+routine+products", "https://flipkart.com/search?q=sunscreen+spf+50+daily"],
            "image_url": "skincare_morning_routine.jpg"
          }}
        ]
        
        IMPORTANT: Return ONLY the JSON array, no other text.
        """
        
        # 4. HEALTH RECOMMENDATIONS
        health_conditions_str = ', '.join(request.health_conditions) if request.health_conditions else 'general wellness'
        health_prompt = f"""
        Based on user profile: {profile_summary}
        Focus on: {health_conditions_str}
        
        Generate 3 personalized health management recommendations in this EXACT JSON format (array of objects):
        [
          {{
            "title": "Daily Wellness Management",
            "description": "Holistic approach to managing {health_conditions_str} while achieving your wellness goals.",
            "duration": "Ongoing Daily Routine",
            "level": "Personalized for Your Conditions",
            "requirements": ["Daily commitment", "Health monitoring tools", "Professional guidance when needed"],
            "steps": ["Morning health check: 5 min", "Medication/supplement routine if needed", "Physical activity as recommended", "Evening reflection and planning"],
            "youtube_video": "https://www.youtube.com/results?search_query=health+management+{health_conditions_str.replace(' ', '+')}+wellness",
            "product_links": ["https://amazon.com/s?k=health+monitoring+devices+wellness", "https://flipkart.com/search?q=health+supplements+wellness"],
            "image_url": "health_wellness_management.jpg",
            "motivational_quote": "Every step you take towards better health is a victory. BELIEVE NUTRACIAA YOU WILL HEAL SOON! 💪✨"
          }}
        ]
        
        IMPORTANT: Return ONLY the JSON array, no other text.
        """
        
        # Generate recommendations using OpenAI
        categories = {
            'workout': workout_prompt,
            'diet': diet_prompt, 
            'skincare': skincare_prompt,
            'health': health_prompt
        }
        
        for category, prompt in categories.items():
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional wellness coach. Return ONLY valid JSON arrays as requested, no additional text or formatting."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                
                # Parse the response
                ai_response = response.choices[0].message.content.strip()
                
                # Clean the response to ensure it's valid JSON
                ai_response = ai_response.replace('```json', '').replace('```', '').strip()
                
                # Parse JSON response
                category_recommendations = json.loads(ai_response)
                
                # Convert to WellnessRecommendation objects
                recommendations[category] = []
                for rec_data in category_recommendations:
                    rec_data['category'] = category
                    recommendation = WellnessRecommendation(**rec_data)
                    recommendations[category].append(recommendation)
                    
            except Exception as e:
                print(f"Error generating {category} recommendations: {str(e)}")
                # Fallback recommendations
                recommendations[category] = get_fallback_recommendations(category, request)
        
        # Store recommendations in database for future reference
        recommendation_doc = {
            "user_id": request.user_id,
            "timestamp": datetime.utcnow(),
            "user_profile": profile_summary,
            "recommendations": {
                category: [rec.dict() for rec in recs] 
                for category, recs in recommendations.items()
            }
        }
        await db.personalized_recommendations.insert_one(recommendation_doc)
        
        return PersonalizedWellnessResponse(
            success=True,
            message="Personalized wellness recommendations generated successfully!",
            recommendations=recommendations
        )
        
    except Exception as e:
        print(f"Error in personalized wellness recommendations: {str(e)}")
        return PersonalizedWellnessResponse(
            success=False,
            message=f"Failed to generate recommendations: {str(e)}",
            recommendations={}
        )

def get_fallback_recommendations(category: str, request: PersonalizedWellnessRequest) -> List[WellnessRecommendation]:
    """Provide fallback recommendations if AI generation fails"""
    fallback_data = {
        'workout': [
            {
                "category": "workout",
                "title": "Personalized Strength Training",
                "description": f"Custom workout plan for {request.fitness_level} level focusing on your goals.",
                "duration": "30-45 min",
                "level": request.fitness_level.title(),
                "requirements": ["Basic equipment", "Proper form", "Consistency"],
                "steps": ["Warm up", "Main exercises", "Cool down", "Stretch"],
                "youtube_video": f"https://www.youtube.com/results?search_query={request.fitness_level}+workout+routine",
                "product_links": ["https://amazon.com/s?k=home+gym+equipment", "https://flipkart.com/search?q=fitness+accessories"],
                "image_url": "workout_default.jpg"
            }
        ],
        'diet': [
            {
                "category": "diet",
                "title": "Balanced Nutrition Plan",
                "description": f"Healthy meal plan avoiding {request.allergies} and supporting your goals.",
                "duration": "30 min prep",
                "level": "Easy to Follow",
                "requirements": ["Fresh ingredients", "Basic cooking skills", "Meal planning"],
                "steps": ["Plan meals", "Shop ingredients", "Prep in advance", "Cook and enjoy"],
                "youtube_video": f"https://www.youtube.com/results?search_query=healthy+meal+prep+{'+'.join(request.wellness_goals)}",
                "product_links": ["https://amazon.com/s?k=healthy+cooking+ingredients", "https://flipkart.com/search?q=organic+food+items"],
                "image_url": "diet_default.jpg"
            }
        ],
        'skincare': [
            {
                "category": "skincare",
                "title": "Daily Skincare Routine",
                "description": f"Simple skincare routine perfect for {request.age} year old {request.gender}.",
                "duration": "10 min",
                "level": "Beginner Friendly",
                "requirements": ["Gentle cleanser", "Moisturizer", "Sunscreen", "Consistency"],
                "steps": ["Cleanse", "Treat", "Moisturize", "Protect"],
                "youtube_video": f"https://www.youtube.com/results?search_query=skincare+routine+{request.gender}+{request.age}",
                "product_links": ["https://amazon.com/s?k=basic+skincare+products", "https://flipkart.com/search?q=skincare+essentials"],
                "image_url": "skincare_default.jpg"
            }
        ],
        'health': [
            {
                "category": "health",
                "title": "Wellness Management",
                "description": f"Comprehensive health approach for your wellness journey.",
                "duration": "Daily routine",
                "level": "Personalized",
                "requirements": ["Commitment", "Regular monitoring", "Professional guidance"],
                "steps": ["Monitor health", "Stay active", "Eat well", "Rest properly"],
                "youtube_video": f"https://www.youtube.com/results?search_query=health+wellness+management",
                "product_links": ["https://amazon.com/s?k=health+monitoring+tools", "https://flipkart.com/search?q=wellness+supplements"],
                "image_url": "health_default.jpg",
                "motivational_quote": "Your health journey is unique and every step forward matters. BELIEVE NUTRACIAA YOU WILL HEAL SOON! 🌟"
            }
        ]
    }
    
    return [WellnessRecommendation(**rec) for rec in fallback_data.get(category, [])]

# Mind and Soul API Models
class MoodEntry(BaseModel):
    user_id: str
    date: str
    mood: int = Field(..., ge=1, le=5)  # 1-5 scale
    mood_label: str  # "Very Sad", "Sad", "Neutral", "Happy", "Very Happy"
    energy: int = Field(..., ge=1, le=5)
    stress: int = Field(..., ge=1, le=5)
    notes: Optional[str] = ""

class MeditationSession(BaseModel):
    user_id: str
    session_type: str  # "meditation", "breathing", "mindfulness", etc.
    duration_minutes: int
    completed: bool
    date: str
    session_id: str

class HabitProgress(BaseModel):
    user_id: str
    habit_name: str
    date: str
    completed: bool
    streak_count: int

# Mind and Soul API Endpoints

@api_router.get("/mind-soul/meditation-content")
async def get_meditation_content():
    """Get meditation and mindfulness content"""
    meditation_content = [
        {
            "id": "guided-meditation-1",
            "title": "Morning Mindfulness",
            "description": "Start your day with clarity and focus through guided morning meditation",
            "duration": "10 minutes",
            "type": "guided_meditation",
            "difficulty": "Beginner",
            "benefits": ["Reduces stress", "Improves focus", "Increases energy"],
            "instructions": [
                "Find a comfortable seated position",
                "Close your eyes gently",
                "Focus on your breathing",
                "Follow the guided instructions",
                "End with gratitude practice"
            ],
            "youtube_video": "https://www.youtube.com/embed/inpok4MKVLM",
            "category": "morning_routine",
            "image_url": "meditation_morning.jpg"
        },
        {
            "id": "breathing-exercise-1", 
            "title": "4-7-8 Breathing Technique",
            "description": "Powerful breathing exercise for anxiety relief and better sleep",
            "duration": "5 minutes",
            "type": "breathing_exercise",
            "difficulty": "Beginner",
            "benefits": ["Reduces anxiety", "Improves sleep", "Calms nervous system"],
            "instructions": [
                "Sit comfortably with back straight",
                "Exhale completely through mouth",
                "Inhale through nose for 4 counts",
                "Hold breath for 7 counts", 
                "Exhale through mouth for 8 counts",
                "Repeat cycle 4 times"
            ],
            "youtube_video": "https://www.youtube.com/embed/YRPh_GaiL8s",
            "category": "breathing",
            "image_url": "breathing_exercise.jpg"
        },
        {
            "id": "mindfulness-practice-1",
            "title": "Body Scan Meditation",
            "description": "Deep relaxation technique to release tension and increase awareness",
            "duration": "15 minutes", 
            "type": "mindfulness",
            "difficulty": "Intermediate",
            "benefits": ["Releases tension", "Increases body awareness", "Promotes relaxation"],
            "instructions": [
                "Lie down comfortably",
                "Start with deep breathing",
                "Focus on each body part systematically",
                "Notice sensations without judgment",
                "Complete with whole body awareness"
            ],
            "youtube_video": "https://www.youtube.com/embed/yCJ6fNd-jCE",
            "category": "relaxation",
            "image_url": "body_scan.jpg"
        },
        {
            "id": "stress-relief-1",
            "title": "Quick Stress Relief",
            "description": "5-minute emergency stress relief technique for busy schedules",
            "duration": "5 minutes",
            "type": "stress_relief",
            "difficulty": "Beginner", 
            "benefits": ["Immediate stress relief", "Lowers cortisol", "Improves mood"],
            "instructions": [
                "Take 3 deep breaths",
                "Tense and release each muscle group",
                "Visualize a calm place",
                "Practice gratitude",
                "Return to normal breathing"
            ],
            "youtube_video": "https://www.youtube.com/embed/p8fjYPC-7bM",
            "category": "stress_relief",
            "image_url": "stress_relief.jpg"
        },
        {
            "id": "sleep-meditation-1",
            "title": "Sleep Preparation Meditation",
            "description": "Gentle meditation to prepare mind and body for restful sleep",
            "duration": "20 minutes",
            "type": "sleep_meditation",
            "difficulty": "Beginner",
            "benefits": ["Improves sleep quality", "Calms racing thoughts", "Promotes deep rest"],
            "instructions": [
                "Lie down in bed comfortably",
                "Progressive muscle relaxation",
                "Guided visualization for peace",
                "Focus on releasing the day",
                "Drift into natural sleep"
            ],
            "youtube_video": "https://www.youtube.com/embed/j2YWMaDQ9LI",
            "category": "sleep",
            "image_url": "sleep_meditation.jpg"
        },
        {
            "id": "focus-meditation-1",
            "title": "Concentration Enhancement",
            "description": "Meditation practice to improve focus and mental clarity",
            "duration": "12 minutes",
            "type": "focus_meditation", 
            "difficulty": "Intermediate",
            "benefits": ["Enhances concentration", "Improves productivity", "Strengthens mental clarity"],
            "instructions": [
                "Sit with spine straight",
                "Focus on single point of attention",
                "When mind wanders, gently return focus",
                "Gradually extend concentration periods",
                "End with appreciation for the practice"
            ],
            "youtube_video": "https://www.youtube.com/embed/oNkIzE_4WB8",
            "category": "focus",
            "image_url": "focus_meditation.jpg"
        }
    ]
    
    return {
        "status": "success",
        "content": meditation_content,
        "total_count": len(meditation_content)
    }

@api_router.post("/mind-soul/mood-tracker")
async def log_mood(mood_entry: MoodEntry):
    """Log daily mood entry"""
    try:
        # Create mood entry document with UUID instead of ObjectId
        mood_doc = {
            "id": str(uuid.uuid4()),
            "user_id": mood_entry.user_id,
            "date": mood_entry.date,
            "mood": mood_entry.mood,
            "mood_label": mood_entry.mood_label,
            "energy": mood_entry.energy,
            "stress": mood_entry.stress,
            "notes": mood_entry.notes,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Check if entry for this date already exists
        existing_entry = await db.mood_entries.find_one({
            "user_id": mood_entry.user_id,
            "date": mood_entry.date
        })
        
        if existing_entry:
            # Update existing entry
            await db.mood_entries.update_one(
                {"user_id": mood_entry.user_id, "date": mood_entry.date},
                {"$set": mood_doc}
            )
            message = "Mood entry updated successfully"
        else:
            # Create new entry
            await db.mood_entries.insert_one(mood_doc)
            message = "Mood entry logged successfully"
        
        # Remove MongoDB _id from response
        response_data = {k: v for k, v in mood_doc.items() if k != '_id'}
        
        return {
            "status": "success",
            "message": message,
            "mood_data": response_data
        }
        
    except Exception as e:
        print(f"Error logging mood: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error logging mood: {str(e)}")

@api_router.get("/mind-soul/mood-history/{user_id}")
async def get_mood_history(user_id: str, days: int = 30):
    """Get mood history for a user"""
    try:
        # Get mood entries for the last N days
        mood_entries = await db.mood_entries.find(
            {"user_id": user_id}
        ).sort("date", -1).limit(days).to_list(length=days)
        
        # Remove MongoDB ObjectId and ensure datetime serialization
        clean_entries = []
        for entry in mood_entries:
            clean_entry = {k: v for k, v in entry.items() if k != '_id'}
            # Convert datetime to string if it exists
            if 'timestamp' in clean_entry and hasattr(clean_entry['timestamp'], 'isoformat'):
                clean_entry['timestamp'] = clean_entry['timestamp'].isoformat()
            clean_entries.append(clean_entry)
        
        # Calculate mood statistics
        if clean_entries:
            moods = [entry["mood"] for entry in clean_entries]
            energy_levels = [entry["energy"] for entry in clean_entries]
            stress_levels = [entry["stress"] for entry in clean_entries]
            
            avg_mood = sum(moods) / len(moods)
            avg_energy = sum(energy_levels) / len(energy_levels)
            avg_stress = sum(stress_levels) / len(stress_levels)
        else:
            avg_mood = avg_energy = avg_stress = 0
        
        return {
            "status": "success",
            "mood_history": clean_entries,
            "statistics": {
                "average_mood": round(avg_mood, 2),
                "average_energy": round(avg_energy, 2), 
                "average_stress": round(avg_stress, 2),
                "total_entries": len(clean_entries)
            }
        }
        
    except Exception as e:
        print(f"Error getting mood history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting mood history: {str(e)}")

@api_router.post("/mind-soul/meditation-session")
async def log_meditation_session(session: MeditationSession):
    """Log a meditation session"""
    try:
        session_doc = {
            "user_id": session.user_id,
            "session_type": session.session_type,
            "duration_minutes": session.duration_minutes,
            "completed": session.completed,
            "date": session.date,
            "session_id": session.session_id,
            "timestamp": datetime.utcnow()
        }
        
        await db.meditation_sessions.insert_one(session_doc)
        
        # Update user's meditation streak and total time
        await update_meditation_progress(session.user_id, session.duration_minutes, session.completed)
        
        return {
            "status": "success",
            "message": "Meditation session logged successfully",
            "session_data": session_doc
        }
        
    except Exception as e:
        print(f"Error logging meditation session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error logging session: {str(e)}")

@api_router.get("/mind-soul/meditation-progress/{user_id}")
async def get_meditation_progress(user_id: str):
    """Get meditation progress for a user"""
    try:
        # Get total meditation time and sessions
        sessions = await db.meditation_sessions.find({"user_id": user_id}).to_list(length=1000)
        
        total_sessions = len(sessions)
        total_minutes = sum(session["duration_minutes"] for session in sessions if session["completed"])
        
        # Calculate current streak
        current_streak = await calculate_meditation_streak(user_id)
        
        # Get this week's sessions
        from datetime import datetime, timedelta
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        this_week_sessions = [s for s in sessions if datetime.fromisoformat(s["date"]) >= week_start]
        
        return {
            "status": "success",
            "progress": {
                "total_sessions": total_sessions,
                "total_minutes": total_minutes,
                "current_streak": current_streak,
                "this_week_sessions": len(this_week_sessions),
                "average_session_length": round(total_minutes / total_sessions if total_sessions > 0 else 0, 1)
            }
        }
        
    except Exception as e:
        print(f"Error getting meditation progress: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting progress: {str(e)}")

@api_router.post("/mind-soul/habit-tracker")
async def log_habit_progress(habit: HabitProgress):
    """Log habit progress"""
    try:
        habit_doc = {
            "user_id": habit.user_id,
            "habit_name": habit.habit_name,
            "date": habit.date,
            "completed": habit.completed,
            "streak_count": habit.streak_count,
            "timestamp": datetime.utcnow()
        }
        
        # Check if entry exists for this date and habit
        existing_habit = await db.habit_progress.find_one({
            "user_id": habit.user_id,
            "habit_name": habit.habit_name,
            "date": habit.date
        })
        
        if existing_habit:
            await db.habit_progress.update_one(
                {"user_id": habit.user_id, "habit_name": habit.habit_name, "date": habit.date},
                {"$set": habit_doc}
            )
        else:
            await db.habit_progress.insert_one(habit_doc)
        
        return {
            "status": "success",
            "message": "Habit progress logged successfully",
            "habit_data": habit_doc
        }
        
    except Exception as e:
        print(f"Error logging habit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error logging habit: {str(e)}")

@api_router.get("/mind-soul/habits/{user_id}")
async def get_user_habits(user_id: str):
    """Get all habits for a user with current streaks"""
    try:
        # Get all habit entries for user
        habits = await db.habit_progress.find({"user_id": user_id}).to_list(length=1000)
        
        # Group by habit name and calculate streaks
        habit_summary = {}
        for habit in habits:
            habit_name = habit["habit_name"]
            if habit_name not in habit_summary:
                habit_summary[habit_name] = {
                    "habit_name": habit_name,
                    "current_streak": 0,
                    "total_completions": 0,
                    "last_completed": None
                }
            
            if habit["completed"]:
                habit_summary[habit_name]["total_completions"] += 1
                if not habit_summary[habit_name]["last_completed"] or habit["date"] > habit_summary[habit_name]["last_completed"]:
                    habit_summary[habit_name]["last_completed"] = habit["date"]
        
        # Calculate current streaks for each habit
        for habit_name, data in habit_summary.items():
            data["current_streak"] = await calculate_habit_streak(user_id, habit_name)
        
        return {
            "status": "success",
            "habits": list(habit_summary.values())
        }
        
    except Exception as e:
        print(f"Error getting habits: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting habits: {str(e)}")

# Helper functions
async def update_meditation_progress(user_id: str, duration_minutes: int, completed: bool):
    """Update user's overall meditation progress"""
    if not completed:
        return
    
    # This could be expanded to update user profile with meditation stats
    pass

async def calculate_meditation_streak(user_id: str) -> int:
    """Calculate current meditation streak"""
    try:
        sessions = await db.meditation_sessions.find(
            {"user_id": user_id, "completed": True}
        ).sort("date", -1).to_list(length=100)
        
        if not sessions:
            return 0
        
        # Count consecutive days from today backwards
        from datetime import datetime, timedelta
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        session_dates = set(datetime.fromisoformat(s["date"]).date() for s in sessions)
        
        while current_date in session_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
        
    except Exception as e:
        print(f"Error calculating streak: {str(e)}")
        return 0

async def calculate_habit_streak(user_id: str, habit_name: str) -> int:
    """Calculate current habit streak"""
    try:
        habits = await db.habit_progress.find(
            {"user_id": user_id, "habit_name": habit_name, "completed": True}
        ).sort("date", -1).to_list(length=100)
        
        if not habits:
            return 0
        
        from datetime import datetime, timedelta
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        habit_dates = set(datetime.fromisoformat(h["date"]).date() for h in habits)
        
        while current_date in habit_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
        
    except Exception as e:
        print(f"Error calculating habit streak: {str(e)}")
        return 0

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