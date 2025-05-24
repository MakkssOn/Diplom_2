expected_responses = {
    "create_user": {
        "existing_user_status": {"message": "User already exists", "success": False},
        "missing_field_status": {"message": "Email, password and name are required fields", "success": False},
    },

    "login_user": {
        "incorrect_credentials_status": {"message": "email or password are incorrect", "success": False},
        "unauthorized_status": {"message": "You should be authorised", "success": False},
    },

     "create_order": {
        "no_ingredients_status": {"message": "Ingredient ids must be provided", "success": False},
        "invalid_ingredient_hash_status": {"message": "Internal Server Error", "success": False},
    }
}