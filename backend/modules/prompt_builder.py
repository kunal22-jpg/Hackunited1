def build_task_prompt(user_prefs):
    """Build AI prompt for grocery recommendations"""
    brand_list = ", ".join(user_prefs["preferred_brands"])
    platforms = ", ".join(user_prefs["platforms"])
    
    return f"""
    You are a smart grocery shopping assistant.

    Based on the user's preferences:
    - Diet: {user_prefs['diet']}
    - Budget: ₹{user_prefs['budget']}
    - Preferred Brands: {brand_list}
    - Delivery: {user_prefs['delivery_speed']}
    - Query: {user_prefs['query']}

    Your task:
    - Search for recommended grocery/supplement items across {platforms}
    - Compare prices and delivery timelines
    - Choose best deal (brand + speed) under the budget
    - Focus on products that match the user's specific request
    - Provide detailed nutritional information when available
    - Generate exactly 5 specific product recommendations
    """

def build_recommendation_prompt(query, diet, budget, preferred_brands):
    """Build specific recommendation prompt for AI"""
    brands_str = ', '.join(preferred_brands)
    
    return f"""
    You are a smart grocery shopping assistant. Based on this specific request: "{query}"
    
    User preferences:
    - Diet: {diet}
    - Budget: ₹{budget}
    - Preferred Brands: {brands_str}
    
    Generate exactly 5 specific product recommendations that match the user's request.
    For each product, provide in this exact format:
    
    Product 1:
    Name: [Specific product name]
    Price: ₹[amount]
    Description: [Brief description explaining why it fits their request]
    Protein: [protein content if applicable, otherwise "N/A"]
    Rating: [rating out of 5]
    Platform: [Amazon Fresh or Flipkart Minutes]
    
    Make sure the products are relevant to their specific query: "{query}"
    Focus on products that actually exist and match their needs.
    """