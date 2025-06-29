import requests
import json
import os
import sys
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

def test_workouts_endpoint():
    """Test the workouts endpoint with enhanced validation for exercise data"""
    print("\n=== Testing Workouts Endpoint ===")
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

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    try:
        # Test login endpoint with sample credentials
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post(f"{API_URL}/auth/login", json=login_data)
        print(f"Login Status Code: {response.status_code}")
        
        # We don't expect a successful login with these credentials,
        # but the endpoint should respond with a proper structure
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        assert "success" in data, "Response missing 'success' field"
        assert "message" in data, "Response missing 'message' field"
        
        print("✅ Authentication endpoints test passed")
        return True
    except Exception as e:
        print(f"❌ Authentication endpoints test failed: {str(e)}")
        return False

def test_wellness_recommendations_endpoint():
    """Test the personalized wellness recommendations endpoint"""
    print("\n=== Testing Personalized Wellness Recommendations Endpoint ===")
    try:
        # Sample request data
        request_data = {
            "user_id": "test-user",
            "weight": "70 kg", 
            "allergies": "none",
            "wellness_goals": ["general fitness"],
            "health_conditions": [],
            "age": 30,
            "gender": "male",
            "fitness_level": "intermediate"
        }
        
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        print(f"Status Code: {response.status_code}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        assert "success" in data, "Response missing 'success' field"
        assert "recommendations" in data, "Response missing 'recommendations' field"
        
        # Check if all 4 required categories are present
        recommendations = data["recommendations"]
        required_categories = ["workout", "diet", "skincare", "health"]
        for category in required_categories:
            assert category in recommendations, f"Missing '{category}' category in recommendations"
        
        print("✅ Wellness recommendations endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Wellness recommendations endpoint test failed: {str(e)}")
        return False

def test_backend_after_frontend_changes():
    """Test backend functionality after removing AI personalized workout feature from frontend"""
    print("\n=== TESTING BACKEND FUNCTIONALITY AFTER FRONTEND CHANGES ===")
    print("This test verifies that removing the AI personalized workout feature from the frontend")
    print("doesn't break any backend functionality.")
    
    results = {}
    
    # Test basic connectivity
    print("\n--- Testing Basic Connectivity ---")
    results["root_endpoint"] = test_root_endpoint()
    
    # Test workout endpoint (main focus)
    print("\n--- Testing Workout Endpoint ---")
    results["workouts_endpoint"] = test_workouts_endpoint()
    
    # Test other core endpoints
    print("\n--- Testing Other Core Endpoints ---")
    results["skincare_endpoint"] = test_skincare_endpoint()
    results["meals_endpoint"] = test_meals_endpoint()
    results["health_conditions_endpoint"] = test_health_conditions_endpoint()
    results["auth_endpoints"] = test_auth_endpoints()
    results["wellness_recommendations"] = test_wellness_recommendations_endpoint()
    
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
    
    if success_rate == 100:
        print("\n✅ BACKEND FUNCTIONALITY VERIFIED: All backend endpoints are working correctly after frontend changes.")
        print("The removal of the AI personalized workout feature from the frontend has not affected backend functionality.")
    else:
        print("\n❌ BACKEND ISSUES DETECTED: Some backend endpoints are not working correctly.")
        print("The frontend changes may have affected backend functionality.")
    
    return results

if __name__ == "__main__":
    test_backend_after_frontend_changes()