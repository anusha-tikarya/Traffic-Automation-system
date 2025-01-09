from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask import request, jsonify
from flask_jwt_extended import create_access_token
import datetime
from db import get_db_connection
import os
from routes.auth import auth_bp
from routes.vehicles import vehicles_bp
from routes.signals import signals_bp
from routes.violations import violations_bp
from routes.sensors import sensors_bp
from routes.fines import fines_bp
 
# Load environment variables from .env file
load_dotenv()
 
# Initialize Flask app
app = Flask(__name__)
 
# Configure JWT Secret Key from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
 
# Initialize JWTManager to handle token creation and validation
jwt = JWTManager(app)
 
# Route for user sign-in (authentication)
@app.route('/signin', methods=['POST'])
def signin():
    """Sign-in endpoint to authenticate users and generate JWT token."""
    # Get the JSON data from the request
    data = request.json
    email_id = data.get('email_id')
    password = data.get('password')
 
    # Validate if email_id and password are provided
    if not email_id or not password:
        return jsonify({'message': 'Email_id and password are required'}), 400
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Query to check if the provided email and password match an existing user
        query = "SELECT * FROM users WHERE email_id = %s AND pass = %s;"
        cursor.execute(query, (email_id, password))
        user = cursor.fetchone()
 
        # If user exists, create a JWT token
        if user:
            expiration = datetime.timedelta(hours=1)  # Token expiration time (1 hour)
            token = create_access_token(identity=user['email_id'], expires_delta=expiration)
            return jsonify({
                "message": "success",
                "credentials": {
                    "id": user['user_id'],
                    "email": user['email_id'],
                    "token": token
                }
            }), 200
        else:
            # If credentials are incorrect, return unauthorized error
            return jsonify({'status': 401, 'message': 'failed', 'Error': 'Access Denied'}), 401
 
    except Exception as err:
        # Return database error in case of failure
        return jsonify({'message': 'Database error', 'error': str(err)}), 500
    finally:
        # Ensure the database connection is properly closed
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
 
# Register blueprints for modular route management
# Register blueprints : This method integrates a blueprint into the main Flask application (app).
app.register_blueprint(auth_bp, url_prefix='/auth')  # Authentication routes
app.register_blueprint(vehicles_bp, url_prefix='/vehicles')  # Vehicle routes
app.register_blueprint(signals_bp, url_prefix='/signals')  # Signal routes
app.register_blueprint(violations_bp, url_prefix='/violations')  # Violation routes
app.register_blueprint(sensors_bp, url_prefix='/sensors')  # Sensor routes
app.register_blueprint(fines_bp, url_prefix='/fines')  # Fine routes
 
# Run the Flask app on port 2999 for development
if __name__ == '__main__':
    app.run(debug=True, port=2999)
 