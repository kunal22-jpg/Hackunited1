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

def test_grocery_recommendations_with_sample_data():
    """Test the grocery recommendations API with the sample data from the review request"""
    print("\n=== Testing Grocery Recommendations API with Sample Data ===")
    
    # Sample data from the review request
    sample_data = {
        "query": "protein powder for muscle building",
        "budget": 1000,
        "preferred_brands": ["MuscleBlaze", "Optimum Nutrition"],
        "diet": "high protein"
    }
    
    print(f"Sending request with sample data: {json.dumps(sample_data, indent=2)}")
    response = requests.post(f"{API_URL}/grocery/recommendations", json=sample_data)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    # Basic validation
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "recommendations" in data, "Response missing 'recommendations' field"
    assert isinstance(data["recommendations"], list), "'recommendations' is not a list"
    assert len(data["recommendations"]) > 0, "No recommendations returned"
    
    # Check for AI response (may be missing if using fallback)
    if "ai_response" in data and data["ai_response"]:
        print(f"\nAI Response: {data['ai_response'][:200]}...")  # Print first 200 chars of AI response
    else:
        print("\nNote: AI response is missing - API is likely using fallback recommendations")
        print(f"Response status: {data.get('status', 'unknown')}")
    
    # Validate user preferences
    assert "user_preferences" in data, "Response missing 'user_preferences' field"
    assert data["user_preferences"]["query"] == sample_data["query"], "Query in preferences doesn't match request"
    
    # Print all recommendations for inspection
    print(f"\nFound {len(data['recommendations'])} recommendations:")
    for i, rec in enumerate(data["recommendations"]):
        print(f"\nRecommendation {i+1}:")
        print(f"  Name: {rec.get('name', 'N/A')}")
        print(f"  Price: {rec.get('price', 'N/A')}")
        print(f"  Description: {rec.get('description', 'N/A')[:50]}...")  # Truncate long descriptions
        print(f"  Protein: {rec.get('protein', 'N/A')}")
        print(f"  Rating: {rec.get('rating', 'N/A')}")
        print(f"  Platform: {rec.get('platform', 'N/A')}")
    
    # Check if recommendations are personalized (not the same fallback response)
    # Store the first response for comparison
    first_response = data
    
    # Make a second request with different query to check for personalization
    print("\n=== Testing with Different Query to Verify Personalization ===")
    different_data = {
        "query": "vegan protein powder for weight loss",
        "budget": 1000,
        "preferred_brands": ["MuscleBlaze", "Optimum Nutrition"],
        "diet": "high protein"
    }
    
    print(f"Sending request with different data: {json.dumps(different_data, indent=2)}")
    response2 = requests.post(f"{API_URL}/grocery/recommendations", json=different_data)
    print(f"Status Code: {response2.status_code}")
    data2 = response2.json()
    
    # Basic validation for second response
    assert response2.status_code == 200, f"Expected status code 200, got {response2.status_code}"
    assert "recommendations" in data2, "Response missing 'recommendations' field"
    assert isinstance(data2["recommendations"], list), "'recommendations' is not a list"
    assert len(data2["recommendations"]) > 0, "No recommendations returned"
    
    # Print all recommendations from second request for inspection
    print(f"\nFound {len(data2['recommendations'])} recommendations for different query:")
    for i, rec in enumerate(data2["recommendations"]):
        print(f"\nRecommendation {i+1}:")
        print(f"  Name: {rec.get('name', 'N/A')}")
        print(f"  Price: {rec.get('price', 'N/A')}")
        print(f"  Description: {rec.get('description', 'N/A')[:50]}...")  # Truncate long descriptions
        print(f"  Protein: {rec.get('protein', 'N/A')}")
        print(f"  Rating: {rec.get('rating', 'N/A')}")
        print(f"  Platform: {rec.get('platform', 'N/A')}")
    
    # Check if the responses are different (indicating personalization)
    is_personalized = False
    
    # Compare first recommendation from each response
    if (len(first_response["recommendations"]) > 0 and 
        len(data2["recommendations"]) > 0):
        rec1 = first_response["recommendations"][0]
        rec2 = data2["recommendations"][0]
        
        # Check if names or descriptions are different
        if (rec1.get("name") != rec2.get("name") or 
            rec1.get("description") != rec2.get("description")):
            is_personalized = True
            print("\n✅ Responses are different for different queries - API is personalized")
        else:
            print("\n❌ Responses are identical for different queries - API may not be personalized")
    
    # Check if AI responses are different
    if first_response.get("ai_response") != data2.get("ai_response"):
        is_personalized = True
        print("✅ AI responses are different for different queries - AI integration is working")
    else:
        print("❌ AI responses are identical for different queries - AI integration may not be working properly")
    
    # Make a third request with completely different query to further verify personalization
    print("\n=== Testing with Completely Different Query ===")
    third_data = {
        "query": "organic fruits and vegetables",
        "budget": 500,
        "preferred_brands": ["Organic India", "24 Mantra"],
        "diet": "vegetarian"
    }
    
    print(f"Sending request with third data: {json.dumps(third_data, indent=2)}")
    response3 = requests.post(f"{API_URL}/grocery/recommendations", json=third_data)
    print(f"Status Code: {response3.status_code}")
    data3 = response3.json()
    
    # Basic validation for third response
    assert response3.status_code == 200, f"Expected status code 200, got {response3.status_code}"
    assert "recommendations" in data3, "Response missing 'recommendations' field"
    assert isinstance(data3["recommendations"], list), "'recommendations' is not a list"
    assert len(data3["recommendations"]) > 0, "No recommendations returned"
    
    # Print all recommendations from third request for inspection
    print(f"\nFound {len(data3['recommendations'])} recommendations for third query:")
    for i, rec in enumerate(data3["recommendations"]):
        print(f"\nRecommendation {i+1}:")
        print(f"  Name: {rec.get('name', 'N/A')}")
        print(f"  Price: {rec.get('price', 'N/A')}")
        print(f"  Description: {rec.get('description', 'N/A')[:50]}...")  # Truncate long descriptions
        print(f"  Protein: {rec.get('protein', 'N/A')}")
        print(f"  Rating: {rec.get('rating', 'N/A')}")
        print(f"  Platform: {rec.get('platform', 'N/A')}")
    
    # Check if the third response is different from the first two
    if (len(data3["recommendations"]) > 0):
        rec3 = data3["recommendations"][0]
        rec1 = first_response["recommendations"][0] if len(first_response["recommendations"]) > 0 else None
        
        if rec1 and rec3.get("name") != rec1.get("name"):
            is_personalized = True
            print("\n✅ Third response is different from first response - API is personalized")
        else:
            print("\n❌ Third response is similar to first response - API may not be personalized")
    
    # Check if AI text is meaningful (not generic)
    ai_text_meaningful = False
    
    # Check if AI response contains specific terms from the query
    for query_term in sample_data["query"].split():
        if len(query_term) > 3 and query_term.lower() in data["ai_response"].lower():
            ai_text_meaningful = True
            print(f"\n✅ AI response contains query term '{query_term}' - AI text is meaningful")
            break
    
    # Check if AI response mentions preferred brands
    for brand in sample_data["preferred_brands"]:
        if brand.lower() in data["ai_response"].lower():
            ai_text_meaningful = True
            print(f"✅ AI response mentions preferred brand '{brand}' - AI text is meaningful")
            break
    
    # Check if AI response mentions diet preference
    if sample_data["diet"].lower() in data["ai_response"].lower():
        ai_text_meaningful = True
        print(f"✅ AI response mentions diet preference '{sample_data['diet']}' - AI text is meaningful")
    
    if not ai_text_meaningful:
        print("❌ AI response doesn't contain specific terms from the query - AI text may be generic")
    
    # Overall test result
    if is_personalized and ai_text_meaningful:
        print("\n✅ Grocery recommendations API is working properly with personalized responses")
        return True
    else:
        print("\n❌ Grocery recommendations API may not be providing fully personalized responses")
        return False

if __name__ == "__main__":
    test_grocery_recommendations_with_sample_data()