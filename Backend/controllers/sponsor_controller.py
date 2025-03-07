from flask import Blueprint, jsonify, request
from models import User, Sponsor, Campaign , AdRequest , Influencer
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from datetime import datetime
from cache import cache
import csv
from io import StringIO
from flask import make_response
# from app import export_cache as cache


# Create the Blueprint for sponsor-related routes
sponsor_bp = Blueprint('sponsor', __name__)

# Function to check if the current user is a sponsor
def is_sponsor():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id) 
    return user and user.role == 'Sponsor'  # Check if the user is a sponsor

# Function to check if the sponsor's profile is complete
def is_profile_complete(sponsor):
    return sponsor and sponsor.industry and sponsor.sponsor_type

# Sponsor Profile Completion API
@sponsor_bp.route('/complete-profile', methods=['POST'])
@jwt_required()
def complete_profile():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    data = request.json
    industry = data.get('industry')
    sponsor_type = data.get('sponsor_type')

    # Validate that industry and sponsor_type are provided
    if not industry or not sponsor_type:
        return jsonify({'error': 'Industry and sponsor type are required.'}), 400

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # If the sponsor exists, update their profile
    if sponsor:
        sponsor.sponsor_type = sponsor_type
        sponsor.industry = industry
        db.session.commit()
        return jsonify({'message': 'Profile completed successfully!'}), 200
    else:
        return jsonify({'error': 'Sponsor not found.'}), 404

# Sponsor Dashboard - View Campaigns
@sponsor_bp.route('/campaigns', methods=['GET'])
@jwt_required()
@cache.cached(timeout=10, key_prefix='sponsor_campaigns')
def view_campaigns():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(sponsor):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403
    

    # If the sponsor exists, return their campaigns
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id,flagged='Active').all()
    campaign_list = [{
        'id': campaign.id,
        'name': campaign.name,
        'description': campaign.description,
        'start_date': campaign.start_date,
        'end_date': campaign.end_date,
        'budget': campaign.budget,
        'visibility': campaign.visibility,
        'goals': campaign.goals,
        'flagged': campaign.flagged,
        'category': campaign.category
    } for campaign in campaigns]

    return jsonify(campaign_list), 200

# Sponsor - Add a Campaign
@sponsor_bp.route('/campaigns', methods=['POST'])
@jwt_required()
def add_campaign():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(sponsor):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    data = request.json
    name = data.get('name')
    description = data.get('description')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    budget = data.get('budget')
    visibility = data.get('visibility')
    goals = data.get('goals')
    category = data.get('category')

    # Validate the required fields
    if not name or not budget or not visibility:
        return jsonify({'error': 'Name, budget, and visibility are required.'}), 400

    # If the sponsor exists, create a new campaign
    new_campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals,
        sponsor_id=sponsor.id,
        category= category
    )
    db.session.add(new_campaign)
    db.session.commit()
    invalidate_campaign_cache()  # Invalidate cache
    return jsonify({'message': 'Campaign added successfully!'}), 201

# Sponsor - Update a Campaign
@sponsor_bp.route('/campaigns/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(sponsor):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    # If the sponsor exists, allow them to update their campaign
    campaign = Campaign.query.get(campaign_id)

    # Ensure the campaign belongs to the sponsor
    if campaign and campaign.sponsor_id == sponsor.id:
        data = request.json
        campaign.name = data.get('name', campaign.name)
        campaign.description = data.get('description', campaign.description)
        campaign.start_date = data.get('start_date', campaign.start_date)
        campaign.end_date = data.get('end_date', campaign.end_date)
        campaign.budget = data.get('budget', campaign.budget)
        campaign.visibility = data.get('visibility', campaign.visibility)
        campaign.goals = data.get('goals', campaign.goals)

        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully!'}), 200
    else:
        return jsonify({'error': 'Campaign not found or you do not own this campaign.'}), 404

# Sponsor - Delete a Campaign
@sponsor_bp.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(sponsor):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    # If the sponsor exists, allow them to delete their campaign
    campaign = Campaign.query.get(campaign_id)

    # Ensure the campaign belongs to the sponsor
    if campaign and campaign.sponsor_id == sponsor.id:
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign deleted successfully!'}), 200
    else:
        return jsonify({'error': 'Campaign not found or you do not own this campaign.'}), 404

# Fetch Sponsor Details (e.g., Username)
@sponsor_bp.route('/details', methods=['GET'])
@jwt_required()
def get_sponsor_details():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'Sponsor not found.'}), 404
    
    return jsonify({
        'username': user.username
    }), 200




