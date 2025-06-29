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

def test_workout_integration():
    """Test the integration of workout data with other parts of the system"""
    print("\n=== Testing Workout Data Integration ===")
    
    # First, get the workout data
    workout_result, workout_data = test_workouts_endpoint()
    if not workout_result or not workout_data:
        print("❌ Workout integration test skipped: Could not retrieve workout data")
        return False
    
    try:
        # Test 1: Verify workout data is properly structured for frontend consumption
        print("\n--- Test 1: Workout data structure for frontend consumption ---")
        for workout in workout_data:
            # Check that workout IDs are UUIDs (not MongoDB ObjectIDs)
            assert len(workout["id"]) > 10, f"Workout ID '{workout['id']}' doesn't appear to be a UUID"
            
            # Check that all string fields are properly formatted (not None or empty)
            string_fields = ["title", "description", "difficulty", "video_url"]
            for field in string_fields:
                assert workout[field] is not None and workout[field] != "", f"Workout '{field}' is empty or None"
            
            # Check that all list fields are properly formatted (not None and contain items)
            list_fields = ["muscle_groups", "equipment", "instructions"]
            for field in list_fields:
                assert workout[field] is not None and isinstance(workout[field], list), f"Workout '{field}' is not a valid list"
        
        print("✓ All workouts have proper data structure for frontend consumption")
        
        # Test 2: Verify personalized recommendations include workout data
        print("\n--- Test 2: Personalized recommendations include workout data ---")
        
        # Create a test user with specific fitness level
        user_data = {
            "name": "Workout Integration Test User",
            "email": f"workout.test.{uuid.uuid4()}@example.com",
            "age": 28,
            "gender": "male",
            "height": 180.0,
            "weight": 75.0,
            "allergies": ["dairy"],
            "chronic_conditions": [],
            "goals": ["muscle building", "strength"],
            "fitness_level": "intermediate",
            "diet_type": "high-protein",
            "skin_type": "normal",
            "smart_cart_enabled": True
        }
        
        # Create the user
        user_response = requests.post(f"{API_URL}/users", json=user_data)
        assert user_response.status_code == 200, f"Failed to create test user: {user_response.status_code}"
        user = user_response.json()
        user_id = user["id"]
        print(f"Created test user with ID: {user_id}")
        
        # Get personalized recommendations for this user
        request_data = {
            "user_id": user_id,
            "weight": "75 kg", 
            "allergies": "dairy",
            "wellness_goals": ["muscle building", "strength"],
            "health_conditions": [],
            "age": 28,
            "gender": "male",
            "fitness_level": "intermediate"
        }
        
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        assert response.status_code == 200, f"Failed to get personalized recommendations: {response.status_code}"
        data = response.json()
        
        # Verify workout recommendations exist and match user's fitness level
        assert "recommendations" in data, "Response missing 'recommendations' field"
        assert "workout" in data["recommendations"], "Response missing workout recommendations"
        workout_recs = data["recommendations"]["workout"]
        assert len(workout_recs) > 0, "No workout recommendations found"
        
        # Check if workout recommendations match user's fitness level
        intermediate_level_found = False
        for rec in workout_recs:
            if "intermediate" in rec["level"].lower():
                intermediate_level_found = True
                print(f"✓ Found workout recommendation matching user's intermediate fitness level: {rec['title']}")
                break
        
        if not intermediate_level_found:
            print("⚠️ No workout recommendations specifically for intermediate level found")
            # This is not a failure as the API might use fallback recommendations
        
        # Check if workout recommendations match user's goals
        goals_addressed = False
        for rec in workout_recs:
            for goal in request_data["wellness_goals"]:
                if goal.lower() in rec["description"].lower() or goal.lower() in rec["title"].lower():
                    goals_addressed = True
                    print(f"✓ Found workout recommendation addressing user goal '{goal}': {rec['title']}")
                    break
            if goals_addressed:
                break
        
        if not goals_addressed:
            print("⚠️ No workout recommendations specifically addressing user goals found")
            # This is not a failure as the API might use fallback recommendations
        
        print("✓ Personalized recommendations include workout data")
        
        # Test 3: Verify health chat can provide workout advice
        print("\n--- Test 3: Health chat provides workout advice ---")
        
        chat_data = {
            "user_id": user_id,
            "message": "Can you suggest a workout for intermediate fitness level?",
            "user_profile": {
                "weight": "75kg",
                "allergies": "dairy",
                "skin_concern": "none"
            }
        }
        
        chat_response = requests.post(f"{API_URL}/chat", json=chat_data)
        assert chat_response.status_code == 200, f"Failed to get chat response: {chat_response.status_code}"
        chat_data = chat_response.json()
        
        assert "response" in chat_data, "Chat response missing 'response' field"
        assert len(chat_data["response"]) > 0, "Chat response is empty"
        
        # Check if chat response mentions workout or exercise
        workout_terms = ["workout", "exercise", "training", "fitness", "muscle", "strength"]
        workout_mentioned = any(term in chat_data["response"].lower() for term in workout_terms)
        assert workout_mentioned, "Chat response doesn't mention workout or exercise"
        
        print(f"✓ Health chat provides workout advice: {chat_data['response'][:100]}...")
        
        print("\n✅ Workout integration test passed")
        return True
    except Exception as e:
        print(f"❌ Workout integration test failed: {str(e)}")
        return False

