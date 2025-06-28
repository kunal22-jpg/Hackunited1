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
    
    # Test enhanced grocery agent
    grocery_recommendations_result, recommendations = test_grocery_recommendations()
    results["grocery_recommendations"] = grocery_recommendations_result
    results["grocery_cart_creation"] = test_grocery_cart_creation(recommendations)
    results["grocery_error_handling"] = test_grocery_error_handling()
    
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