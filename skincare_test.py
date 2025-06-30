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
        
        print("\n✅ Skincare endpoint test passed with validation")
        return True, data
    except Exception as e:
        print(f"❌ Skincare endpoint test failed: {str(e)}")
        return False, None

def test_chat_skincare_references():
    """Test if the chat endpoint properly handles skincare-related queries"""
    print("\n=== Testing Chat Endpoint for Skincare References ===")
    try:
        # Create a test user ID
        test_user_id = "skincare-test-user"
        
        # Test with a skincare-specific query
        chat_data = {
            "user_id": test_user_id,
            "message": "What's a good skincare routine for acne-prone skin?",
            "user_profile": {
                "weight": "65kg",
                "allergies": "none",
                "skin_concern": "acne"
            }
        }
        
        response = requests.post(f"{API_URL}/chat", json=chat_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "response" in data, "Response missing 'response' field"
        assert "message_id" in data, "Response missing 'message_id' field"
        
        # Check if the response contains skincare-related content
        response_text = data["response"].lower()
        print(f"Chat response excerpt: {response_text[:200]}...")
        
        skincare_keywords = ["skincare", "routine", "acne", "skin", "cleanser", "moisturizer", "treatment"]
        contains_skincare_content = any(keyword in response_text for keyword in skincare_keywords)
        
        assert contains_skincare_content, "Chat response doesn't contain skincare-related content"
        
        print("✅ Chat endpoint properly handles skincare-related queries")
        return True
    except Exception as e:
        print(f"❌ Chat endpoint test for skincare references failed: {str(e)}")
        return False

def test_personalized_wellness_skincare_recommendations():
    """Test if the personalized wellness recommendations endpoint includes skincare recommendations"""
    print("\n=== Testing Personalized Wellness Recommendations for Skincare ===")
    try:
        # Sample request data
        request_data = {
            "user_id": "skincare-test-user",
            "weight": "65 kg", 
            "allergies": "none",
            "wellness_goals": ["better skin", "clear acne"],
            "health_conditions": ["mild acne"],
            "age": 28,
            "gender": "male",
            "fitness_level": "intermediate"
        }
        
        response = requests.post(f"{API_URL}/wellness/personalized-recommendations", json=request_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "success" in data, "Response missing 'success' field"
        assert data["success"], "Request was not successful"
        assert "recommendations" in data, "Response missing 'recommendations' field"
        assert "skincare" in data["recommendations"], "Response missing 'skincare' category in recommendations"
        
        skincare_recs = data["recommendations"]["skincare"]
        assert len(skincare_recs) > 0, "No skincare recommendations found"
        
        # Print the first skincare recommendation
        print(f"Sample skincare recommendation: {json.dumps(skincare_recs[0], indent=2)}")
        
        # Check if the skincare recommendations address the user's skin concerns
        skin_concerns_addressed = False
        for rec in skincare_recs:
            description = rec["description"].lower()
            if "acne" in description or "clear skin" in description or "better skin" in description:
                skin_concerns_addressed = True
                break
        
        assert skin_concerns_addressed, "Skincare recommendations don't address the user's skin concerns"
        
        print("✅ Personalized wellness recommendations include appropriate skincare recommendations")
        return True
    except Exception as e:
        print(f"❌ Personalized wellness skincare recommendations test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all skincare-related tests"""
    results = {}
    
    # Test skincare endpoint
    skincare_result = test_skincare_endpoint()
    results["skincare_endpoint"] = skincare_result[0] if isinstance(skincare_result, tuple) else skincare_result
    
    # Test chat endpoint for skincare references
    results["chat_skincare_references"] = test_chat_skincare_references()
    
    # Test personalized wellness recommendations for skincare
    results["personalized_wellness_skincare"] = test_personalized_wellness_skincare_recommendations()
    
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