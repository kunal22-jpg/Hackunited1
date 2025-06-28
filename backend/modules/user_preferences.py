def get_user_preferences(query=None, budget=500, preferred_brands=None, diet="high protein"):
    """Extract and structure user preferences from query and parameters"""
    if preferred_brands is None:
        preferred_brands = ["MuscleBlaze", "Organic India"]
    
    return {
        "diet": diet,
        "budget": budget,
        "preferred_brands": preferred_brands,
        "delivery_speed": "fastest",
        "platforms": ["Amazon Fresh", "Flipkart Minutes"],
        "query": query
    }