import requests
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
# nutracia
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

def test_skincare_endpoint():
    """Test the skincare endpoint with comprehensive validation"""
    print("\n=== Testing Skincare Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/skincare")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} skincare routines")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) >= 2, f"Expected at least 2 skincare routines, found {len(data)}"
        
        # Validate each skincare routine has the required fields and proper structure
        required_fields = [
            "id", "title", "description", "skin_type", "time_of_day", 
            "steps", "products", "video_url"
        ]
        
        for i, routine in enumerate(data):
            print(f"\nValidating skincare routine {i+1}: {routine.get('title', 'Unknown')}")
            
            # Check all required fields exist
            for field in required_fields:
                assert field in routine, f"Skincare routine missing '{field}' field"
            
            # Validate field types
            assert isinstance(routine["id"], str), "Skincare routine 'id' is not a string"
            assert isinstance(routine["title"], str), "Skincare routine 'title' is not a string"
            assert isinstance(routine["description"], str), "Skincare routine 'description' is not a string"
            assert isinstance(routine["skin_type"], str), "Skincare routine 'skin_type' is not a string"
            assert isinstance(routine["time_of_day"], str), "Skincare routine 'time_of_day' is not a string"
            assert isinstance(routine["steps"], list), "Skincare routine 'steps' is not a list"
            assert isinstance(routine["products"], list), "Skincare routine 'products' is not a list"
            assert isinstance(routine["video_url"], str), "Skincare routine 'video_url' is not a string"
            
            # Validate content
            assert len(routine["title"]) > 0, "Skincare routine title is empty"
            assert len(routine["description"]) > 0, "Skincare routine description is empty"
            assert len(routine["skin_type"]) > 0, "Skincare routine skin_type is empty"
            assert len(routine["time_of_day"]) > 0, "Skincare routine time_of_day is empty"
            assert len(routine["steps"]) > 0, "Skincare routine has no steps"
            assert len(routine["products"]) > 0, "Skincare routine has no products"
            assert routine["video_url"].startswith("http"), "Video URL is not properly formatted"
            
            print(f"✓ Skincare routine {i+1} validated successfully")
            
            # Print detailed info for the first routine
            if i == 0:
                print(f"Sample skincare routine details:")
                print(f"  Title: {routine['title']}")
                print(f"  Description: {routine['description']}")
                print(f"  Skin Type: {routine['skin_type']}")
                print(f"  Time of Day: {routine['time_of_day']}")
                print(f"  Steps: {len(routine['steps'])} steps")
                print(f"  Products: {len(routine['products'])} products")
                print(f"  Video URL: {routine['video_url']}")
        
        print("\n✅ Skincare endpoint test passed with comprehensive validation")
        return True
    except Exception as e:
        print(f"❌ Skincare endpoint test failed: {str(e)}")
        return False

def test_workouts_endpoint():
    """Test the workouts endpoint"""
    print("\n=== Testing Workouts Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/workouts")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} workouts")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) > 0, "No workouts found"
        print("✅ Workouts endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Workouts endpoint test failed: {str(e)}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    
    # Test signup endpoint
    print("\n--- Testing Signup Endpoint ---")
    try:
        # Use a unique email to avoid conflicts
        import uuid
        unique_email = f"test.user.{uuid.uuid4().hex[:8]}@example.com"
        
        signup_data = {
            "name": "Test User",
            "email": unique_email,
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            "age": 30,
            "gender": "Male",
            "height": 180,
            "heightUnit": "cm",
            "weight": 75,
            "weightUnit": "kg",
            "allergies": ["Peanuts"],
            "chronicConditions": [],
            "wellnessGoals": ["Weight Loss", "Muscle Building"],
            "fitnessLevel": "Beginner",
            "dietPreference": "Balanced",
            "skinType": "Normal",
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
            user_id = data["user_id"]
            print(f"✅ Signup endpoint test passed - Created user with ID: {user_id}")
        else:
            print(f"⚠️ Signup response indicates failure: {data['message']}")
            print("This may be expected if there are validation issues or the email is already in use")
        
        # Test login endpoint with the same credentials
        print("\n--- Testing Login Endpoint ---")
        login_data = {
            "email": unique_email,
            "password": "SecurePass123!"
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
            user_id = data["user_id"]
            print(f"✅ Login endpoint test passed - User ID: {user_id}")
            
            # Test user retrieval endpoint
            print("\n--- Testing User Retrieval Endpoint ---")
            response = requests.get(f"{API_URL}/auth/user/{user_id}")
            print(f"Status Code: {response.status_code}")
            data = response.json()
            print(f"User retrieval response: {json.dumps(data, indent=2)}")
            
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
            assert "success" in data, "Response missing 'success' field"
            assert "message" in data, "Response missing 'message' field"
            
            if data["success"]:
                assert "user" in data, "Response missing 'user' field"
                assert "user_id" in data, "Response missing 'user_id' field"
                assert data["user_id"] == user_id, "User ID in response doesn't match requested ID"
                print(f"✅ User retrieval endpoint test passed - User ID: {user_id}")
            else:
                print(f"❌ User retrieval failed with message: {data['message']}")
                return False
        else:
            print(f"❌ Login failed with message: {data['message']}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Authentication endpoints test failed: {str(e)}")
        return False

def test_personalized_recommendations_endpoint():
    """Test the personalized wellness recommendations endpoint"""
    print("\n=== Testing Personalized Wellness Recommendations Endpoint ===")
    try:
        # Sample request data
        request_data = {
            "user_id": "test-user-id",
            "weight": "75 kg", 
            "allergies": "peanuts",
            "wellness_goals": ["weight loss", "muscle building"],
            "health_conditions": ["back pain"],
            "age": 30,
            "gender": "male",
            "fitness_level": "beginner"
        }
        
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Print a summary of the response
        print(f"Response success: {data.get('success', False)}")
        print(f"Response message: {data.get('message', 'No message')}")
        
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
        
        # Print sample recommendations for each category
        for category, recs in recommendations.items():
            print(f"\nFound {len(recs)} recommendations for {category} category")
            if len(recs) > 0:
                print(f"Sample {category} recommendation title: {recs[0]['title']}")
        
        print("\n✅ Personalized wellness recommendations endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Personalized wellness recommendations endpoint test failed: {str(e)}")
        return False

def run_tests():
    """Run all tests and return results"""
    results = {}
    
    # Test basic connectivity
    results["root_endpoint"] = test_root_endpoint()
    
    # Test skincare endpoint (main focus)
    results["skincare_endpoint"] = test_skincare_endpoint()
    
    # Test other core endpoints
    results["workouts_endpoint"] = test_workouts_endpoint()
    results["auth_endpoints"] = test_auth_endpoints()
    results["personalized_recommendations"] = test_personalized_recommendations_endpoint()
    
    # Print summary
    print("\n=== Test Summary ===")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Calculate overall success
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"\nOverall Success Rate: {success_rate:.2f}% ({success_count}/{total_count} tests passed)")
    
    return results

if __name__ == "__main__":
    run_tests()