# Fetch all ad requests for a sponsor's campaigns
@sponsor_bp.route('/ad-requests', methods=['GET'])
@jwt_required()
def get_ad_requests():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Fetch campaigns created by the sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    campaign_ids = [campaign.id for campaign in campaigns]

    # Fetch ad requests for these campaigns
    ad_requests = AdRequest.query.filter(AdRequest.campaign_id.in_(campaign_ids)).all()

    ad_request_list = [{
        'id': ad_request.id,
        'campaign_id': ad_request.campaign_id,
        'requirements': ad_request.requirements,
        'payment_amount': ad_request.payment_amount,
        'negotiated_payment_amount': ad_request.negotiated_payment_amount,  # New field
        'is_negotiated': ad_request.is_negotiated,  # New field to indicate negotiation status
        'status': ad_request.status,
        'messages': ad_request.messages,
        'influencer_name': ad_request.influencer.user.username
    } for ad_request in ad_requests]

    return jsonify(ad_request_list), 200



# Create a new ad request for a campaign
@sponsor_bp.route('/ad-requests', methods=['POST'])
@jwt_required()
def create_ad_request():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    data = request.json
    campaign_id = data.get('campaign_id')
    influencer_id = data.get('influencer_id')
    requirements = data.get('requirements')
    payment_amount = data.get('payment_amount')

    # Validate input data
    if not campaign_id or not influencer_id or not requirements or not payment_amount:
        return jsonify({'error': 'All fields are required.'}), 400

    # Ensure the sponsor owns the campaign
    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)
    campaign = Campaign.query.get(campaign_id)

    if campaign.sponsor_id != sponsor.id:
        return jsonify({'error': 'You do not own this campaign.'}), 403

    # Create the ad request
    new_ad_request = AdRequest(
        campaign_id=campaign_id,
        influencer_id=influencer_id,
        
        requirements=requirements,
        payment_amount=payment_amount,
        status='Pending',
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_ad_request)
    db.session.commit()

    return jsonify({'message': 'Ad request created successfully!'}), 201


