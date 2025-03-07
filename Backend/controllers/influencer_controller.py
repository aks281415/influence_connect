from flask import Blueprint, jsonify, request
from models import User, Influencer, Campaign , AdRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from datetime import datetime
from cache import cache
# from app import export_cache as cache

# Create the Blueprint for influencer-related routes
influencer_bp = Blueprint('influencer', __name__)

# Function to check if the current user is an influencer
def is_influencer():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    #print("i am inside is influencer , user iss", user)
    # <User inf3 - Influencer>
    return user and user.role == 'Influencer'  # Check if the user is an influencer

# Function to check if the influencer's profile is complete
def is_profile_complete(influencer):
    return influencer and influencer.expertise and influencer.category and influencer.reach

# Influencer Profile Completion API
@influencer_bp.route('/profile-setup', methods=['POST'])
@jwt_required()
def complete_profile():
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    data = request.json
    category = data.get('category')
    expertise = data.get('expertise')
    reach = data.get('reach')

    # Validate that category, expertise, and reach are provided
    if not category or not expertise or not reach:
        return jsonify({'error': 'Category, expertise, and reach are required.'}), 400

    user_id = get_jwt_identity()
    #print("here is the user id",user_id)

    influencer = Influencer.query.get(user_id)    # influencer = user.influencer
    #print("here is the influencer",influencer)


    # If the influencer exists, update their profile
    if influencer:
        influencer.category = category
        influencer.expertise = expertise
        influencer.reach = reach
        db.session.commit()
        return jsonify({'message': 'Profile completed successfully!'}), 200
    else:
        return jsonify({'error': 'Influencer not found.'}), 404

@influencer_bp.route('/profile', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=10)
def get_influencer_details():
    # Fetch user details from the User table
    user_id = get_jwt_identity()  # Get the user ID from the JWT
    user = User.query.get(user_id)  # Fetch the user from the User table

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    # Check if the user is an influencer
    if user.role != 'Influencer':
        return jsonify({'error': 'Access forbidden: Only influencers can access this.'}), 403
    
    # Fetch influencer-specific details from the Influencer table
    influencer = user.influencer  # Assuming one-to-one relationship with Influencer model

    if not influencer:
        return jsonify({'error': 'Influencer profile not found.'}), 404

    # Return both user and influencer-specific data
    return jsonify({
        'username': user.username,  # From User table
        'email': user.email,        # From User table
        'category': influencer.category,  # From Influencer table
        'expertise': influencer.expertise,  # From Influencer table
        'reach': influencer.reach,  # From Influencer table
    }), 200


# Add cache invalidation when profile is updated
def invalidate_profile_cache(user_id):
    cache.delete_memoized(get_influencer_details, user_id)

@influencer_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_influencer_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.influencer:
        return jsonify({'error': 'Influencer profile not found.'}), 404
    
    data = request.json
    influencer = user.influencer

    # Update influencer's profile data
    user.username = data.get('username',user.username)
    influencer.category = data.get('category', influencer.category)
    influencer.expertise = data.get('expertise', influencer.expertise)
    influencer.reach = data.get('reach', influencer.reach)

    db.session.commit()
    invalidate_profile_cache(user_id)  # Invalidate cache

    return jsonify({'message': 'Profile updated successfully!'}), 200



@influencer_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=10)  # Cache based on query parameters
def influencer_dashboard():
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    user_id = get_jwt_identity()
    influencer = Influencer.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(influencer):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    # Fetch filter parameters from query
    category = request.args.get('category')
    min_budget = request.args.get('min_budget', type=float)
    max_budget = request.args.get('max_budget', type=float)

    # Base query for public campaigns
    query = Campaign.query.filter_by(visibility='public')

    # Apply category filter
    if category:
        query = query.filter(Campaign.category == category)

    # Apply budget filters
    if min_budget is not None:
        query = query.filter(Campaign.budget >= min_budget)
    if max_budget is not None:
        query = query.filter(Campaign.budget <= max_budget)

    # Filter out campaigns that have already been accepted by other influencers
    campaigns = query.all()
    campaign_list = []
    for campaign in campaigns:
        accepted_ad_request = AdRequest.query.filter_by(campaign_id=campaign.id, status='Accepted').first()
        if accepted_ad_request:
            continue

        # Prepare campaign details for display
        campaign_info = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'sponsor_name': campaign.sponsor.user.username,
            'category': campaign.category
        }

        # Check if the influencer has already applied for this campaign
        ad_request = AdRequest.query.filter_by(campaign_id=campaign.id, influencer_id=influencer.id).first()
        campaign_info['status'] = ad_request.status if ad_request else 'Not Applied'

        campaign_list.append(campaign_info)

    return jsonify(campaign_list), 200








