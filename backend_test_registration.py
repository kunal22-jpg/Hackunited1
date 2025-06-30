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
    """Test user registration with complete profile data"""
    print("\n=== Testing Authentication Signup Endpoint ===")
    try:
        # Generate a unique email to avoid conflicts with existing users
        unique_id = uuid.uuid4().hex[:8]
        
        # Complete profile data as specified in the requirements
        signup_data = {
            "name": "Michael Johnson",
            "email": f"michael.johnson.{unique_id}@example.com",
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            "age": 32,
            "gender": "Male",
            "height": 180,
            "heightUnit": "cm",
            "weight": 78,
            "weightUnit": "kg",
            "allergies": ["Peanuts", "Dairy"],
            "chronicConditions": ["Mild asthma"],
            "wellnessGoals": ["Weight management", "Muscle building", "Stress reduction"],
            "fitnessLevel": "Intermediate",
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
            "email": email or "michael.johnson@example.com",
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
            
            # Verify all profile fields are returned
            user = data["user"]
            assert "name" in user, "User profile missing 'name' field"
            assert "email" in user, "User profile missing 'email' field"
            assert "age" in user, "User profile missing 'age' field"
            assert "gender" in user, "User profile missing 'gender' field"
            assert "height" in user, "User profile missing 'height' field"
            assert "weight" in user, "User profile missing 'weight' field"
            assert "allergies" in user, "User profile missing 'allergies' field"
            assert "chronic_conditions" in user, "User profile missing 'chronic_conditions' field"
            assert "goals" in user, "User profile missing 'goals' field"
            assert "fitness_level" in user, "User profile missing 'fitness_level' field"
            assert "diet_type" in user, "User profile missing 'diet_type' field"
            assert "skin_type" in user, "User profile missing 'skin_type' field"
            
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
            
            # Verify all profile fields are returned
            user = data["user"]
            assert "name" in user, "User profile missing 'name' field"
            assert "email" in user, "User profile missing 'email' field"
            assert "age" in user, "User profile missing 'age' field"
            assert "gender" in user, "User profile missing 'gender' field"
            assert "height" in user, "User profile missing 'height' field"
            assert "weight" in user, "User profile missing 'weight' field"
            assert "allergies" in user, "User profile missing 'allergies' field"
            assert "chronic_conditions" in user, "User profile missing 'chronic_conditions' field"
            assert "goals" in user, "User profile missing 'goals' field"
            assert "fitness_level" in user, "User profile missing 'fitness_level' field"
            assert "diet_type" in user, "User profile missing 'diet_type' field"
            assert "skin_type" in user, "User profile missing 'skin_type' field"
            
            print(f"✅ Authentication get user test passed - User ID: {user_id}")
            return True
        else:
            print(f"❌ Get user failed with message: {data['message']}")
            return False
    except Exception as e:
        print(f"❌ Authentication get user test failed: {str(e)}")
        return False

def verify_mongodb_connection():
    """Verify that the backend can connect to MongoDB"""
    print("\n=== Verifying MongoDB Connection ===")
    
    # We'll test this indirectly by checking if the signup and login endpoints work
    # If they work, it means the MongoDB connection is functioning properly
    
    # First, test the signup endpoint
    signup_success, user_id, email, password = test_auth_signup()
    if not signup_success:
        print("❌ MongoDB connection verification failed: Signup test failed")
        return False
    
    # Then, test the login endpoint with the created user
    login_success, _ = test_auth_login(email, password)
    if not login_success:
        print("❌ MongoDB connection verification failed: Login test failed")
        return False
    
    # Finally, test retrieving the user profile
    get_user_success = test_auth_get_user(user_id)
    if not get_user_success:
        print("❌ MongoDB connection verification failed: Get user test failed")
        return False
    
    print("✅ MongoDB connection verification passed: All authentication endpoints are working")
    return True

def run_tests():
    """Run all tests and return results"""
    results = {}
    
    # Test basic connectivity
    results["root_endpoint"] = test_root_endpoint()
    
    # Test authentication endpoints
    success, user_id, email, password = test_auth_signup()
    results["auth_signup"] = success
    
    if success and user_id:
        results["auth_login"], user_id = test_auth_login(email, password)
        results["auth_get_user"] = test_auth_get_user(user_id)
    else:
        print("❌ Skipping authentication-dependent tests due to signup failure")
        results["auth_login"] = False
        results["auth_get_user"] = False
    
    # Verify MongoDB connection
    results["mongodb_connection"] = verify_mongodb_connection()
    
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