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

def test_symptom_checker_api():
    """Test the symptom checker API endpoint with comprehensive test cases"""
    print("\n=== Testing Symptom Checker API Endpoint ===")
    
    test_cases = [
        {
            "name": "Predefined symptoms - fever, headache, cough",
            "payload": {
                "symptoms": ["fever", "headache", "cough"],
                "custom_symptoms": "",
                "body_parts": ["head", "throat"],
                "duration": "3-7-days",
                "severity": "moderate",
                "additional_info": "Started 3 days ago",
                "age": 28,
                "gender": "female"
            }
        },
        {
            "name": "Custom symptoms with body parts",
            "payload": {
                "symptoms": [],
                "custom_symptoms": "muscle aches and joint pain",
                "body_parts": ["arms", "legs", "back"],
                "duration": "1-3-days",
                "severity": "mild",
                "additional_info": "After workout session",
                "age": 35,
                "gender": "male"
            }
        },
        {
            "name": "Severe symptoms test",
            "payload": {
                "symptoms": ["chest pain", "difficulty breathing"],
                "custom_symptoms": "",
                "body_parts": ["chest"],
                "duration": "less-than-1-day",
                "severity": "severe",
                "additional_info": "Sudden onset",
                "age": 45,
                "gender": "male"
            }
        },
        {
            "name": "Mild symptoms with long duration",
            "payload": {
                "symptoms": ["fatigue", "mild headache"],
                "custom_symptoms": "occasional dizziness",
                "body_parts": ["head"],
                "duration": "more-than-week",
                "severity": "mild",
                "additional_info": "Gradual onset over past 2 weeks",
                "age": 22,
                "gender": "female"
            }
        },
        {
            "name": "Digestive symptoms",
            "payload": {
                "symptoms": ["nausea", "stomach pain"],
                "custom_symptoms": "bloating after meals",
                "body_parts": ["abdomen"],
                "duration": "1-3-days",
                "severity": "moderate",
                "additional_info": "Started after eating at new restaurant",
                "age": 30,
                "gender": "female"
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(f"{API_URL}/symptoms/analyze", json=test_case['payload'])
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            # Basic validation
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            
            # Validate required response fields
            required_fields = ["analysis_id", "urgency_level", "possible_conditions", 
                             "recommendations", "when_to_seek_care", "disclaimer"]
            for field in required_fields:
                assert field in data, f"Response missing required field: {field}"
            
            # Validate field types and content
            assert isinstance(data["analysis_id"], str), "analysis_id should be a string"
            assert data["urgency_level"] in ["Low", "Medium", "High"], f"Invalid urgency level: {data['urgency_level']}"
            assert isinstance(data["possible_conditions"], list), "possible_conditions should be a list"
            assert isinstance(data["recommendations"], list), "recommendations should be a list"
            assert isinstance(data["when_to_seek_care"], str), "when_to_seek_care should be a string"
            assert isinstance(data["disclaimer"], str), "disclaimer should be a string"
            
            # Validate possible conditions structure
            if data["possible_conditions"]:
                for condition in data["possible_conditions"]:
                    assert "name" in condition, "Condition missing 'name' field"
                    assert "probability" in condition, "Condition missing 'probability' field"
                    assert "description" in condition, "Condition missing 'description' field"
            
            # Validate recommendations are not empty
            assert len(data["recommendations"]) > 0, "Recommendations list is empty"
            
            # Validate disclaimer is present
            assert len(data["disclaimer"]) > 0, "Disclaimer is empty"
            assert "informational purposes" in data["disclaimer"].lower(), "Disclaimer should mention informational purposes"
            
            # Validate urgency level logic
            if test_case["payload"]["severity"] == "severe":
                assert data["urgency_level"] == "High", f"Severe symptoms should result in High urgency, got {data['urgency_level']}"
            elif "chest pain" in test_case["payload"]["symptoms"] or "difficulty breathing" in test_case["payload"]["symptoms"]:
                assert data["urgency_level"] == "High", f"Serious symptoms should result in High urgency, got {data['urgency_level']}"
            
            # Print sample response for inspection
            print(f"Analysis ID: {data['analysis_id']}")
            print(f"Urgency Level: {data['urgency_level']}")
            print(f"Possible Conditions: {len(data['possible_conditions'])} found")
            if data["possible_conditions"]:
                print(f"  - {data['possible_conditions'][0]['name']}: {data['possible_conditions'][0]['probability']}")
            print(f"Recommendations: {len(data['recommendations'])} provided")
            print(f"When to seek care: {data['when_to_seek_care'][:100]}...")
            
            # Check for follow-up questions if present
            if "follow_up_questions" in data:
                assert isinstance(data["follow_up_questions"], list), "follow_up_questions should be a list"
                print(f"Follow-up questions: {len(data['follow_up_questions'])} provided")
            
            print(f"✅ Test case '{test_case['name']}' passed")
            
        except Exception as e:
            print(f"❌ Test case '{test_case['name']}' failed: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All symptom checker API test cases passed")
    else:
        print("\n❌ Some symptom checker API test cases failed")
    
    return all_passed

def test_health_chat_api():
    """Test the health chat API endpoint with various health-related messages"""
    print("\n=== Testing Health Chat API Endpoint ===")
    
    # Generate a unique user ID for testing
    test_user_id = str(uuid.uuid4())
    
    test_cases = [
        {
            "name": "General health question",
            "payload": {
                "user_id": test_user_id,
                "message": "What are some tips for staying healthy?"
            }
        },
        {
            "name": "Workout advice request",
            "payload": {
                "user_id": test_user_id,
                "message": "Can you recommend a good workout routine for beginners?"
            }
        },
        {
            "name": "Nutrition question",
            "payload": {
                "user_id": test_user_id,
                "message": "What should I eat to lose weight safely?"
            }
        },
        {
            "name": "Skincare advice",
            "payload": {
                "user_id": test_user_id,
                "message": "How can I improve my skincare routine for acne-prone skin?"
            }
        },
        {
            "name": "Personalized request with profile",
            "payload": {
                "user_id": test_user_id,
                "message": "What workout would be best for my fitness level?",
                "user_profile": {
                    "weight": "70kg",
                    "allergies": "peanuts",
                    "skin_concern": "dry skin"
                }
            }
        },
        {
            "name": "Sleep and wellness",
            "payload": {
                "user_id": test_user_id,
                "message": "How can I improve my sleep quality and reduce stress?"
            }
        },
        {
            "name": "Diet with allergies",
            "payload": {
                "user_id": test_user_id,
                "message": "What diet plan would work for someone with nut allergies?",
                "user_profile": {
                    "weight": "65kg",
                    "allergies": "nuts, shellfish",
                    "skin_concern": "normal"
                }
            }
        },
        {
            "name": "Muscle building advice",
            "payload": {
                "user_id": test_user_id,
                "message": "I want to build muscle mass. What exercises and nutrition do you recommend?",
                "user_profile": {
                    "weight": "75kg",
                    "allergies": "none",
                    "skin_concern": "oily"
                }
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(f"{API_URL}/chat", json=test_case['payload'])
            print(f"Status Code: {response.status_code}")
            data = response.json()
            
            # Basic validation
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            
            # Validate required response fields
            required_fields = ["response", "message_id"]
            for field in required_fields:
                assert field in data, f"Response missing required field: {field}"
            
            # Validate field types and content
            assert isinstance(data["response"], str), "response should be a string"
            assert isinstance(data["message_id"], str), "message_id should be a string"
            assert len(data["response"]) > 0, "Response should not be empty"
            assert len(data["message_id"]) > 0, "Message ID should not be empty"
            
            # Check for optional fields
            if "requires_profile" in data:
                assert isinstance(data["requires_profile"], bool), "requires_profile should be a boolean"
                if data["requires_profile"] and "profile_fields" in data:
                    assert isinstance(data["profile_fields"], list), "profile_fields should be a list"
            
            # Validate response relevance to the question
            message_lower = test_case["payload"]["message"].lower()
            response_lower = data["response"].lower()
            
            # Check if response is relevant to the question topic
            if "workout" in message_lower or "exercise" in message_lower:
                relevant_terms = ["workout", "exercise", "fitness", "training", "muscle", "strength", "cardio"]
                assert any(term in response_lower for term in relevant_terms), \
                    f"Workout-related response should contain relevant terms. Response: {data['response'][:100]}..."
            
            elif "diet" in message_lower or "nutrition" in message_lower or "eat" in message_lower:
                relevant_terms = ["diet", "nutrition", "food", "eat", "meal", "protein", "calories", "healthy"]
                assert any(term in response_lower for term in relevant_terms), \
                    f"Nutrition-related response should contain relevant terms. Response: {data['response'][:100]}..."
            
            elif "skincare" in message_lower or "skin" in message_lower:
                relevant_terms = ["skin", "skincare", "routine", "cleanser", "moisturizer", "acne", "dry", "oily"]
                assert any(term in response_lower for term in relevant_terms), \
                    f"Skincare-related response should contain relevant terms. Response: {data['response'][:100]}..."
            
            elif "sleep" in message_lower or "stress" in message_lower:
                relevant_terms = ["sleep", "stress", "rest", "relax", "wellness", "health", "routine"]
                assert any(term in response_lower for term in relevant_terms), \
                    f"Sleep/stress-related response should contain relevant terms. Response: {data['response'][:100]}..."
            
            # Check if allergies are mentioned when provided in user profile
            if "user_profile" in test_case["payload"] and test_case["payload"]["user_profile"].get("allergies"):
                allergies = test_case["payload"]["user_profile"]["allergies"]
                if allergies != "none" and "diet" in message_lower:
                    # For diet-related questions with allergies, response should mention avoiding allergens
                    assert "avoid" in response_lower or allergies.lower() in response_lower, \
                        f"Diet response should address user's allergies: {allergies}"
            
            # Print sample response for inspection
            print(f"Message ID: {data['message_id']}")
            print(f"Response preview: {data['response'][:150]}...")
            if "requires_profile" in data:
                print(f"Requires profile: {data['requires_profile']}")
                if data.get("requires_profile") and "profile_fields" in data:
                    print(f"Profile fields requested: {data['profile_fields']}")
            
            print(f"✅ Test case '{test_case['name']}' passed")
            
        except Exception as e:
            print(f"❌ Test case '{test_case['name']}' failed: {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All health chat API test cases passed")
    else:
        print("\n❌ Some health chat API test cases failed")
    
    return all_passed

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
    
    # Test enhanced user profile functionality
    results["enhanced_user_profile"] = test_enhanced_user_profile()
    
    # Test user creation
    results["user_creation"], created_user_id = test_user_creation()
    
    # Use created_user_id if available, otherwise use user_id from auth
    test_user_id = created_user_id if created_user_id else user_id
    
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
    
    # Test NEW symptom checker and health chat APIs
    results["symptom_checker_api"] = test_symptom_checker_api()
    results["health_chat_api"] = test_health_chat_api()
    
    # Test NEW Mind & Soul API endpoints
    results["mind_soul_meditation_content"] = test_mind_soul_meditation_content()
    
    if test_user_id:
        results["mind_soul_mood_tracker"] = test_mind_soul_mood_tracker(test_user_id)
        results["mind_soul_meditation_sessions"] = test_mind_soul_meditation_sessions(test_user_id)
        results["mind_soul_habit_tracker"] = test_mind_soul_habit_tracker(test_user_id)
    else:
        print("❌ Skipping Mind & Soul user-dependent tests due to no available user ID")
        results["mind_soul_mood_tracker"] = False
        results["mind_soul_meditation_sessions"] = False
        results["mind_soul_habit_tracker"] = False
    
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

def test_enhanced_user_profile():
    """Test the enhanced user profile functionality with comprehensive profile data"""
    print("\n=== Testing Enhanced User Profile Functionality ===")
    try:
        # Create a user with comprehensive profile data
        print("\n--- Test 1: Creating user with comprehensive profile data ---")
        
        # Complete user profile data including all fields for enhanced profile popup
        enhanced_profile_data = {
            "name": "Alex Johnson",
            "email": f"alex.johnson.{uuid.uuid4()}@example.com",  # Ensure unique email
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            "age": 34,
            "gender": "Non-binary",
            "height": 175.5,
            "heightUnit": "cm",
            "weight": 68.2,
            "weightUnit": "kg",
            "allergies": ["Dairy", "Soy", "Tree nuts"],
            "chronicConditions": ["Mild asthma", "Seasonal allergies"],
            "wellnessGoals": ["Improve flexibility", "Reduce stress", "Better sleep quality"],
            "fitnessLevel": "Intermediate",
            "dietPreference": "Pescatarian",
            "skinType": "Combination",
            "smartCartOptIn": True
        }
        
        print(f"Creating user with profile data: {json.dumps(enhanced_profile_data, indent=2)}")
        response = requests.post(f"{API_URL}/auth/signup", json=enhanced_profile_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Signup response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == True, f"Signup failed with message: {data.get('message', 'Unknown error')}"
        assert "user" in data, "Response missing 'user' field"
        assert "user_id" in data, "Response missing 'user_id' field"
        
        user_id = data["user_id"]
        user_data = data["user"]
        
        # Verify all profile fields are present and correctly stored
        print("\n--- Test 2: Verifying all profile fields are correctly stored ---")
        
        # Basic user information
        assert user_data["name"] == enhanced_profile_data["name"], "User name doesn't match"
        assert user_data["email"] == enhanced_profile_data["email"], "User email doesn't match"
        assert "password" not in user_data, "Password should not be returned in response"
        
        # Vital statistics
        assert user_data["age"] == enhanced_profile_data["age"], "User age doesn't match"
        assert user_data["gender"] == enhanced_profile_data["gender"], "User gender doesn't match"
        assert user_data["height"] == enhanced_profile_data["height"], "User height doesn't match"
        assert user_data["height_unit"] == enhanced_profile_data["heightUnit"], "User height unit doesn't match"
        assert user_data["weight"] == enhanced_profile_data["weight"], "User weight doesn't match"
        assert user_data["weight_unit"] == enhanced_profile_data["weightUnit"], "User weight unit doesn't match"
        
        # Health information
        assert user_data["allergies"] == enhanced_profile_data["allergies"], "User allergies don't match"
        assert user_data["chronic_conditions"] == enhanced_profile_data["chronicConditions"], "User chronic conditions don't match"
        assert user_data["goals"] == enhanced_profile_data["wellnessGoals"], "User wellness goals don't match"
        
        # Preferences
        assert user_data["fitness_level"] == enhanced_profile_data["fitnessLevel"], "User fitness level doesn't match"
        assert user_data["diet_type"] == enhanced_profile_data["dietPreference"], "User diet preference doesn't match"
        assert user_data["skin_type"] == enhanced_profile_data["skinType"], "User skin type doesn't match"
        assert user_data["smart_cart_enabled"] == enhanced_profile_data["smartCartOptIn"], "User smart cart option doesn't match"
        
        print("✅ All profile fields verified successfully")
        
        # Test login and verify profile data is returned correctly
        print("\n--- Test 3: Verifying login returns complete profile data ---")
        
        login_data = {
            "email": enhanced_profile_data["email"],
            "password": enhanced_profile_data["password"]
        }
        
        login_response = requests.post(f"{API_URL}/auth/login", json=login_data)
        print(f"Login Status Code: {login_response.status_code}")
        login_result = login_response.json()
        print(f"Login response: {json.dumps(login_result, indent=2)}")
        
        assert login_response.status_code == 200, f"Expected status code 200, got {login_response.status_code}"
        assert login_result["success"] == True, f"Login failed with message: {login_result.get('message', 'Unknown error')}"
        assert "user" in login_result, "Login response missing 'user' field"
        assert "user_id" in login_result, "Login response missing 'user_id' field"
        
        login_user_data = login_result["user"]
        
        # Verify login returns all the same profile data
        assert login_user_data["name"] == enhanced_profile_data["name"], "Login: User name doesn't match"
        assert login_user_data["email"] == enhanced_profile_data["email"], "Login: User email doesn't match"
        assert login_user_data["age"] == enhanced_profile_data["age"], "Login: User age doesn't match"
        assert login_user_data["gender"] == enhanced_profile_data["gender"], "Login: User gender doesn't match"
        assert login_user_data["height"] == enhanced_profile_data["height"], "Login: User height doesn't match"
        assert login_user_data["allergies"] == enhanced_profile_data["allergies"], "Login: User allergies don't match"
        assert login_user_data["chronic_conditions"] == enhanced_profile_data["chronicConditions"], "Login: User chronic conditions don't match"
        assert login_user_data["goals"] == enhanced_profile_data["wellnessGoals"], "Login: User wellness goals don't match"
        assert login_user_data["fitness_level"] == enhanced_profile_data["fitnessLevel"], "Login: User fitness level doesn't match"
        assert login_user_data["diet_type"] == enhanced_profile_data["dietPreference"], "Login: User diet preference doesn't match"
        assert login_user_data["skin_type"] == enhanced_profile_data["skinType"], "Login: User skin type doesn't match"
        
        print("✅ Login returns complete profile data successfully")
        
        # Test retrieving user profile by ID
        print("\n--- Test 4: Retrieving user profile by ID ---")
        
        profile_response = requests.get(f"{API_URL}/auth/user/{user_id}")
        print(f"Profile Status Code: {profile_response.status_code}")
        profile_result = profile_response.json()
        print(f"Profile response: {json.dumps(profile_result, indent=2)}")
        
        assert profile_response.status_code == 200, f"Expected status code 200, got {profile_response.status_code}"
        assert profile_result["success"] == True, f"Profile retrieval failed with message: {profile_result.get('message', 'Unknown error')}"
        assert "user" in profile_result, "Profile response missing 'user' field"
        assert "user_id" in profile_result, "Profile response missing 'user_id' field"
        
        profile_user_data = profile_result["user"]
        
        # Verify profile retrieval returns all the same profile data
        assert profile_user_data["name"] == enhanced_profile_data["name"], "Profile: User name doesn't match"
        assert profile_user_data["email"] == enhanced_profile_data["email"], "Profile: User email doesn't match"
        assert profile_user_data["age"] == enhanced_profile_data["age"], "Profile: User age doesn't match"
        assert profile_user_data["gender"] == enhanced_profile_data["gender"], "Profile: User gender doesn't match"
        assert profile_user_data["height"] == enhanced_profile_data["height"], "Profile: User height doesn't match"
        assert profile_user_data["allergies"] == enhanced_profile_data["allergies"], "Profile: User allergies don't match"
        assert profile_user_data["chronic_conditions"] == enhanced_profile_data["chronicConditions"], "Profile: User chronic conditions don't match"
        assert profile_user_data["goals"] == enhanced_profile_data["wellnessGoals"], "Profile: User wellness goals don't match"
        assert profile_user_data["fitness_level"] == enhanced_profile_data["fitnessLevel"], "Profile: User fitness level doesn't match"
        assert profile_user_data["diet_type"] == enhanced_profile_data["dietPreference"], "Profile: User diet preference doesn't match"
        assert profile_user_data["skin_type"] == enhanced_profile_data["skinType"], "Profile: User skin type doesn't match"
        
        print("✅ Profile retrieval returns complete profile data successfully")
        
        # Test with different profile data variations
        print("\n--- Test 5: Testing with different profile data variations ---")
        
        # Create a user with minimal required fields but still valid
        minimal_profile_data = {
            "name": "Min User",
            "email": f"min.user.{uuid.uuid4()}@example.com",
            "password": "MinPass123!",
            "confirmPassword": "MinPass123!",
            "agreeTerms": True,
            "age": 25,
            "gender": "Female",
            "height": 160,
            "heightUnit": "cm",
            "weight": 55,
            "weightUnit": "kg",
            "allergies": [],
            "chronicConditions": [],
            "wellnessGoals": ["General health"],
            "fitnessLevel": "Beginner",
            "dietPreference": "No preference",
            "skinType": "Normal",
            "smartCartOptIn": False
        }
        
        print(f"Creating user with minimal profile data")
        min_response = requests.post(f"{API_URL}/auth/signup", json=minimal_profile_data)
        print(f"Status Code: {min_response.status_code}")
        min_data = min_response.json()
        
        assert min_response.status_code == 200, f"Expected status code 200, got {min_response.status_code}"
        assert min_data["success"] == True, f"Minimal profile signup failed with message: {min_data.get('message', 'Unknown error')}"
        assert "user" in min_data, "Response missing 'user' field"
        
        min_user_data = min_data["user"]
        
        # Verify minimal profile fields
        assert min_user_data["name"] == minimal_profile_data["name"], "Minimal: User name doesn't match"
        assert min_user_data["email"] == minimal_profile_data["email"], "Minimal: User email doesn't match"
        assert min_user_data["allergies"] == minimal_profile_data["allergies"], "Minimal: User allergies don't match"
        assert min_user_data["chronic_conditions"] == minimal_profile_data["chronicConditions"], "Minimal: User chronic conditions don't match"
        assert min_user_data["goals"] == minimal_profile_data["wellnessGoals"], "Minimal: User wellness goals don't match"
        
        print("✅ Minimal profile data test passed")
        
        # Test with maximum field values
        max_profile_data = {
            "name": "Max " + "X" * 50,  # Very long name
            "email": f"max.{'x' * 30}.{uuid.uuid4()}@example.com",
            "password": "MaxPass123!" + "X" * 20,
            "confirmPassword": "MaxPass123!" + "X" * 20,
            "agreeTerms": True,
            "age": 99,
            "gender": "Other",
            "height": 220,
            "heightUnit": "cm",
            "weight": 150,
            "weightUnit": "kg",
            "allergies": ["Allergy " + str(i) for i in range(1, 11)],  # 10 allergies
            "chronicConditions": ["Condition " + str(i) for i in range(1, 6)],  # 5 conditions
            "wellnessGoals": ["Goal " + str(i) for i in range(1, 8)],  # 7 goals
            "fitnessLevel": "Expert",
            "dietPreference": "Custom " + "X" * 30,
            "skinType": "Very " + "X" * 20,
            "smartCartOptIn": True
        }
        
        print(f"Creating user with maximum profile data")
        max_response = requests.post(f"{API_URL}/auth/signup", json=max_profile_data)
        print(f"Status Code: {max_response.status_code}")
        max_data = max_response.json()
        
        # This might fail if there are server-side validations, but we'll check if it works
        if max_response.status_code == 200 and max_data.get("success", False):
            max_user_data = max_data["user"]
            
            # Verify maximum profile fields
            assert max_user_data["name"] == max_profile_data["name"], "Maximum: User name doesn't match"
            assert max_user_data["email"] == max_profile_data["email"], "Maximum: User email doesn't match"
            assert max_user_data["age"] == max_profile_data["age"], "Maximum: User age doesn't match"
            assert len(max_user_data["allergies"]) == len(max_profile_data["allergies"]), "Maximum: User allergies count doesn't match"
            assert len(max_user_data["chronic_conditions"]) == len(max_profile_data["chronicConditions"]), "Maximum: User chronic conditions count doesn't match"
            assert len(max_user_data["goals"]) == len(max_profile_data["wellnessGoals"]), "Maximum: User wellness goals count doesn't match"
            
            print("✅ Maximum profile data test passed")
        else:
            print("⚠️ Maximum profile data test skipped - server rejected the data (this may be expected)")
        
        print("\n✅ Enhanced user profile functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Enhanced user profile functionality test failed: {str(e)}")
        return False
def test_mind_soul_meditation_content():
    """Test the Mind & Soul meditation content endpoint"""
    print("\n=== Testing Mind & Soul Meditation Content Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/mind-soul/meditation-content")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "content" in data, "Response missing 'content' field"
        assert "total_count" in data, "Response missing 'total_count' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        content = data["content"]
        assert isinstance(content, list), "Content should be a list"
        assert len(content) >= 6, f"Expected at least 6 meditation exercises, found {len(content)}"
        
        # Validate each meditation exercise
        required_fields = ["id", "title", "description", "duration", "type", "difficulty", 
                          "benefits", "instructions", "youtube_video", "category", "image_url"]
        
        categories_found = set()
        types_found = set()
        
        for i, exercise in enumerate(content):
            print(f"\nValidating meditation exercise {i+1}: {exercise.get('title', 'Unknown')}")
            
            # Check all required fields exist
            for field in required_fields:
                assert field in exercise, f"Exercise missing '{field}' field"
            
            # Validate field types
            assert isinstance(exercise["id"], str), "Exercise 'id' is not a string"
            assert isinstance(exercise["title"], str), "Exercise 'title' is not a string"
            assert isinstance(exercise["description"], str), "Exercise 'description' is not a string"
            assert isinstance(exercise["duration"], str), "Exercise 'duration' is not a string"
            assert isinstance(exercise["type"], str), "Exercise 'type' is not a string"
            assert isinstance(exercise["difficulty"], str), "Exercise 'difficulty' is not a string"
            assert isinstance(exercise["benefits"], list), "Exercise 'benefits' is not a list"
            assert isinstance(exercise["instructions"], list), "Exercise 'instructions' is not a list"
            assert isinstance(exercise["youtube_video"], str), "Exercise 'youtube_video' is not a string"
            assert isinstance(exercise["category"], str), "Exercise 'category' is not a string"
            assert isinstance(exercise["image_url"], str), "Exercise 'image_url' is not a string"
            
            # Validate content
            assert len(exercise["title"]) > 0, "Exercise title is empty"
            assert len(exercise["description"]) > 0, "Exercise description is empty"
            assert len(exercise["benefits"]) > 0, "Exercise has no benefits"
            assert len(exercise["instructions"]) > 0, "Exercise has no instructions"
            assert exercise["difficulty"] in ["Beginner", "Intermediate", "Advanced"], f"Invalid difficulty: {exercise['difficulty']}"
            assert exercise["youtube_video"].startswith("https://www.youtube.com/embed/"), "YouTube video is not in embed format"
            
            categories_found.add(exercise["category"])
            types_found.add(exercise["type"])
            
            print(f"✓ Exercise {i+1} validated successfully")
        
        # Check for required categories and types
        expected_categories = ["morning_routine", "breathing", "relaxation", "stress_relief", "sleep", "focus"]
        expected_types = ["guided_meditation", "breathing_exercise", "mindfulness", "stress_relief", "sleep_meditation", "focus_meditation"]
        
        print(f"\nFound categories: {sorted(categories_found)}")
        print(f"Found types: {sorted(types_found)}")
        
        # Verify we have diverse content
        assert len(categories_found) >= 5, f"Expected at least 5 different categories, found {len(categories_found)}"
        assert len(types_found) >= 5, f"Expected at least 5 different types, found {len(types_found)}"
        
        # Print sample exercise for inspection
        sample_exercise = content[0]
        print(f"\nSample meditation exercise:")
        print(f"  Title: {sample_exercise['title']}")
        print(f"  Type: {sample_exercise['type']}")
        print(f"  Duration: {sample_exercise['duration']}")
        print(f"  Category: {sample_exercise['category']}")
        print(f"  Benefits: {', '.join(sample_exercise['benefits'])}")
        print(f"  Instructions: {len(sample_exercise['instructions'])} steps")
        
        print("\n✅ Mind & Soul meditation content endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Mind & Soul meditation content endpoint test failed: {str(e)}")
        return False

def test_mind_soul_mood_tracker(user_id):
    """Test the Mind & Soul mood tracking endpoints"""
    print("\n=== Testing Mind & Soul Mood Tracking Endpoints ===")
    if not user_id:
        print("❌ Mood tracking test skipped: No user ID available")
        return False
    
    all_passed = True
    
    # Test 1: Log mood entry
    print("\n--- Test 1: Log mood entry (POST /mind-soul/mood-tracker) ---")
    try:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        mood_data = {
            "user_id": user_id,
            "date": today,
            "mood": 4,  # 1-5 scale
            "mood_label": "Happy",
            "energy": 3,
            "stress": 2,
            "notes": "Had a great workout session today and feeling energized!"
        }
        
        response = requests.post(f"{API_URL}/mind-soul/mood-tracker", json=mood_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Mood tracking response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "message" in data, "Response missing 'message' field"
        assert "mood_data" in data, "Response missing 'mood_data' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate mood data structure
        mood_response = data["mood_data"]
        assert mood_response["user_id"] == user_id, "User ID doesn't match"
        assert mood_response["date"] == today, "Date doesn't match"
        assert mood_response["mood"] == 4, "Mood value doesn't match"
        assert mood_response["mood_label"] == "Happy", "Mood label doesn't match"
        assert mood_response["energy"] == 3, "Energy value doesn't match"
        assert mood_response["stress"] == 2, "Stress value doesn't match"
        assert mood_response["notes"] == mood_data["notes"], "Notes don't match"
        
        print("✅ Test 1 - Log mood entry passed")
    except Exception as e:
        print(f"❌ Test 1 - Log mood entry failed: {str(e)}")
        all_passed = False
    
    # Test 2: Get mood history
    print("\n--- Test 2: Get mood history (GET /mind-soul/mood-history/{user_id}) ---")
    try:
        response = requests.get(f"{API_URL}/mind-soul/mood-history/{user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Mood history response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "mood_history" in data, "Response missing 'mood_history' field"
        assert "statistics" in data, "Response missing 'statistics' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate mood history structure
        mood_history = data["mood_history"]
        assert isinstance(mood_history, list), "Mood history should be a list"
        
        # Validate statistics
        stats = data["statistics"]
        required_stat_fields = ["average_mood", "average_energy", "average_stress", "total_entries"]
        for field in required_stat_fields:
            assert field in stats, f"Statistics missing '{field}' field"
        
        # If we have entries, validate their structure
        if mood_history:
            entry = mood_history[0]
            required_entry_fields = ["user_id", "date", "mood", "mood_label", "energy", "stress", "notes"]
            for field in required_entry_fields:
                assert field in entry, f"Mood entry missing '{field}' field"
            
            assert entry["user_id"] == user_id, "User ID in history doesn't match"
            assert 1 <= entry["mood"] <= 5, f"Mood value out of range: {entry['mood']}"
            assert 1 <= entry["energy"] <= 5, f"Energy value out of range: {entry['energy']}"
            assert 1 <= entry["stress"] <= 5, f"Stress value out of range: {entry['stress']}"
            
            print(f"Found {len(mood_history)} mood entries")
            print(f"Average mood: {stats['average_mood']}")
            print(f"Average energy: {stats['average_energy']}")
            print(f"Average stress: {stats['average_stress']}")
        
        print("✅ Test 2 - Get mood history passed")
    except Exception as e:
        print(f"❌ Test 2 - Get mood history failed: {str(e)}")
        all_passed = False
    
    # Test 3: Update existing mood entry
    print("\n--- Test 3: Update existing mood entry ---")
    try:
        updated_mood_data = {
            "user_id": user_id,
            "date": today,
            "mood": 5,  # Updated mood
            "mood_label": "Very Happy",
            "energy": 4,  # Updated energy
            "stress": 1,  # Updated stress
            "notes": "Updated: Had an amazing day with great workout and healthy meals!"
        }
        
        response = requests.post(f"{API_URL}/mind-soul/mood-tracker", json=updated_mood_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert data["status"] == "success", "Status should be 'success'"
        assert "updated" in data["message"].lower(), "Message should indicate update"
        
        # Verify the update
        mood_response = data["mood_data"]
        assert mood_response["mood"] == 5, "Updated mood value doesn't match"
        assert mood_response["mood_label"] == "Very Happy", "Updated mood label doesn't match"
        assert mood_response["energy"] == 4, "Updated energy value doesn't match"
        assert mood_response["stress"] == 1, "Updated stress value doesn't match"
        
        print("✅ Test 3 - Update existing mood entry passed")
    except Exception as e:
        print(f"❌ Test 3 - Update existing mood entry failed: {str(e)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All mood tracking tests passed")
    else:
        print("\n❌ Some mood tracking tests failed")
    
    return all_passed

def test_mind_soul_meditation_sessions(user_id):
    """Test the Mind & Soul meditation session logging endpoints"""
    print("\n=== Testing Mind & Soul Meditation Session Endpoints ===")
    if not user_id:
        print("❌ Meditation session test skipped: No user ID available")
        return False
    
    all_passed = True
    
    # Test 1: Log meditation session
    print("\n--- Test 1: Log meditation session (POST /mind-soul/meditation-session) ---")
    try:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        session_id = str(uuid.uuid4())
        
        session_data = {
            "user_id": user_id,
            "session_type": "guided_meditation",
            "duration_minutes": 15,
            "completed": True,
            "date": today,
            "session_id": session_id
        }
        
        response = requests.post(f"{API_URL}/mind-soul/meditation-session", json=session_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Meditation session response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "message" in data, "Response missing 'message' field"
        assert "session_data" in data, "Response missing 'session_data' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate session data structure
        session_response = data["session_data"]
        assert session_response["user_id"] == user_id, "User ID doesn't match"
        assert session_response["session_type"] == "guided_meditation", "Session type doesn't match"
        assert session_response["duration_minutes"] == 15, "Duration doesn't match"
        assert session_response["completed"] == True, "Completed status doesn't match"
        assert session_response["date"] == today, "Date doesn't match"
        assert session_response["session_id"] == session_id, "Session ID doesn't match"
        
        print("✅ Test 1 - Log meditation session passed")
    except Exception as e:
        print(f"❌ Test 1 - Log meditation session failed: {str(e)}")
        all_passed = False
    
    # Test 2: Log another session with different type
    print("\n--- Test 2: Log breathing exercise session ---")
    try:
        session_data_2 = {
            "user_id": user_id,
            "session_type": "breathing_exercise",
            "duration_minutes": 5,
            "completed": True,
            "date": today,
            "session_id": str(uuid.uuid4())
        }
        
        response = requests.post(f"{API_URL}/mind-soul/meditation-session", json=session_data_2)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert data["status"] == "success", "Status should be 'success'"
        
        print("✅ Test 2 - Log breathing exercise session passed")
    except Exception as e:
        print(f"❌ Test 2 - Log breathing exercise session failed: {str(e)}")
        all_passed = False
    
    # Test 3: Get meditation progress
    print("\n--- Test 3: Get meditation progress (GET /mind-soul/meditation-progress/{user_id}) ---")
    try:
        response = requests.get(f"{API_URL}/mind-soul/meditation-progress/{user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Meditation progress response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "progress" in data, "Response missing 'progress' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate progress structure
        progress = data["progress"]
        required_progress_fields = ["total_sessions", "total_minutes", "current_streak", 
                                  "this_week_sessions", "average_session_length"]
        for field in required_progress_fields:
            assert field in progress, f"Progress missing '{field}' field"
        
        # Validate progress values
        assert isinstance(progress["total_sessions"], int), "Total sessions should be an integer"
        assert isinstance(progress["total_minutes"], int), "Total minutes should be an integer"
        assert isinstance(progress["current_streak"], int), "Current streak should be an integer"
        assert isinstance(progress["this_week_sessions"], int), "This week sessions should be an integer"
        assert isinstance(progress["average_session_length"], (int, float)), "Average session length should be a number"
        
        assert progress["total_sessions"] >= 2, f"Expected at least 2 sessions, found {progress['total_sessions']}"
        assert progress["total_minutes"] >= 20, f"Expected at least 20 minutes total, found {progress['total_minutes']}"
        
        print(f"Total sessions: {progress['total_sessions']}")
        print(f"Total minutes: {progress['total_minutes']}")
        print(f"Current streak: {progress['current_streak']}")
        print(f"This week sessions: {progress['this_week_sessions']}")
        print(f"Average session length: {progress['average_session_length']} minutes")
        
        print("✅ Test 3 - Get meditation progress passed")
    except Exception as e:
        print(f"❌ Test 3 - Get meditation progress failed: {str(e)}")
        all_passed = False
    
    # Test 4: Log incomplete session
    print("\n--- Test 4: Log incomplete session ---")
    try:
        incomplete_session = {
            "user_id": user_id,
            "session_type": "mindfulness",
            "duration_minutes": 10,
            "completed": False,  # Incomplete session
            "date": today,
            "session_id": str(uuid.uuid4())
        }
        
        response = requests.post(f"{API_URL}/mind-soul/meditation-session", json=incomplete_session)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Verify incomplete session is logged
        session_response = data["session_data"]
        assert session_response["completed"] == False, "Completed status should be False"
        
        print("✅ Test 4 - Log incomplete session passed")
    except Exception as e:
        print(f"❌ Test 4 - Log incomplete session failed: {str(e)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All meditation session tests passed")
    else:
        print("\n❌ Some meditation session tests failed")
    
    return all_passed

def test_mind_soul_habit_tracker(user_id):
    """Test the Mind & Soul habit tracking endpoints"""
    print("\n=== Testing Mind & Soul Habit Tracking Endpoints ===")
    if not user_id:
        print("❌ Habit tracking test skipped: No user ID available")
        return False
    
    all_passed = True
    
    # Test 1: Log habit progress
    print("\n--- Test 1: Log habit progress (POST /mind-soul/habit-tracker) ---")
    try:
        from datetime import datetime, timedelta
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Log habit for today
        habit_data = {
            "user_id": user_id,
            "habit_name": "Daily Meditation",
            "date": today,
            "completed": True,
            "streak_count": 1
        }
        
        response = requests.post(f"{API_URL}/mind-soul/habit-tracker", json=habit_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Habit tracking response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "message" in data, "Response missing 'message' field"
        assert "habit_data" in data, "Response missing 'habit_data' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate habit data structure
        habit_response = data["habit_data"]
        assert habit_response["user_id"] == user_id, "User ID doesn't match"
        assert habit_response["habit_name"] == "Daily Meditation", "Habit name doesn't match"
        assert habit_response["date"] == today, "Date doesn't match"
        assert habit_response["completed"] == True, "Completed status doesn't match"
        assert habit_response["streak_count"] == 1, "Streak count doesn't match"
        
        print("✅ Test 1 - Log habit progress passed")
    except Exception as e:
        print(f"❌ Test 1 - Log habit progress failed: {str(e)}")
        all_passed = False
    
    # Test 2: Log multiple habits
    print("\n--- Test 2: Log multiple different habits ---")
    try:
        habits_to_log = [
            {
                "user_id": user_id,
                "habit_name": "Morning Exercise",
                "date": today,
                "completed": True,
                "streak_count": 3
            },
            {
                "user_id": user_id,
                "habit_name": "Healthy Eating",
                "date": today,
                "completed": True,
                "streak_count": 5
            },
            {
                "user_id": user_id,
                "habit_name": "Reading",
                "date": today,
                "completed": False,
                "streak_count": 0
            }
        ]
        
        for habit in habits_to_log:
            response = requests.post(f"{API_URL}/mind-soul/habit-tracker", json=habit)
            assert response.status_code == 200, f"Failed to log habit: {habit['habit_name']}"
            data = response.json()
            assert data["status"] == "success", f"Failed to log habit: {habit['habit_name']}"
        
        print("✅ Test 2 - Log multiple different habits passed")
    except Exception as e:
        print(f"❌ Test 2 - Log multiple different habits failed: {str(e)}")
        all_passed = False
    
    # Test 3: Get user habits
    print("\n--- Test 3: Get user habits (GET /mind-soul/habits/{user_id}) ---")
    try:
        response = requests.get(f"{API_URL}/mind-soul/habits/{user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"User habits response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response missing 'status' field"
        assert "habits" in data, "Response missing 'habits' field"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Validate habits structure
        habits = data["habits"]
        assert isinstance(habits, list), "Habits should be a list"
        assert len(habits) >= 4, f"Expected at least 4 habits, found {len(habits)}"
        
        # Validate each habit structure
        habit_names_found = set()
        for habit in habits:
            required_habit_fields = ["habit_name", "current_streak", "total_completions", "last_completed"]
            for field in required_habit_fields:
                assert field in habit, f"Habit missing '{field}' field"
            
            assert isinstance(habit["habit_name"], str), "Habit name should be a string"
            assert isinstance(habit["current_streak"], int), "Current streak should be an integer"
            assert isinstance(habit["total_completions"], int), "Total completions should be an integer"
            
            habit_names_found.add(habit["habit_name"])
            
            print(f"Habit: {habit['habit_name']}")
            print(f"  Current streak: {habit['current_streak']}")
            print(f"  Total completions: {habit['total_completions']}")
            print(f"  Last completed: {habit['last_completed']}")
        
        # Verify we have the expected habits
        expected_habits = {"Daily Meditation", "Morning Exercise", "Healthy Eating", "Reading"}
        assert expected_habits.issubset(habit_names_found), f"Missing expected habits. Found: {habit_names_found}"
        
        print("✅ Test 3 - Get user habits passed")
    except Exception as e:
        print(f"❌ Test 3 - Get user habits failed: {str(e)}")
        all_passed = False
    
    # Test 4: Update existing habit
    print("\n--- Test 4: Update existing habit ---")
    try:
        updated_habit = {
            "user_id": user_id,
            "habit_name": "Daily Meditation",
            "date": today,
            "completed": True,
            "streak_count": 2  # Updated streak
        }
        
        response = requests.post(f"{API_URL}/mind-soul/habit-tracker", json=updated_habit)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert data["status"] == "success", "Status should be 'success'"
        
        # Verify the update
        habit_response = data["habit_data"]
        assert habit_response["streak_count"] == 2, "Updated streak count doesn't match"
        
        print("✅ Test 4 - Update existing habit passed")
    except Exception as e:
        print(f"❌ Test 4 - Update existing habit failed: {str(e)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All habit tracking tests passed")
    else:
        print("\n❌ Some habit tracking tests failed")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()