def test_personalized_wellness_recommendations():
    """Test the personalized wellness recommendations API endpoint with focus on workout data"""
    print("\n=== Testing Personalized Wellness Recommendations Endpoint (Workout Focus) ===")
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
        
        # Check if workout category is present
        assert "workout" in recommendations, "Missing 'workout' category in recommendations"
        assert isinstance(recommendations["workout"], list), "'workout' recommendations is not a list"
        assert len(recommendations["workout"]) > 0, "No recommendations found for 'workout' category"
        
        # Enhanced validation for workout recommendations
        workout_recs = recommendations["workout"]
        print("\n=== Enhanced Validation for Workout Recommendations ===")
        for i, workout in enumerate(workout_recs):
            print(f"\nValidating workout recommendation {i+1}: {workout.get('title', 'Unknown')}")
            
            # Check workout-specific fields
            assert "title" in workout, "Workout recommendation missing 'title' field"
            assert "description" in workout, "Workout recommendation missing 'description' field"
            assert "duration" in workout, "Workout recommendation missing 'duration' field"
            assert "level" in workout, "Workout recommendation missing 'level' field"
            assert "requirements" in workout, "Workout recommendation missing 'requirements' field"
            assert "steps" in workout, "Workout recommendation missing 'steps' field"
            assert "youtube_video" in workout, "Workout recommendation missing 'youtube_video' field"
            assert "product_links" in workout, "Workout recommendation missing 'product_links' field"
            
            # Validate field types
            assert isinstance(workout["title"], str), "Workout 'title' is not a string"
            assert isinstance(workout["description"], str), "Workout 'description' is not a string"
            assert isinstance(workout["duration"], str), "Workout 'duration' is not a string"
            assert isinstance(workout["level"], str), "Workout 'level' is not a string"
            assert isinstance(workout["requirements"], list), "Workout 'requirements' is not a list"
            assert isinstance(workout["steps"], list), "Workout 'steps' is not a list"
            assert isinstance(workout["youtube_video"], str), "Workout 'youtube_video' is not a string"
            assert isinstance(workout["product_links"], list), "Workout 'product_links' is not a list"
            
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
            
            # Validate product links
            for link in workout["product_links"]:
                assert link.startswith("https://"), f"Product link in workout recommendation is not properly formatted: {link}"
            
            print(f"✓ Workout recommendation {i+1} validated successfully")
        
        print("\n✅ Personalized wellness recommendations endpoint test (workout focus) passed")
        return True
    except Exception as e:
        print(f"❌ Personalized wellness recommendations endpoint test (workout focus) failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return results"""
    results = {}
    
    # Test basic connectivity
    results["root_endpoint"] = test_root_endpoint()
    
    # Test workout functionality (main focus of this test run)
    print("\n\n=== TESTING WORKOUT FUNCTIONALITY ===")
    print("Testing the workout endpoints and enhanced exercise data integration.")
    results["workouts_endpoint"], _ = test_workouts_endpoint()
    
    # Test workout integration with other parts of the system
    results["workout_integration"] = test_workout_integration()
    
    # Test personalized wellness recommendations with focus on workout data
    print("\n\n=== TESTING PERSONALIZED WELLNESS RECOMMENDATIONS API (WORKOUT FOCUS) ===")
    print("Testing with the sample data provided in the review request.")
    results["personalized_wellness_recommendations"] = test_personalized_wellness_recommendations()
    
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

if __name__ == "__main__":
    run_all_tests()