# Edit an ad request
@sponsor_bp.route('/ad-requests/<int:ad_request_id>', methods=['PUT'])
@jwt_required()
def update_ad_request(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    data = request.json
    ad_request = AdRequest.query.get(ad_request_id)

    if not ad_request:
        return jsonify({'error': 'Ad request not found.'}), 404

    # Ensure the ad request belongs to the sponsor's campaign
    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    if ad_request.campaign.sponsor_id != sponsor.id:
        return jsonify({'error': 'You do not own this ad request.'}), 403

    # Update ad request details
    ad_request.requirements = data.get('requirements', ad_request.requirements)
    ad_request.payment_amount = data.get('payment_amount', ad_request.payment_amount)
    ad_request.status = data.get('status', ad_request.status)

    db.session.commit()

    return jsonify({'message': 'Ad request updated successfully!'}), 200

# Delete an ad request
@sponsor_bp.route('/ad-requests/<int:ad_request_id>', methods=['DELETE'])
@jwt_required()
def delete_ad_request(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    ad_request = AdRequest.query.get(ad_request_id)

    if not ad_request:
        return jsonify({'error': 'Ad request not found.'}), 404

    # Ensure the ad request belongs to the sponsor's campaign
    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    if ad_request.campaign.sponsor_id != sponsor.id:
        return jsonify({'error': 'You do not own this ad request.'}), 403

    db.session.delete(ad_request)
    db.session.commit()

    return jsonify({'message': 'Ad request deleted successfully!'}), 200




@sponsor_bp.route('/influencers', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=10)  # Cache based on query parameters
def get_all_influencers():
    category = request.args.get('category')
    expertise = request.args.get('expertise')
    reach = request.args.get('reach', type=int)

    query = Influencer.query

    if category:
        query = query.filter_by(category=category)
    if expertise:
        query = query.filter(Influencer.expertise.ilike(f"%{expertise}%"))
    if reach:
        query = query.filter(Influencer.reach >= reach)

    influencers = query.all()

    influencer_list = [{
        'id': influencer.id,
        'username': influencer.user.username,
        'category': influencer.category,
        'expertise': influencer.expertise,
        'reach': influencer.reach
    } for influencer in influencers]

    return jsonify(influencer_list), 200

# Add cache invalidation when campaign is created/updated
def invalidate_campaign_cache():
    cache.delete('sponsor_campaigns')



# Endpoint to accept a negotiation
@sponsor_bp.route('/ad-requests/<int:ad_request_id>/accept', methods=['PUT'])
@jwt_required()
def accept_negotiation(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad Request not found.'}), 404

    # Update the payment to the negotiated amount and set status to 'Accepted'
    if ad_request.is_negotiated and ad_request.negotiated_payment_amount:
        #ad_request.payment_amount = ad_request.negotiated_payment_amount
        ad_request.status = "Accepted"
        # Clear the negotiated payment after acceptance
        ad_request.is_negotiated = False
        
        db.session.commit()
        return jsonify({'message': 'Ad Request accepted and payment updated to negotiated amount.'}), 200
    else:
        return jsonify({'error': 'No negotiated amount found for this request.'}), 400


# Endpoint to reject a negotiation
@sponsor_bp.route('/ad-requests/<int:ad_request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_negotiation(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad Request not found.'}), 404

    # Reset negotiation status and clear negotiated amount
    ad_request.negotiated_payment_amount = ad_request.payment_amount
    ad_request.is_negotiated = False

    db.session.commit()

    return jsonify({'message': 'Negotiation rejected. Payment remains unchanged.'}), 200



# Route to fetch incoming ad requests from influencers who applied to sponsor's campaigns (public)
@sponsor_bp.route('/incoming-requests', methods=['GET'])
@jwt_required()
def get_incoming_requests():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Get all public campaigns created by the sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id, visibility='public').all()
    campaign_ids = [campaign.id for campaign in campaigns]

    # Filter out public campaigns that already have an accepted request
    ad_requests = (
        db.session.query(AdRequest)
        .filter(AdRequest.campaign_id.in_(campaign_ids), AdRequest.status == 'Pending')
        .all()
    )

    # Filter out campaigns that already have an accepted request
    filtered_ad_requests = []
    for ad_request in ad_requests:
        # Check if there is already an accepted request for this campaign
        accepted_request_exists = AdRequest.query.filter_by(campaign_id=ad_request.campaign_id, status='Accepted').first()
        if not accepted_request_exists:
            filtered_ad_requests.append(ad_request)

    # Prepare the response
    ad_request_list = [{
        'id': ad_request.id,
        'campaign_name': ad_request.campaign.name,
        'influencer_name': ad_request.influencer.user.username,
        'payment_amount': ad_request.payment_amount,
        'category': ad_request.influencer.category,
        'reach': ad_request.influencer.reach,
        'status': ad_request.status,
        'is_public': ad_request.campaign.visibility == 'public'
    } for ad_request in filtered_ad_requests]

    return jsonify(ad_request_list), 200




# Endpoint to accept an incoming request
@sponsor_bp.route('/incoming-requests/<int:ad_request_id>/accept', methods=['PUT'])
@jwt_required()
def accept_incoming_request(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad Request not found.'}), 404

    ad_request.status = 'Accepted'
    db.session.commit()

    return jsonify({'message': 'Ad Request has been accepted.'}), 200


# Endpoint to reject an incoming request
@sponsor_bp.route('/incoming-requests/<int:ad_request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_incoming_request(ad_request_id):
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'error': 'Ad Request not found.'}), 404

    ad_request.status = 'Rejected'
    db.session.commit()

    return jsonify({'message': 'Ad Request has been rejected.'}), 200



@sponsor_bp.route('/export-campaigns', methods=['GET'])
@jwt_required()
def export_campaigns():
    if not is_sponsor():
        return jsonify({'error': 'Access forbidden: Sponsors only!'}), 403

    user_id = get_jwt_identity()
    sponsor = Sponsor.query.get(user_id)

    # Check if the profile is complete
    if not is_profile_complete(sponsor):
        return jsonify({'error': 'Profile incomplete. Please complete your profile first.'}), 403

    # Get all campaigns for the sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id, flagged='Active').all()

    # Create a StringIO object to write CSV data
    si = StringIO()
    writer = csv.writer(si)

    # Write headers
    writer.writerow(['Campaign Name', 'Description', 'Start Date', 'End Date', 
                    'Budget', 'Visibility', 'Goals', 'Category', 'Status'])

    # Write campaign data
    for campaign in campaigns:
        writer.writerow([
            campaign.name,
            campaign.description,
            campaign.start_date,
            campaign.end_date,
            campaign.budget,
            campaign.visibility,
            campaign.goals,
            campaign.category,
            campaign.flagged
        ])

    # Create the response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=campaign_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output
