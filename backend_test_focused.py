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
    """Test the skincare endpoint with enhanced validation for skincare data"""
    print("\n=== Testing Skincare Endpoint with Enhanced Validation ===")
    try:
        response = requests.get(f"{API_URL}/skincare")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} skincare routines")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) > 0, f"Expected at least 1 skincare routine, found {len(data)}"
        
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
        
        print("\n✅ Skincare endpoint test passed with enhanced validation")
        return True, data
    except Exception as e:
        print(f"❌ Skincare endpoint test failed: {str(e)}")
        return False, None

def test_meals_endpoint():
    """Test the meals endpoint with enhanced validation"""
    print("\n=== Testing Meals Endpoint with Enhanced Validation ===")
    try:
        response = requests.get(f"{API_URL}/meals")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} meal plans")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) > 0, f"Expected at least 1 meal plan, found {len(data)}"
        
        # Validate each meal plan has the required fields and proper structure
        required_fields = [
            "id", "title", "description", "diet_type", "calories", 
            "macros", "ingredients", "instructions", "prep_time"
        ]
        
        for i, meal in enumerate(data):
            print(f"\nValidating meal plan {i+1}: {meal.get('title', 'Unknown')}")
            
            # Check all required fields exist
            for field in required_fields:
                assert field in meal, f"Meal plan missing '{field}' field"
            
            # Validate field types
            assert isinstance(meal["id"], str), "Meal plan 'id' is not a string"
            assert isinstance(meal["title"], str), "Meal plan 'title' is not a string"
            assert isinstance(meal["description"], str), "Meal plan 'description' is not a string"
            assert isinstance(meal["diet_type"], str), "Meal plan 'diet_type' is not a string"
            assert isinstance(meal["calories"], int), "Meal plan 'calories' is not an integer"
            assert isinstance(meal["macros"], dict), "Meal plan 'macros' is not a dictionary"
            assert isinstance(meal["ingredients"], list), "Meal plan 'ingredients' is not a list"
            assert isinstance(meal["instructions"], list), "Meal plan 'instructions' is not a list"
            assert isinstance(meal["prep_time"], int), "Meal plan 'prep_time' is not an integer"
            
            # Validate content
            assert len(meal["title"]) > 0, "Meal plan title is empty"
            assert len(meal["description"]) > 0, "Meal plan description is empty"
            assert len(meal["diet_type"]) > 0, "Meal plan diet_type is empty"
            assert meal["calories"] > 0, "Meal plan calories must be positive"
            assert len(meal["macros"]) > 0, "Meal plan has no macros"
            assert len(meal["ingredients"]) > 0, "Meal plan has no ingredients"
            assert len(meal["instructions"]) > 0, "Meal plan has no instructions"
            assert meal["prep_time"] > 0, "Meal plan prep_time must be positive"
            
            print(f"✓ Meal plan {i+1} validated successfully")
            
            # Print detailed info for the first meal plan
            if i == 0:
                print(f"Sample meal plan details:")
                print(f"  Title: {meal['title']}")
                print(f"  Description: {meal['description']}")
                print(f"  Diet Type: {meal['diet_type']}")
                print(f"  Calories: {meal['calories']}")
                print(f"  Macros: {meal['macros']}")
                print(f"  Ingredients: {len(meal['ingredients'])} ingredients")
                print(f"  Instructions: {len(meal['instructions'])} steps")
                print(f"  Prep Time: {meal['prep_time']} minutes")
        
        print("\n✅ Meals endpoint test passed with enhanced validation")
        return True, data
    except Exception as e:
        print(f"❌ Meals endpoint test failed: {str(e)}")
        return False, None

def test_health_conditions_endpoint():
    """Test the health conditions endpoint with enhanced validation"""
    print("\n=== Testing Health Conditions Endpoint with Enhanced Validation ===")
    try:
        response = requests.get(f"{API_URL}/health-conditions")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} health condition plans")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert isinstance(data, list), "Response is not a list"
        assert len(data) > 0, f"Expected at least 1 health condition plan, found {len(data)}"
        
        # Validate each health condition plan has the required fields and proper structure
        required_fields = [
            "id", "condition", "title", "description", 
            "daily_routine", "lifestyle_tips", "video_url"
        ]
        
        for i, plan in enumerate(data):
            print(f"\nValidating health condition plan {i+1}: {plan.get('title', 'Unknown')}")
            
            # Check all required fields exist
            for field in required_fields:
                assert field in plan, f"Health condition plan missing '{field}' field"
            
            # Validate field types
            assert isinstance(plan["id"], str), "Health condition plan 'id' is not a string"
            assert isinstance(plan["condition"], str), "Health condition plan 'condition' is not a string"
            assert isinstance(plan["title"], str), "Health condition plan 'title' is not a string"
            assert isinstance(plan["description"], str), "Health condition plan 'description' is not a string"
            assert isinstance(plan["daily_routine"], list), "Health condition plan 'daily_routine' is not a list"
            assert isinstance(plan["lifestyle_tips"], list), "Health condition plan 'lifestyle_tips' is not a list"
            assert isinstance(plan["video_url"], str), "Health condition plan 'video_url' is not a string"
            
            # Validate content
            assert len(plan["condition"]) > 0, "Health condition plan condition is empty"
            assert len(plan["title"]) > 0, "Health condition plan title is empty"
            assert len(plan["description"]) > 0, "Health condition plan description is empty"
            assert len(plan["daily_routine"]) > 0, "Health condition plan has no daily routine"
            assert len(plan["lifestyle_tips"]) > 0, "Health condition plan has no lifestyle tips"
            assert plan["video_url"].startswith("http"), "Video URL is not properly formatted"
            
            print(f"✓ Health condition plan {i+1} validated successfully")
            
            # Print detailed info for the first health condition plan
            if i == 0:
                print(f"Sample health condition plan details:")
                print(f"  Condition: {plan['condition']}")
                print(f"  Title: {plan['title']}")
                print(f"  Description: {plan['description']}")
                print(f"  Daily Routine: {len(plan['daily_routine'])} steps")
                print(f"  Lifestyle Tips: {len(plan['lifestyle_tips'])} tips")
                print(f"  Video URL: {plan['video_url']}")
        
        print("\n✅ Health conditions endpoint test passed with enhanced validation")
        return True, data
    except Exception as e:
        print(f"❌ Health conditions endpoint test failed: {str(e)}")
        return False, None

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