from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

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

@api_router.post("/chat", response_model=dict)
async def chat_with_ai(chat_data: ChatMessageCreate):
    # Placeholder for AI chat integration
    # This will be connected to OpenAI when API key is provided
    response_text = f"Thank you for your message: '{chat_data.message}'. I'm here to help with your wellness journey! (AI integration pending API key)"
    
    chat_obj = ChatMessage(
        user_id=chat_data.user_id,
        message=chat_data.message,
        response=response_text
    )
    await db.chat_history.insert_one(chat_obj.dict())
    
    return {
        "response": response_text,
        "message_id": chat_obj.id
    }

# Grocery agent endpoints (will be integrated from the cloned repo)
@api_router.post("/grocery/recommendations")
async def get_grocery_recommendations(query_data: dict):
    # Placeholder - will integrate actual grocery agent logic
    return {
        "recommendations": [
            {
                "name": "Organic Protein Powder",
                "price": "₹2,499",
                "description": "High-quality whey protein for muscle building",
                "rating": "4.5",
                "platform": "Amazon",
                "selected": False
            }
        ]
    }

@api_router.post("/grocery/create-cart")
async def create_grocery_cart(products: List[dict]):
    # Placeholder - will integrate actual cart creation logic
    total_cost = sum([int(p.get('price', '0').replace('₹', '').replace(',', '')) for p in products])
    return {
        "cart_items": products,
        "total_cost": total_cost,
        "status": "created"
    }

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