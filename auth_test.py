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

def test_auth_signup():
    """Test user registration with complete profile data"""
    print("\n=== Testing Authentication Signup Endpoint ===")
    try:
        # Generate a unique email to avoid conflicts with existing users
        unique_id = uuid.uuid4().hex[:8]
        email = f"test.user.{unique_id}@example.com"
        
        # Complete profile data
        signup_data = {
            "name": "Test User",
            "email": email,
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!",
            "agreeTerms": True,
            "age": 28,
            "gender": "Male",
            "height": 175,
            "heightUnit": "cm",
            "weight": 70,
            "weightUnit": "kg",
            "allergies": ["Gluten", "Dairy"],
            "chronicConditions": ["Mild asthma"],
            "wellnessGoals": ["Weight management", "Muscle gain", "Better sleep"],
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
            "email": email,
            "password": password
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
            required_fields = [
                "name", "email", "age", "gender", "height", "weight", 
                "allergies", "chronic_conditions", "goals", "fitness_level", 
                "diet_type", "skin_type"
            ]
            
            for field in required_fields:
                assert field in user, f"User profile missing '{field}' field"
            
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
            required_fields = [
                "name", "email", "age", "gender", "height", "weight", 
                "allergies", "chronic_conditions", "goals", "fitness_level", 
                "diet_type", "skin_type"
            ]
            
            for field in required_fields:
                assert field in user, f"User profile missing '{field}' field"
            
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
        # Generate a unique email
        unique_id = uuid.uuid4().hex[:8]
        email = f"validation.test.{unique_id}@example.com"
        
        signup_data = {
            "name": "Validation Test User",
            "email": email,
            "password": "SecurePass123!",
            "confirmPassword": "DifferentPassword123!",  # Mismatched password
            "agreeTerms": True,
            "age": 30,
            "gender": "Female",
            "height": 165,
            "heightUnit": "cm",
            "weight": 60,
            "weightUnit": "kg",
            "allergies": ["Peanuts"],
            "chronicConditions": [],
            "wellnessGoals": ["Weight loss"],
            "fitnessLevel": "Beginner",
            "dietPreference": "Vegetarian",
            "skinType": "Dry",
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
    
    # Test 2: Missing required fields validation
    print("\n--- Test 2: Required fields validation ---")
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
    
    # Test 3: Invalid credentials for login
    print("\n--- Test 3: Invalid credentials for login ---")
    try:
        login_data = {
            "email": "nonexistent@example.com",
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
    
    if all_passed:
        print("\n✅ All authentication validation tests passed")
    else:
        print("\n❌ Some authentication validation tests failed")
    
    return all_passed

def run_auth_tests():
    """Run all authentication tests and return results"""
    results = {}
    
    # Test signup with a new user
    success, user_id, email, password = test_auth_signup()
    results["auth_signup"] = success
    
    # Test login with the created user
    if success and email and password:
        results["auth_login"], user_id = test_auth_login(email, password)
    else:
        print("❌ Skipping login test due to signup failure")
        results["auth_login"] = False
    
    # Test user profile retrieval
    if success and user_id:
        results["auth_get_user"] = test_auth_get_user(user_id)
    else:
        print("❌ Skipping user profile retrieval test due to signup/login failure")
        results["auth_get_user"] = False
    
    # Test validation scenarios
    results["auth_validation"] = test_auth_validation()
    
    # Print summary
    print("\n=== Authentication Tests Summary ===")
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
    run_auth_tests()