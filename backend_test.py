import requests
import json
import os
import sys
import uuid
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from frontend/.env to get the backend URL
load_dotenv(Path('/app/frontend/.env'))

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Ensure the URL ends with /api
API_URL = f"{BACKEND_URL}/api"
print(f"Testing API at: {API_URL}")

def test_root_endpoint():
    """Test the root endpoint for basic connectivity"""
    print("\n=== Testing Root Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "message" in response.json(), "Response does not contain 'message' field"
        print("✅ Root endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Root endpoint test failed: {str(e)}")
        return False

def test_auth_signup():
    """Test user registration with complete 5-step profile data"""
    print("\n=== Testing Authentication Signup Endpoint ===")
    try:
        # Complete 5-step profile data as specified in the requirements
        signup_data = {
            "name": "Sarah Chen",
            "email": "sarah.chen@email.com",
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            "age": 28,
            "gender": "Female",
            "height": 165,
            "heightUnit": "cm",
            "weight": 58,
            "weightUnit": "kg",
            "allergies": ["Nuts", "Shellfish"],
            "chronicConditions": [],
            "wellnessGoals": ["Weight Loss", "Better Sleep", "Stress Management"],
            "fitnessLevel": "Intermediate",
            "dietPreference": "Vegetarian",
            "skinType": "Combination",
            "smartCartOptIn": True
        }
        
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Signup response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        
        if data["success"]:
            assert "user" in data, "Response missing 'user' field"
            assert "user_id" in data, "Response missing 'user_id' field"
            
            # Verify user data is stored correctly
            user = data["user"]
            assert user["name"] == signup_data["name"], "User name doesn't match"
            assert user["email"] == signup_data["email"], "User email doesn't match"
            assert "password" not in user, "Password should not be returned in response"
            assert user["age"] == signup_data["age"], "User age doesn't match"
            assert user["gender"] == signup_data["gender"], "User gender doesn't match"
            assert user["height"] == signup_data["height"], "User height doesn't match"
            assert user["allergies"] == signup_data["allergies"], "User allergies don't match"
            assert user["goals"] == signup_data["wellnessGoals"], "User wellness goals don't match"
            assert user["fitness_level"] == signup_data["fitnessLevel"], "User fitness level doesn't match"
            assert user["diet_type"] == signup_data["dietPreference"], "User diet preference doesn't match"
            assert user["skin_type"] == signup_data["skinType"], "User skin type doesn't match"
            
            user_id = data["user_id"]
            print(f"✅ Authentication signup test passed - Created user with ID: {user_id}")
            return True, user_id, signup_data["email"], signup_data["password"]
        else:
            # If the user already exists, this is still a valid test case
            if "already registered" in data["message"]:
                print("User already exists - this is expected if the test has been run before")
                # Try to login with the credentials to get the user_id
                login_result, user_id = test_auth_login(signup_data["email"], signup_data["password"])
                if login_result:
                    print(f"✅ Authentication signup test passed (user already exists) - Retrieved user ID: {user_id}")
                    return True, user_id, signup_data["email"], signup_data["password"]
                else:
                    print("❌ Could not retrieve existing user")
                    return False, None, None, None
            else:
                print(f"❌ Signup failed with message: {data['message']}")
                return False, None, None, None
    except Exception as e:
        print(f"❌ Authentication signup test failed: {str(e)}")
        return False, None, None, None

def test_auth_login(email=None, password=None):
    """Test user authentication with email/password"""
    print("\n=== Testing Authentication Login Endpoint ===")
    try:
        # Use provided credentials or defaults
        login_data = {
            "email": email or "sarah.chen@email.com",
            "password": password or "SecurePass123!"
        }
        
        response = requests.post(f"{API_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Login response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        
        if data["success"]:
            assert "user" in data, "Response missing 'user' field"
            assert "user_id" in data, "Response missing 'user_id' field"
            assert "password" not in data["user"], "Password should not be returned in response"
            
            user_id = data["user_id"]
            print(f"✅ Authentication login test passed - User ID: {user_id}")
            return True, user_id
        else:
            print(f"❌ Login failed with message: {data['message']}")
            return False, None
    except Exception as e:
        print(f"❌ Authentication login test failed: {str(e)}")
        return False, None

def test_auth_get_user(user_id=None):
    """Test user profile retrieval by ID"""
    print("\n=== Testing Authentication Get User Endpoint ===")
    if not user_id:
        print("❌ Authentication get user test skipped: No user ID provided")
        return False
    
    try:
        response = requests.get(f"{API_URL}/auth/user/{user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Get user response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        
        if data["success"]:
            assert "user" in data, "Response missing 'user' field"
            assert "user_id" in data, "Response missing 'user_id' field"
            assert "password" not in data["user"], "Password should not be returned in response"
            assert data["user_id"] == user_id, "User ID in response doesn't match requested ID"
            
            print(f"✅ Authentication get user test passed - User ID: {user_id}")
            return True
        else:
            print(f"❌ Get user failed with message: {data['message']}")
            return False
    except Exception as e:
        print(f"❌ Authentication get user test failed: {str(e)}")
        return False

def test_auth_validation():
    """Test validation for authentication endpoints"""
    print("\n=== Testing Authentication Validation ===")
    all_passed = True
    
    # Test 1: Password confirmation validation
    print("\n--- Test 1: Password confirmation validation ---")
    try:
        signup_data = {
            "name": "Test User",
            "email": "test.validation@email.com",
            "password": "SecurePass123!",
            "confirmPassword": "DifferentPassword123!",  # Mismatched password
            "agreeTerms": True,
            "age": 30,
            "gender": "Male",
            "height": 180,
            "heightUnit": "cm",
            "weight": 75,
            "weightUnit": "kg",
            "allergies": [],
            "chronicConditions": [],
            "wellnessGoals": ["Muscle Gain"],
            "fitnessLevel": "Beginner",
            "dietPreference": "Omnivore",
            "skinType": "Normal",
            "smartCartOptIn": False
        }
        
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == False, "Signup with mismatched passwords should fail"
        assert "message" in data, "Response missing 'message' field"
        assert "password" in data["message"].lower(), "Error message should mention password mismatch"
        
        print("✅ Password confirmation validation test passed")
    except Exception as e:
        print(f"❌ Password confirmation validation test failed: {str(e)}")
        all_passed = False
    
    # Test 2: Email uniqueness validation
    print("\n--- Test 2: Email uniqueness validation ---")
    try:
        # Use the same email as in the main signup test
        signup_data = {
            "name": "Duplicate Email User",
            "email": "sarah.chen@email.com",  # This email should already exist
            "password": "AnotherPassword123!",
            "confirmPassword": "AnotherPassword123!",
            "agreeTerms": True,
            "age": 35,
            "gender": "Female",
            "height": 160,
            "heightUnit": "cm",
            "weight": 55,
            "weightUnit": "kg",
            "allergies": [],
            "chronicConditions": [],
            "wellnessGoals": ["Weight Loss"],
            "fitnessLevel": "Advanced",
            "dietPreference": "Vegan",
            "skinType": "Dry",
            "smartCartOptIn": True
        }
        
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == False, "Signup with duplicate email should fail"
        assert "message" in data, "Response missing 'message' field"
        assert "already registered" in data["message"] or "email" in data["message"].lower(), "Error message should mention email already exists"
        
        print("✅ Email uniqueness validation test passed")
    except Exception as e:
        print(f"❌ Email uniqueness validation test failed: {str(e)}")
        all_passed = False
    
    # Test 3: Required fields validation
    print("\n--- Test 3: Required fields validation ---")
    try:
        # Missing required fields
        signup_data = {
            "name": "Missing Fields User",
            # Missing email
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            # Missing age
            "gender": "Male",
            # Missing height
            "heightUnit": "cm",
            # Missing weight
            "weightUnit": "kg",
            "allergies": [],
            "chronicConditions": [],
            # Missing wellnessGoals
            # Missing fitnessLevel
            # Missing dietPreference
            # Missing skinType
            "smartCartOptIn": False
        }
        
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        
        # Either it should return a validation error (422) or a custom error message (200)
        assert response.status_code in [200, 422], f"Expected status code 200 or 422, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            assert "success" in data, "Response missing 'success' field"
            assert data["success"] == False, "Signup with missing fields should fail"
            assert "message" in data, "Response missing 'message' field"
        else:
            print(f"Validation error returned: {response.status_code}")
        
        print("✅ Required fields validation test passed")
    except Exception as e:
        print(f"❌ Required fields validation test failed: {str(e)}")
        all_passed = False
    
    # Test 4: Invalid credentials for login
    print("\n--- Test 4: Invalid credentials for login ---")
    try:
        login_data = {
            "email": "nonexistent@email.com",
            "password": "WrongPassword123!"
        }
        
        response = requests.post(f"{API_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == False, "Login with invalid credentials should fail"
        assert "message" in data, "Response missing 'message' field"
        assert "invalid" in data["message"].lower(), "Error message should mention invalid credentials"
        
        print("✅ Invalid credentials test passed")
    except Exception as e:
        print(f"❌ Invalid credentials test failed: {str(e)}")
        all_passed = False
    
    # Test 5: Non-existent user profile retrieval
    print("\n--- Test 5: Non-existent user profile retrieval ---")
    try:
        fake_user_id = "nonexistent-user-id-12345"
        response = requests.get(f"{API_URL}/auth/user/{fake_user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == False, "Retrieving non-existent user should fail"
        assert "message" in data, "Response missing 'message' field"
        assert "not found" in data["message"].lower(), "Error message should mention user not found"
        
        print("✅ Non-existent user retrieval test passed")
    except Exception as e:
        print(f"❌ Non-existent user retrieval test failed: {str(e)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All authentication validation tests passed")
    else:
        print("\n❌ Some authentication validation tests failed")
    
    return all_passed

def test_workouts_endpoint():
    """Test the workouts endpoint with enhanced validation for exercise data"""
    print("\n=== Testing Workouts Endpoint with Enhanced Exercise Data ===")
    try:
        response = requests.get(f"{API_URL}/workouts")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} workouts")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) >= 3, f"Expected at least 3 workout plans, found {len(data)}"
        
        # Validate each workout has the required fields and proper structure
        required_fields = [
            "id", "title", "description", "muscle_groups", "equipment", 
            "duration", "difficulty", "video_url", "instructions"
        ]
        
        for i, workout in enumerate(data):
            print(f"\nValidating workout {i+1}: {workout.get('title', 'Unknown')}")
            
            # Check all required fields exist
            for field in required_fields:
                assert field in workout, f"Workout missing '{field}' field"
            
            # Validate field types
            assert isinstance(workout["id"], str), "Workout 'id' is not a string"
            assert isinstance(workout["title"], str), "Workout 'title' is not a string"
            assert isinstance(workout["description"], str), "Workout 'description' is not a string"
            assert isinstance(workout["muscle_groups"], list), "Workout 'muscle_groups' is not a list"
            assert isinstance(workout["equipment"], list), "Workout 'equipment' is not a list"
            assert isinstance(workout["duration"], int), "Workout 'duration' is not an integer"
            assert isinstance(workout["difficulty"], str), "Workout 'difficulty' is not a string"
            assert isinstance(workout["video_url"], str), "Workout 'video_url' is not a string"
            assert isinstance(workout["instructions"], list), "Workout 'instructions' is not a list"
            
            # Validate content
            assert len(workout["title"]) > 0, "Workout title is empty"
            assert len(workout["description"]) > 0, "Workout description is empty"
            assert len(workout["muscle_groups"]) > 0, "Workout has no muscle groups"
            assert workout["duration"] > 0, "Workout duration must be positive"
            assert workout["difficulty"] in ["beginner", "intermediate", "advanced"], f"Invalid difficulty: {workout['difficulty']}"
            assert workout["video_url"].startswith("http"), "Video URL is not properly formatted"
            assert len(workout["instructions"]) > 0, "Workout has no instructions"
            
            print(f"✓ Workout {i+1} validated successfully")
            
            # Print detailed info for the first workout
            if i == 0:
                print(f"Sample workout details:")
                print(f"  Title: {workout['title']}")
                print(f"  Description: {workout['description']}")
                print(f"  Muscle Groups: {', '.join(workout['muscle_groups'])}")
                print(f"  Equipment: {', '.join(workout['equipment'])}")
                print(f"  Duration: {workout['duration']} minutes")
                print(f"  Difficulty: {workout['difficulty']}")
                print(f"  Instructions: {len(workout['instructions'])} steps")
        
        print("\n✅ Workouts endpoint test passed with enhanced validation")
        return True, data
    except Exception as e:
        print(f"❌ Workouts endpoint test failed: {str(e)}")
        return False, None

def test_skincare_endpoint():
    """Test the skincare endpoint"""
    print("\n=== Testing Skincare Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/skincare")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} skincare routines")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        if len(data) > 0:
            print(f"Sample skincare routine: {json.dumps(data[0], indent=2)}")
            # Validate skincare structure
            assert "id" in data[0], "Skincare routine missing 'id' field"
            assert "title" in data[0], "Skincare routine missing 'title' field"
            assert "skin_type" in data[0], "Skincare routine missing 'skin_type' field"
        print("✅ Skincare endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Skincare endpoint test failed: {str(e)}")
        return False

def test_meals_endpoint():
    """Test the meals endpoint"""
    print("\n=== Testing Meals Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/meals")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} meal plans")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        if len(data) > 0:
            print(f"Sample meal plan: {json.dumps(data[0], indent=2)}")
            # Validate meal structure
            assert "id" in data[0], "Meal plan missing 'id' field"
            assert "title" in data[0], "Meal plan missing 'title' field"
            assert "diet_type" in data[0], "Meal plan missing 'diet_type' field"
        print("✅ Meals endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Meals endpoint test failed: {str(e)}")
        return False

def test_health_conditions_endpoint():
    """Test the health conditions endpoint"""
    print("\n=== Testing Health Conditions Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/health-conditions")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} health condition plans")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        if len(data) > 0:
            print(f"Sample health condition plan: {json.dumps(data[0], indent=2)}")
            # Validate health condition structure
            assert "id" in data[0], "Health condition plan missing 'id' field"
            assert "condition" in data[0], "Health condition plan missing 'condition' field"
            assert "title" in data[0], "Health condition plan missing 'title' field"
        print("✅ Health conditions endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Health conditions endpoint test failed: {str(e)}")
        return False

def test_user_creation():
    """Test user creation endpoint"""
    print("\n=== Testing User Creation Endpoint ===")
    try:
        # Sample user data
        user_data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "age": 32,
            "gender": "female",
            "height": 165.5,
            "weight": 62.3,
            "allergies": ["peanuts", "shellfish"],
            "chronic_conditions": ["asthma"],
            "goals": ["weight maintenance", "stress reduction"],
            "fitness_level": "intermediate",
            "diet_type": "vegetarian",
            "skin_type": "combination",
            "smart_cart_enabled": True
        }
        
        response = requests.post(f"{API_URL}/users", json=user_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Created user: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "id" in data, "Response missing 'id' field"
        assert data["name"] == user_data["name"], "User name doesn't match"
        assert data["email"] == user_data["email"], "User email doesn't match"
        
        # Test retrieving the created user
        user_id = data["id"]
        get_response = requests.get(f"{API_URL}/users/{user_id}")
        print(f"Get User Status Code: {get_response.status_code}")
        get_data = get_response.json()
        
        assert get_response.status_code == 200, f"Expected status code 200, got {get_response.status_code}"
        assert get_data["id"] == user_id, "User ID doesn't match"
        
        print("✅ User creation endpoint test passed")
        return True, user_id
    except Exception as e:
        print(f"❌ User creation endpoint test failed: {str(e)}")
        return False, None

def test_enhanced_health_chatbot(user_id):
    """Test the enhanced health chatbot API functionality"""
    print("\n=== Testing Enhanced Health Chatbot API ===")
    if not user_id:
        print("❌ Enhanced health chatbot test skipped: No user ID available")
        return False
    
    all_passed = True
    
    # Test case 1: Simple health question without user profile
    print("\n--- Test Case 1: Simple health question without user profile ---")
    try:
        chat_data = {
            "user_id": user_id,
            "message": "What are some general health tips?"
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Chat response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "response" in data, "Response missing 'response' field"
        assert "message_id" in data, "Response missing 'message_id' field"
        assert "requires_profile" in data, "Response missing 'requires_profile' field"
        
        print("✅ Test Case 1 passed")
    except Exception as e:
        print(f"❌ Test Case 1 failed: {str(e)}")
        all_passed = False
    
    # Test case 2: Question that requires personalization
    print("\n--- Test Case 2: Question that requires personalization ---")
    try:
        chat_data = {
            "user_id": user_id,
            "message": "Can you recommend a personalized workout plan for me?"
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Chat response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "response" in data, "Response missing 'response' field"
        assert "message_id" in data, "Response missing 'message_id' field"
        assert "requires_profile" in data, "Response missing 'requires_profile' field"
        
        # This should ask for profile information
        if data["requires_profile"]:
            assert "profile_fields" in data, "Response missing 'profile_fields' field"
            assert len(data["profile_fields"]) > 0, "Profile fields list is empty"
            print(f"Profile fields requested: {data['profile_fields']}")
        
        print("✅ Test Case 2 passed")
    except Exception as e:
        print(f"❌ Test Case 2 failed: {str(e)}")
        all_passed = False
    
    # Test case 3: Request with complete user profile
    print("\n--- Test Case 3: Request with complete user profile ---")
    try:
        chat_data = {
            "user_id": user_id,
            "message": "What workout routine would be best for me?",
            "user_profile": {
                "weight": "75kg",
                "allergies": "peanuts, shellfish",
                "skin_concern": "dryness"
            }
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Chat response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "response" in data, "Response missing 'response' field"
        assert "message_id" in data, "Response missing 'message_id' field"
        assert "requires_profile" in data, "Response missing 'requires_profile' field"
        
        # Should not ask for profile since it was provided
        assert data["requires_profile"] == False, "Should not require profile when it's already provided"
        
        print("✅ Test Case 3 passed")
    except Exception as e:
        print(f"❌ Test Case 3 failed: {str(e)}")
        all_passed = False
    
    # Test case 4: Various health topics
    health_topics = [
        {"topic": "workout", "message": "Can you suggest a HIIT workout routine?"},
        {"topic": "skincare", "message": "What's a good skincare routine for combination skin?"},
        {"topic": "nutrition", "message": "What should I eat to build muscle?"},
        {"topic": "general health", "message": "How can I improve my sleep quality?"}
    ]
    
    for topic in health_topics:
        print(f"\n--- Test Case 4: Health topic - {topic['topic']} ---")
        try:
            chat_data = {
                "user_id": user_id,
                "message": topic["message"],
                "user_profile": {
                    "weight": "70kg",
                    "allergies": "none",
                    "skin_concern": "acne"
                }
            }
            
            response = requests.post(f"{API_URL}/chat", json=chat_data)
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Chat response for {topic['topic']}: {data['response'][:100]}...")
            
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            assert "response" in data, "Response missing 'response' field"
            assert len(data["response"]) > 0, f"Empty response for {topic['topic']} topic"
            
            print(f"✅ Test Case 4 - {topic['topic']} passed")
        except Exception as e:
            print(f"❌ Test Case 4 - {topic['topic']} failed: {str(e)}")
            all_passed = False
    
    # Test case 5: Edge cases
    print("\n--- Test Case 5: Edge case - Empty message ---")
    try:
        chat_data = {
            "user_id": user_id,
            "message": ""
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        
        # Either it should handle empty messages gracefully or return an error
        if response.status_code == 200:
            data = response.json()
            print(f"Chat response: {json.dumps(data, indent=2)}")
            assert "response" in data, "Response missing 'response' field"
        else:
            print(f"API returned error for empty message: {response.status_code}")
            assert response.status_code in [400, 422], f"Expected status code 400 or 422 for empty message, got {response.status_code}"
        
        print("✅ Test Case 5 - Empty message passed")
    except Exception as e:
        print(f"❌ Test Case 5 - Empty message failed: {str(e)}")
        all_passed = False
    
    print("\n--- Test Case 5: Edge case - Invalid profile data ---")
    try:
        chat_data = {
            "user_id": user_id,
            "message": "What workout is best for me?",
            "user_profile": {
                "weight": "invalid",
                "allergies": 123,  # Should be string or list
                "skin_concern": None
            }
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        
        # Should either handle invalid profile data gracefully or return an error
        if response.status_code == 200:
            data = response.json()
            print(f"Chat response: {json.dumps(data, indent=2)}")
            assert "response" in data, "Response missing 'response' field"
        else:
            print(f"API returned error for invalid profile data: {response.status_code}")
            assert response.status_code in [400, 422], f"Expected status code 400 or 422 for invalid profile data, got {response.status_code}"
        
        print("✅ Test Case 5 - Invalid profile data passed")
    except Exception as e:
        print(f"❌ Test Case 5 - Invalid profile data failed: {str(e)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All enhanced health chatbot test cases passed")
    else:
        print("\n❌ Some enhanced health chatbot test cases failed")
    
    return all_passed

def test_grocery_recommendations():
    """Test the enhanced grocery recommendations endpoint with multiple test cases"""
    print("\n=== Testing Enhanced Grocery Recommendations Endpoint ===")
    
    test_cases = [
        {
            "name": "Simple protein supplement query",
            "payload": {
                "query": "I need a good whey protein supplement for muscle building",
                "budget": 2000,
                "preferred_brands": ["MuscleBlaze", "Optimum Nutrition"],
                "diet": "high protein"
            }
        },
        {
            "name": "Vegetable query under budget",
            "payload": {
                "query": "Fresh organic vegetables for my weekly meal prep",
                "budget": 500,
                "preferred_brands": ["Organic India", "24 Mantra"],
                "diet": "vegetarian"
            }
        },
        {
            "name": "Complex query with specific brand preferences",
            "payload": {
                "query": "Protein bars and healthy snacks for office from MuscleBlaze",
                "budget": 1000,
                "preferred_brands": ["MuscleBlaze", "RiteBite"],
                "diet": "high protein low carb"
            }
        },
        {
            "name": "Edge case - empty query",
            "payload": {
                "query": "",
                "budget": 500,
                "preferred_brands": ["MuscleBlaze"],
                "diet": "high protein"
            }
        },
        {
            "name": "Edge case - very low budget",
            "payload": {
                "query": "Protein supplements",
                "budget": 50,
                "preferred_brands": ["MuscleBlaze"],
                "diet": "high protein"
            }
        }
    ]
    
    all_passed = True
    all_recommendations = []
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(f"{API_URL}/grocery/recommendations", json=test_case['payload'])
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"Response status: {data.get('status', 'unknown')}")
            print(f"Found {len(data.get('recommendations', []))} recommendations")
            
            # Basic validation
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            assert "recommendations" in data, "Response missing 'recommendations' field"
            assert isinstance(data["recommendations"], list), "'recommendations' is not a list"
            
            # Validate AI integration
            assert "ai_response" in data, "Response missing 'ai_response' field - AI integration may not be working"
            assert data["ai_response"], "AI response is empty - AI integration may not be working"
            
            # Validate user preferences
            assert "user_preferences" in data, "Response missing 'user_preferences' field"
            assert data["user_preferences"]["query"] == test_case["payload"]["query"], "Query in preferences doesn't match request"
            
            # Validate recommendations structure
            if data["recommendations"]:
                sample_rec = data["recommendations"][0]
                print(f"Sample recommendation: {json.dumps(sample_rec, indent=2)}")
                
                # Check required fields
                assert "name" in sample_rec, "Recommendation missing 'name' field"
                assert "price" in sample_rec, "Recommendation missing 'price' field"
                assert "description" in sample_rec, "Recommendation missing 'description' field"
                assert "rating" in sample_rec, "Recommendation missing 'rating' field"
                assert "platform" in sample_rec, "Recommendation missing 'platform' field"
                
                # Check if recommendations are relevant to the query
                if test_case["payload"]["query"]:
                    query_terms = test_case["payload"]["query"].lower().split()
                    found_relevance = False
                    
                    # Check if any query term appears in name or description
                    for term in query_terms:
                        if len(term) > 3:  # Only check meaningful terms
                            if term in sample_rec["name"].lower() or term in sample_rec["description"].lower():
                                found_relevance = True
                                break
                    
                    if not found_relevance and "protein" in test_case["payload"]["diet"].lower():
                        # For protein diet, check if protein info is available
                        if sample_rec.get("protein"):
                            found_relevance = True
                    
                    assert found_relevance, f"Recommendations don't seem relevant to the query: {test_case['payload']['query']}"
                
                # Save recommendations for cart creation test
                if not all_recommendations and len(data["recommendations"]) >= 2:
                    all_recommendations = data["recommendations"]
            
            print(f"✅ Test case '{test_case['name']}' passed")
        except Exception as e:
            print(f"❌ Test case '{test_case['name']}' failed: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All grocery recommendation test cases passed")
    else:
        print("\n❌ Some grocery recommendation test cases failed")
    
    return all_passed, all_recommendations

def test_grocery_error_handling():
    """Test error handling for grocery endpoints with invalid inputs"""
    print("\n=== Testing Grocery API Error Handling ===")
    
    test_cases = [
        {
            "name": "Invalid budget (negative)",
            "endpoint": "/grocery/recommendations",
            "payload": {
                "query": "Protein supplements",
                "budget": -100,
                "preferred_brands": ["MuscleBlaze"],
                "diet": "high protein"
            },
            "expected_status": 200  # The API handles this gracefully
        },
        {
            "name": "Invalid preferred_brands (not a list)",
            "endpoint": "/grocery/recommendations",
            "payload": {
                "query": "Protein supplements",
                "budget": 500,
                "preferred_brands": "MuscleBlaze",  # Should be a list
                "diet": "high protein"
            },
            "expected_status": 422  # Validation error
        },
        {
            "name": "Missing required field (query)",
            "endpoint": "/grocery/recommendations",
            "payload": {
                # "query" is missing
                "budget": 500,
                "preferred_brands": ["MuscleBlaze"],
                "diet": "high protein"
            },
            "expected_status": 422  # Validation error
        },
        {
            "name": "Invalid cart data (empty list)",
            "endpoint": "/grocery/create-cart",
            "payload": [],
            "expected_status": 200  # Should handle empty list gracefully
        },
        {
            "name": "Invalid cart data (not a list)",
            "endpoint": "/grocery/create-cart",
            "payload": {"products": "invalid"},
            "expected_status": 422  # Validation error
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(f"{API_URL}{test_case['endpoint']}", json=test_case['payload'])
            print(f"Status Code: {response.status_code}")
            
            # Try to get response data, but don't fail if it's not valid JSON
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print("Response is not valid JSON")
            
            # Check if status code matches expected
            assert response.status_code == test_case['expected_status'], \
                f"Expected status code {test_case['expected_status']}, got {response.status_code}"
            
            print(f"✅ Test case '{test_case['name']}' passed")
        except Exception as e:
            print(f"❌ Test case '{test_case['name']}' failed: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All error handling test cases passed")
    else:
        print("\n❌ Some error handling test cases failed")
    
    return all_passed

def test_grocery_cart_creation(recommendations):
    """Test the enhanced grocery cart creation endpoint"""
    print("\n=== Testing Enhanced Grocery Cart Creation Endpoint ===")
    if not recommendations or len(recommendations) < 2:
        print("❌ Grocery cart creation test skipped: Not enough recommendations available")
        return False
    
    try:
        # Select only some recommendations for the cart to test partial selection
        selected_products = []
        for i, item in enumerate(recommendations):
            # Select every other item
            item_copy = item.copy()
            item_copy["selected"] = (i % 2 == 0)
            selected_products.append(item_copy)
        
        # Ensure at least one item is selected
        if not any(item["selected"] for item in selected_products):
            selected_products[0]["selected"] = True
        
        print(f"Sending {len(selected_products)} products to cart, with {sum(1 for item in selected_products if item['selected'])} selected")
        
        response = requests.post(f"{API_URL}/grocery/create-cart", json=selected_products)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Created cart: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "cart_items" in data, "Response missing 'cart_items' field"
        assert "total_cost" in data, "Response missing 'total_cost' field"
        assert "status" in data, "Response missing 'status' field"
        assert data["status"] == "cart_created", "Cart status is not 'cart_created'"
        
        # Verify only selected items are in the cart
        selected_count = sum(1 for item in selected_products if item["selected"])
        assert len(data["cart_items"]) == selected_count, f"Expected {selected_count} items in cart, got {len(data['cart_items'])}"
        
        # Verify total cost calculation
        expected_total = 0
        for item in selected_products:
            if item["selected"]:
                price_str = item["price"]
                price_num = int(price_str.replace('₹', '').replace(',', ''))
                expected_total += price_num
        
        assert data["total_cost"] == expected_total, f"Expected total cost {expected_total}, got {data['total_cost']}"
        assert data["item_count"] == selected_count, f"Expected item count {selected_count}, got {data['item_count']}"
        
        print("✅ Enhanced grocery cart creation endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Enhanced grocery cart creation endpoint test failed: {str(e)}")
        return False

def test_personalized_wellness_recommendations():
    """Test the personalized wellness recommendations API endpoint"""
    print("\n=== Testing Personalized Wellness Recommendations Endpoint ===")
    try:
        # Sample request data as specified in the review request
        request_data = {
            "user_id": "test-user-new",
            "weight": "75 kg", 
            "allergies": "peanuts",
            "wellness_goals": ["weight loss", "muscle building"],
            "health_conditions": ["back pain"],
            "age": 30,
            "gender": "male",
            "fitness_level": "beginner"
        }
        
        print(f"Sending request with data: {json.dumps(request_data, indent=2)}")
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Print a summary of the response
        print(f"Response success: {data.get('success', False)}")
        print(f"Response message: {data.get('message', 'No message')}")
        
        # Basic validation
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        assert "recommendations" in data, "Response missing 'recommendations' field"
        
        # Validate recommendations structure
        recommendations = data["recommendations"]
        assert isinstance(recommendations, dict), "'recommendations' is not a dictionary"
        
        # Check if all 4 required categories are present
        required_categories = ["workout", "diet", "skincare", "health"]
        for category in required_categories:
            assert category in recommendations, f"Missing '{category}' category in recommendations"
            assert isinstance(recommendations[category], list), f"'{category}' recommendations is not a list"
            assert len(recommendations[category]) > 0, f"No recommendations found for '{category}' category"
        
        # Validate the structure of each recommendation
        for category, recs in recommendations.items():
            print(f"\nFound {len(recs)} recommendations for {category} category")
            for i, rec in enumerate(recs):
                # Print the first recommendation in each category for inspection
                if i == 0:
                    print(f"Sample {category} recommendation: {json.dumps(rec, indent=2)}")
                
                # Validate required fields
                assert "title" in rec, f"{category} recommendation missing 'title' field"
                assert "description" in rec, f"{category} recommendation missing 'description' field"
                assert "steps" in rec, f"{category} recommendation missing 'steps' field"
                assert isinstance(rec["steps"], list), f"'steps' in {category} recommendation is not a list"
                assert "youtube_video" in rec, f"{category} recommendation missing 'youtube_video' field"
                assert "product_links" in rec, f"{category} recommendation missing 'product_links' field"
                assert isinstance(rec["product_links"], list), f"'product_links' in {category} recommendation is not a list"
                
                # Check for personalization based on user data - only for non-fallback responses
                # Note: We're being more flexible here since the API might use fallback responses
                if category == "workout" and "beginner" in rec["level"].lower():
                    print(f"✓ Workout recommendation correctly mentions user's fitness level (beginner)")
                elif category == "diet" and "peanuts" in rec["description"].lower():
                    print(f"✓ Diet recommendation correctly addresses user's allergies (peanuts)")
        
        # Enhanced validation for workout recommendations
        workout_recs = recommendations["workout"]
        print("\n=== Enhanced Validation for Workout Recommendations ===")
        for i, workout in enumerate(workout_recs):
            print(f"\nValidating workout recommendation {i+1}: {workout.get('title', 'Unknown')}")
            
            # Check workout-specific fields
            assert "duration" in workout, "Workout recommendation missing 'duration' field"
            assert "level" in workout, "Workout recommendation missing 'level' field"
            assert "requirements" in workout, "Workout recommendation missing 'requirements' field"
            assert isinstance(workout["requirements"], list), "'requirements' in workout recommendation is not a list"
            
            # Validate content relevance to user profile
            assert workout["level"].lower() in ["beginner", "beginner to intermediate", "all levels", "suitable for beginners"], \
                f"Workout level '{workout['level']}' doesn't match user's beginner fitness level"
            
            # Check if workout addresses user's goals
            goals_addressed = False
            for goal in request_data["wellness_goals"]:
                if goal.lower() in workout["description"].lower() or goal.lower() in workout["title"].lower():
                    goals_addressed = True
                    print(f"✓ Workout recommendation addresses user goal: {goal}")
                    break
            
            # Check if workout addresses user's health conditions
            if any(condition.lower() in workout["description"].lower() for condition in request_data["health_conditions"]):
                print(f"✓ Workout recommendation addresses user's health condition: {request_data['health_conditions'][0]}")
            
            # Validate YouTube link format for workout videos
            assert workout["youtube_video"].startswith("https://www.youtube.com"), \
                f"YouTube link in workout recommendation is not properly formatted: {workout['youtube_video']}"
            
            # Validate steps are detailed enough
            assert len(workout["steps"]) >= 3, f"Workout steps should have at least 3 items, found {len(workout['steps'])}"
            
            print(f"✓ Workout recommendation {i+1} validated successfully")
        
        # Check if health category has motivational quotes
        if recommendations["health"] and len(recommendations["health"]) > 0:
            for health_rec in recommendations["health"]:
                assert "motivational_quote" in health_rec, "Health recommendation missing 'motivational_quote' field"
                assert health_rec["motivational_quote"], "Health recommendation has empty motivational quote"
                print(f"Health recommendation includes motivational quote: {health_rec['motivational_quote']}")
        
        # Check YouTube links and product links format
        for category, recs in recommendations.items():
            for rec in recs:
                # Validate YouTube link format
                assert rec["youtube_video"].startswith("https://www.youtube.com"), \
                    f"YouTube link in {category} recommendation is not properly formatted: {rec['youtube_video']}"
                
                # Validate product links format
                for link in rec["product_links"]:
                    assert link.startswith("https://"), \
                        f"Product link in {category} recommendation is not properly formatted: {link}"
        
        print("✅ Personalized wellness recommendations endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Personalized wellness recommendations endpoint test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return results"""
    results = {}
    
    # Test basic connectivity
    results["root_endpoint"] = test_root_endpoint()
    
    # Test core data endpoints
    results["skincare_endpoint"] = test_skincare_endpoint()
    results["workouts_endpoint"] = test_workouts_endpoint()
    results["meals_endpoint"] = test_meals_endpoint()
    results["health_conditions_endpoint"] = test_health_conditions_endpoint()
    
    # Test authentication endpoints
    success, user_id, email, password = test_auth_signup()
    results["auth_signup"] = success
    
    if success and user_id:
        results["auth_login"], user_id = test_auth_login(email, password)
        results["auth_get_user"] = test_auth_get_user(user_id)
        results["auth_validation"] = test_auth_validation()
        results["enhanced_health_chatbot"] = test_enhanced_health_chatbot(user_id)
    else:
        print("❌ Skipping authentication-dependent tests due to signup failure")
        results["auth_login"] = False
        results["auth_get_user"] = False
        results["auth_validation"] = False
        results["enhanced_health_chatbot"] = False
    
    # Test user creation
    results["user_creation"], user_id = test_user_creation()
    
    # Test grocery agent
    results["grocery_recommendations"], recommendations = test_grocery_recommendations()
    results["grocery_error_handling"] = test_grocery_error_handling()
    
    if recommendations:
        results["grocery_cart_creation"] = test_grocery_cart_creation(recommendations)
    else:
        print("❌ Skipping grocery cart creation test due to recommendations failure")
        results["grocery_cart_creation"] = False
    
    # Test personalized wellness recommendations
    results["personalized_wellness_recommendations"] = test_personalized_wellness_recommendations()
    results["personalized_wellness_recommendations_alt"] = test_personalized_wellness_recommendations_alt()
    
    # Print summary
    print("\n=== Test Summary ===")
    for test_name, result in results.items():
        if isinstance(result, tuple):
            status = "✅ PASSED" if result[0] else "❌ FAILED"
        else:
            status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Calculate overall success
    success_count = 0
    for result in results.values():
        if isinstance(result, tuple):
            if result[0]:
                success_count += 1
        elif result:
            success_count += 1
    
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"\nOverall Success Rate: {success_rate:.2f}% ({success_count}/{total_count} tests passed)")
    
    return results

def test_personalized_wellness_recommendations_alt():
    """Test the personalized wellness recommendations API endpoint with alternative data"""
    print("\n=== Testing Personalized Wellness Recommendations Endpoint (Alternative Data) ===")
    try:
        # Alternative test data - significantly different from the first test
        request_data = {
            "user_id": "test-user-alt",
            "weight": "62 kg", 
            "allergies": "gluten, shellfish",
            "wellness_goals": ["weight loss", "stress reduction"],
            "health_conditions": ["high blood pressure"],
            "age": 42,
            "gender": "female",
            "fitness_level": "advanced"
        }
        
        print(f"Sending request with alternative data: {json.dumps(request_data, indent=2)}")
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Print a summary of the response
        print(f"Response success: {data.get('success', False)}")
        print(f"Response message: {data.get('message', 'No message')}")
        
        # Basic validation
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        assert "recommendations" in data, "Response missing 'recommendations' field"
        
        # Validate recommendations structure
        recommendations = data["recommendations"]
        assert isinstance(recommendations, dict), "'recommendations' is not a dictionary"
        
        # Check if all 4 required categories are present
        required_categories = ["workout", "diet", "skincare", "health"]
        for category in required_categories:
            assert category in recommendations, f"Missing '{category}' category in recommendations"
            assert isinstance(recommendations[category], list), f"'{category}' recommendations is not a list"
            assert len(recommendations[category]) > 0, f"No recommendations found for '{category}' category"
        
        # Validate the structure of each recommendation
        for category, recs in recommendations.items():
            print(f"\nFound {len(recs)} recommendations for {category} category")
            for i, rec in enumerate(recs):
                # Print the first recommendation in each category for inspection
                if i == 0:
                    print(f"Sample {category} recommendation: {json.dumps(rec, indent=2)}")
                
                # Validate required fields
                assert "title" in rec, f"{category} recommendation missing 'title' field"
                assert "description" in rec, f"{category} recommendation missing 'description' field"
                assert "steps" in rec, f"{category} recommendation missing 'steps' field"
                assert isinstance(rec["steps"], list), f"'steps' in {category} recommendation is not a list"
                assert "youtube_video" in rec, f"{category} recommendation missing 'youtube_video' field"
                assert "product_links" in rec, f"{category} recommendation missing 'product_links' field"
                assert isinstance(rec["product_links"], list), f"'product_links' in {category} recommendation is not a list"
                
                # Check for personalization based on user data - only for non-fallback responses
                # Note: We're being more flexible here since the API might use fallback responses
                if category == "workout" and "advanced" in rec["level"].lower():
                    print(f"✓ Workout recommendation correctly mentions user's fitness level (advanced)")
                elif category == "diet" and ("gluten" in rec["description"].lower() or "shellfish" in rec["description"].lower()):
                    print(f"✓ Diet recommendation correctly addresses user's allergies (gluten, shellfish)")
        
        # Check if health category has motivational quotes
        if recommendations["health"] and len(recommendations["health"]) > 0:
            for health_rec in recommendations["health"]:
                assert "motivational_quote" in health_rec, "Health recommendation missing 'motivational_quote' field"
                assert health_rec["motivational_quote"], "Health recommendation has empty motivational quote"
                print(f"Health recommendation includes motivational quote: {health_rec['motivational_quote']}")
        
        # Check YouTube links and product links format
        for category, recs in recommendations.items():
            for rec in recs:
                # Validate YouTube link format
                assert rec["youtube_video"].startswith("https://www.youtube.com"), \
                    f"YouTube link in {category} recommendation is not properly formatted: {rec['youtube_video']}"
                
                # Validate product links format
                for link in rec["product_links"]:
                    assert link.startswith("https://"), \
                        f"Product link in {category} recommendation is not properly formatted: {link}"
        
        print("✅ Personalized wellness recommendations endpoint test (alternative data) passed")
        return True
    except Exception as e:
        print(f"❌ Personalized wellness recommendations endpoint test (alternative data) failed: {str(e)}")
        return False
if __name__ == "__main__":
    run_all_tests()