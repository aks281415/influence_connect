from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User  # Import User model and database
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from db import db
from models import Sponsor, Influencer

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Define the Signup Form using Flask-WTF
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Allowed roles for the platform
ALLOWED_ROLES = {'Admin', 'Sponsor', 'Influencer'}

# Signup Route (POST)
@auth_bp.route('/signup', methods=['POST'])
def signup():
    form = SignupForm()

    # Handle both JSON and Form Data
    data = request.get_json() if request.is_json else request.form

    # Validate the role (must be one of the allowed roles)
    role = data.get('role')
    if not role or role not in ALLOWED_ROLES:
        return jsonify({'error': f'Invalid or missing role. Allowed roles are: {", ".join(ALLOWED_ROLES)}'}), 400
    
    if role == 'Admin':
        existing_admin = User.query.filter_by(role='Admin').first()
        if existing_admin:
            return jsonify({'error': 'An Admin already exists. Only one Admin is allowed.'}), 403

    # Check if user with the same email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User already exists!'}), 409

    # Validate form data (if you're submitting via a form)
    if not form.validate_on_submit():
        return jsonify({'error': 'Invalid form data'}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create a new user with the specified role
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    
    if role == 'Sponsor':
        new_sponsor = Sponsor(id=new_user.id)
        db.session.add(new_sponsor)
        db.session.commit()

    if role == 'Influencer':
        new_influencer = Influencer(id=new_user.id)
        db.session.add(new_influencer)
        db.session.commit()

    return jsonify({'message': 'User created successfully!'}), 201

# Login Route (POST)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    requested_role = data.get('role')
    if requested_role != user.role:
        return jsonify({'error': f"Wrong role. You are registered with {user.role}."}), 403

    # Check if the password is correct
    if not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check if the user is a Sponsor and if they are approved
    if user.role == 'Sponsor' and user.flagged != 'Active':
        return jsonify({'error': 'Your account is pending approval by the admin.'}), 403
    
        # Check if the user is a Sponsor and if they are approved
    if user.role == 'Influencer' and user.flagged != 'Active':
        return jsonify({'error': 'Your account is pending approval by the admin.'}), 403

    # Check if the user is an Influencer and if their profile is complete
    profile_incomplete = False
    if user.role == 'Influencer':
        influencer = user.influencer
        if influencer and (not influencer.category or not influencer.expertise or not influencer.reach):
            profile_incomplete = True  # Set flag for incomplete profile

    # Create a JWT token, including the user's ID and role in the payload
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})

    # Return the token and profile completeness status
    return jsonify({
        'access_token': access_token,
        'message': f'Welcome {user.username}!',
        'profile_incomplete': profile_incomplete  # This can be checked in the frontend
    }), 200