# API to fetch private ad requests made to the specific influencer
@influencer_bp.route('/ad-requests', methods=['GET'])
@jwt_required()
def get_private_ad_requests():
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    user_id = get_jwt_identity()
    influencer = Influencer.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(influencer):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    # Fetch private ad requests sent to this influencer
    ad_requests = AdRequest.query.join(Campaign).filter(
        AdRequest.influencer_id == user_id,
        Campaign.visibility == 'private'  # Ensure only private campaigns are fetched
    ).all()

    ad_request_list = [{
        'id': ad_request.id,
        'campaign_id': ad_request.campaign.id,  # Include campaign ID
        'campaign_name': ad_request.campaign.name,
        'requirements': ad_request.requirements,
        'payment_amount': ad_request.payment_amount,
        'status': ad_request.status,
        'negotiated_payment_amount' : ad_request.negotiated_payment_amount,
        'influencer_name': ad_request.influencer.user.username,
        'sponsor_name': ad_request.campaign.sponsor.user.username,
        'requirements' : ad_request.requirements
    } for ad_request in ad_requests]

    return jsonify(ad_request_list), 200




# API to view the details of a specific campaign
@influencer_bp.route('/campaign/<int:campaign_id>', methods=['GET'])
@jwt_required()
def view_campaign(campaign_id):
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    campaign = Campaign.query.get(campaign_id)

    if not campaign:
        return jsonify({'error': 'Campaign not found.'}), 404

    return jsonify({
        'id': campaign.id,
        'name': campaign.name,
        'description': campaign.description,
        'start_date': campaign.start_date,
        'end_date': campaign.end_date,
        'budget': campaign.budget,
        'visibility': campaign.visibility,
        'goals': campaign.goals,
        'category': campaign.category,
        'sponsor_name': campaign.sponsor.user.username
    }), 200


# API to update ad request status (Accept or Reject)
@influencer_bp.route('/ad-request/<int:ad_request_id>/status', methods=['PUT'])
@jwt_required()
def update_ad_request_status(ad_request_id):
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    data = request.json
    new_status = data.get('status')

    if new_status not in ['Accepted', 'Rejected']:
        return jsonify({'error': 'Invalid status value. Must be "Accepted" or "Rejected".'}), 400

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad request not found.'}), 404

    ad_request.status = new_status
    db.session.commit()

    return jsonify({'message': f'Ad request status updated to {new_status}.'}), 200


# API for negotiation (adding a message to the ad request)
# Influencer - Negotiate Ad Request
@influencer_bp.route('/ad-request/<int:ad_request_id>/negotiate', methods=['PUT'])
@jwt_required()
def negotiate_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad Request not found.'}), 404

    data = request.json
    negotiated_payment = data.get('payment_amount')
    negotiation_message = data.get('message')

    # Ensure the negotiation message and payment amount are provided
    if not negotiated_payment or not negotiation_message:
        return jsonify({'error': 'Negotiation message and payment amount are required.'}), 400

    # Update the ad request with the negotiation message and new payment amount
    ad_request.is_negotiated = True
    ad_request.negotiated_payment_amount = negotiated_payment  # This line should update the negotiated amount
    ad_request.messages = (ad_request.messages or '') + f'\nInfluencer: {negotiation_message}'

    db.session.commit()

    return jsonify({'message': 'Negotiation submitted successfully!'}), 200


@influencer_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_for_campaign():
    if not is_influencer():
        return jsonify({'error': 'Access forbidden: Influencers only!'}), 403

    data = request.json
    campaign_id = data.get('campaign_id')

    # Fetch the campaign
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return jsonify({'error': 'Campaign not found.'}), 404

    # Check if the campaign is public
    if campaign.visibility != 'public':
        return jsonify({'error': 'Only public campaigns can be applied for.'}), 403

    # Check if an AdRequest exists and is accepted for this campaign
    existing_ad_request = AdRequest.query.filter_by(campaign_id=campaign.id, status='Accepted').first()
    if existing_ad_request:
        return jsonify({'error': 'This campaign has already been accepted by another influencer.'}), 403

    # Get the current influencer
    influencer_id = get_jwt_identity()
    influencer = Influencer.query.get(influencer_id)

    # Check if the current influencer already has an AdRequest for this campaign
    existing_influencer_request = AdRequest.query.filter_by(campaign_id=campaign.id, influencer_id=influencer.id).first()
    if existing_influencer_request:
        return jsonify({'error': 'You have already applied for this campaign.'}), 400

    # Create a new AdRequest for the application
    new_ad_request = AdRequest(
        campaign_id=campaign.id,
        influencer_id=influencer.id,
        payment_amount=campaign.budget,  # The initial offer is the campaign's budget
        status='Pending',  # Set status to pending until sponsor accepts/rejects
        created_at=datetime.utcnow()
    )

    db.session.add(new_ad_request)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully!'}), 201