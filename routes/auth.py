from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
 
# Create a Blueprint for the authentication routes
auth_bp = Blueprint('auth', __name__)
 
# Route to validate the current JWT token and return user information
@auth_bp.route('/validate', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated with a valid JWT token
def validate():
    """
    Endpoint to validate the current JWT token and retrieve user details.
    The user information is decoded from the JWT token.
    """
    # Get the identity of the current user (decoded from the JWT token)
    current_user = get_jwt_identity()#Retrieves the identity of the currently logged-in user from the token.
 
    # Return a success response with the current user's information
    return jsonify({
        "message": "success"  
    }), 200