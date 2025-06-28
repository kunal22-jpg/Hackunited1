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
    """Test the workouts endpoint"""
    print("\n=== Testing Workouts Endpoint ===")
    try:
        response = requests.get(f"{API_URL}/workouts")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} workouts")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        if len(data) > 0:
            print(f"Sample workout: {json.dumps(data[0], indent=2)}")
            # Validate workout structure
            assert "id" in data[0], "Workout missing 'id' field"
            assert "title" in data[0], "Workout missing 'title' field"
            assert "description" in data[0], "Workout missing 'description' field"
        print("✅ Workouts endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Workouts endpoint test failed: {str(e)}")
        return False

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

def test_chat_functionality(user_id):
    """Test the AI chat endpoint"""
    print("\n=== Testing Chat Functionality ===")
    if not user_id:
        print("❌ Chat functionality test skipped: No user ID available")
        return False
    
    try:
        chat_data = {
            "user_id": user_id,
            "message": "Can you recommend a workout for improving core strength?"
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Chat response: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "response" in data, "Response missing 'response' field"
        assert "message_id" in data, "Response missing 'message_id' field"
        
        print("✅ Chat functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Chat functionality test failed: {str(e)}")
        return False

def test_grocery_recommendations():
    """Test the grocery recommendations endpoint"""
    print("\n=== Testing Grocery Recommendations Endpoint ===")
    try:
        query_data = {
            "diet_type": "high-protein",
            "allergies": ["peanuts"],
            "goals": ["muscle building"]
        }
        
        response = requests.post(f"{API_URL}/grocery/recommendations", json=query_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Grocery recommendations: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "recommendations" in data, "Response missing 'recommendations' field"
        assert isinstance(data["recommendations"], list), "'recommendations' is not a list"
        
        print("✅ Grocery recommendations endpoint test passed")
        return True, data["recommendations"]
    except Exception as e:
        print(f"❌ Grocery recommendations endpoint test failed: {str(e)}")
        return False, None

def test_grocery_cart_creation(recommendations):
    """Test the grocery cart creation endpoint"""
    print("\n=== Testing Grocery Cart Creation Endpoint ===")
    if not recommendations:
        print("❌ Grocery cart creation test skipped: No recommendations available")
        return False
    
    try:
        # Select all recommendations for the cart
        for item in recommendations:
            item["selected"] = True
        
        response = requests.post(f"{API_URL}/grocery/create-cart", json=recommendations)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Created cart: {json.dumps(data, indent=2)}")
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "cart_items" in data, "Response missing 'cart_items' field"
        assert "total_cost" in data, "Response missing 'total_cost' field"
        assert "status" in data, "Response missing 'status' field"
        
        print("✅ Grocery cart creation endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Grocery cart creation endpoint test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return results"""
    results = {}
    
    # Test basic connectivity
    results["root_endpoint"] = test_root_endpoint()
    
    # Test data fetching endpoints
    results["workouts_endpoint"] = test_workouts_endpoint()
    results["skincare_endpoint"] = test_skincare_endpoint()
    results["meals_endpoint"] = test_meals_endpoint()
    results["health_conditions_endpoint"] = test_health_conditions_endpoint()
    
    # Test user management
    user_creation_result, user_id = test_user_creation()
    results["user_creation"] = user_creation_result
    
    # Test chat functionality
    results["chat_functionality"] = test_chat_functionality(user_id)
    
    # Test grocery agent
    grocery_recommendations_result, recommendations = test_grocery_recommendations()
    results["grocery_recommendations"] = grocery_recommendations_result
    results["grocery_cart_creation"] = test_grocery_cart_creation(recommendations)
    
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
    run_all_tests()