from flask import Blueprint, jsonify, request
from models import User, Campaign, AdRequest , Influencer
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy import or_
# from app import export_cache as cache
from cache import cache


admin_bp = Blueprint('admin', __name__)


def is_admin():
    jwt_claims = get_jwt()  # Get the JWT claims (payload)
    return jwt_claims.get('role') == 'Admin'  # Check if the role in the token is 'Admin'


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=10, key_prefix='admin_dashboard')  
def dashboard():
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch statistics from the database
    total_sponsors = User.query.filter_by(role='Sponsor').count()
    flagged_sponsors = User.query.filter_by(role='Sponsor', flagged='Flagged').count()
    
    total_influencers = User.query.filter_by(role='Influencer').count()
    flagged_influencers = User.query.filter_by(role='Influencer', flagged='Flagged').count()
    
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility="public").count()
    private_campaigns = Campaign.query.filter_by(visibility="private").count()
    flagged_campaigns = Campaign.query.filter_by(flagged="Flagged").count()
    
    total_ad_requests = AdRequest.query.count()
    pending_ad_requests = AdRequest.query.filter_by(status='Pending').count()
    accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()
    rejected_ad_requests = AdRequest.query.filter_by(status='Rejected').count()

    return jsonify({
        'total_sponsors': total_sponsors,
        'flagged_sponsors': flagged_sponsors,
        'total_influencers': total_influencers,
        'flagged_influencers': flagged_influencers,
        'total_campaigns': total_campaigns,
        'public_campaigns': public_campaigns,
        'private_campaigns': private_campaigns,
        'flagged_campaigns': flagged_campaigns,
        'total_ad_requests': total_ad_requests,
        'pending_ad_requests': pending_ad_requests,
        'accepted_ad_requests': accepted_ad_requests,
        'rejected_ad_requests': rejected_ad_requests
    }), 200

# Approve a Sponsor 
@admin_bp.route('/approve-sponsor/<int:sponsor_id>', methods=['POST'])
@jwt_required()
def approve_sponsor(sponsor_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    sponsor = User.query.get(sponsor_id)
    if sponsor and sponsor.role == 'Sponsor':
        sponsor.flagged = "Active" 
        db.session.commit()
        return jsonify({'message': 'Sponsor approved successfully!'}), 200
    return jsonify({'error': 'Sponsor not found or invalid'}), 404


# Get flagged sponsors for approval , when a new sponsor logs in (flagged has null )
@admin_bp.route('/flagged-sponsors', methods=['GET'])
@jwt_required()
def get_flagged_sponsors():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch sponsors where flagged is either NULL or "Flagged"
    sponsors = User.query.filter_by(role='Sponsor').filter(or_(User.flagged == None, User.flagged == 'Flagged')).all()
    #sponsors = User.query.filter_by(role='Sponsor').filter(User.flagged == 'Flagged').all()
    return jsonify([{'id': sponsor.id, 'username': sponsor.username, 'email': sponsor.email, 'flagged': sponsor.flagged or 'Active'} for sponsor in sponsors]), 200


# Get all active sponsors (flagged as 'Active')
@admin_bp.route('/active-sponsors', methods=['GET'])
@jwt_required()
def get_active_sponsors():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch sponsors where flagged is 'Active'
    sponsors = User.query.filter_by(role='Sponsor', flagged='Active').all()
    return jsonify([{'id': sponsor.id, 'username': sponsor.username, 'email': sponsor.email, 'flagged': sponsor.flagged} for sponsor in sponsors]), 200


# Get all sponsors with their flagged status
@admin_bp.route('/sponsors', methods=['GET'])
@jwt_required()
def get_sponsors():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch all sponsors and their flagged status from User
    sponsors = User.query.filter_by(role='Sponsor').all()
    return jsonify([
        {'id': sponsor.id, 'username': sponsor.username, 'email': sponsor.email, 'flagged': sponsor.flagged}
        for sponsor in sponsors
    ]), 200


# Invalidate dashboard cache when status changes
def invalidate_dashboard_cache():
    cache.delete('admin_dashboard')
    

# Flag a Sponsor (Admin Action)
@admin_bp.route('/flag-sponsor/<int:sponsor_id>', methods=['PUT'])
@jwt_required()
def flag_sponsor(sponsor_id):
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    sponsor = User.query.get(sponsor_id)
    if sponsor and sponsor.role == 'Sponsor':
        sponsor.flagged = "Flagged"  # Set the sponsor as flagged
        db.session.commit()
        invalidate_dashboard_cache()
        return jsonify({'message': 'Sponsor flagged successfully!'}), 200
    return jsonify({'error': 'Sponsor not found'}), 404

# Unflag a Sponsor (Admin Action)
@admin_bp.route('/unflag-sponsor/<int:sponsor_id>', methods=['PUT'])
@jwt_required()
def unflag_sponsor(sponsor_id):
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    sponsor = User.query.get(sponsor_id)
    if sponsor and sponsor.role == 'Sponsor':
        sponsor.flagged = "Active"  # Set the sponsor as active (unflagged)
        db.session.commit()
        return jsonify({'message': 'Sponsor unflagged successfully!'}), 200
    return jsonify({'error': 'Sponsor not found'}), 404




# Get recent ad requests for the dashboard
@admin_bp.route('/recent-ad-requests', methods=['GET'])
@jwt_required()
def get_recent_ad_requests():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    requests = AdRequest.query.order_by(AdRequest.created_at.desc()).limit(10).all()
    return jsonify([{
        'id': req.id,
        'campaign_name': req.campaign.name,
        'sponsor_name': req.campaign.sponsor.user.username,
        'influencer_name': req.influencer.user.username,
        'requirements': req.requirements,
        'status': req.status
    } for req in requests]), 200


# Flag an Influencer (Admin Action)
@admin_bp.route('/flag-influencer/<int:influencer_id>', methods=['PUT'])
@jwt_required()
def flag_influencer(influencer_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch the user associated with the influencer
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        influencer.user.flagged = "Flagged"  # Set the user (influencer) as flagged
        db.session.commit()
        return jsonify({'message': 'Influencer flagged successfully!'}), 200
    return jsonify({'error': 'Influencer not found'}), 404


# Unflag an Influencer (Admin Action)
@admin_bp.route('/unflag-influencer/<int:influencer_id>', methods=['PUT'])
@jwt_required()
def unflag_influencer(influencer_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch the user associated with the influencer
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        influencer.user.flagged = "Active"  # Set the user (influencer) as active
        db.session.commit()
        return jsonify({'message': 'Influencer unflagged successfully!'}), 200
    return jsonify({'error': 'Influencer not found'}), 404


# Unflag an Influencer (Admin Action)
@admin_bp.route('/approve-influencer/<int:influencer_id>', methods=['POST'])
@jwt_required()
def approve_influencer(influencer_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch the user associated with the influencer
    influencer = Influencer.query.get(influencer_id)
    if influencer:
        influencer.user.flagged = "Active"  # Set the user (influencer) as active
        db.session.commit()
        return jsonify({'message': 'Influencer approved successfully!'}), 200
    return jsonify({'error': 'Influencer not found'}), 404



# Get all influencers with their flagged status
@admin_bp.route('/influencers', methods=['GET'])
@jwt_required()
def get_influencers():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch all influencers and their flagged status from User
    influencers = Influencer.query.join(User).all()
    return jsonify([
        {'id': influencer.id, 'username': influencer.user.username, 'email': influencer.user.email, 'flagged': influencer.user.flagged}
        for influencer in influencers
    ]), 200



# Get all campaigns with their flagged status
@admin_bp.route('/campaigns', methods=['GET'])
@jwt_required()
def get_campaigns():
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch all campaigns and their flagged status
    campaigns = Campaign.query.all()
    return jsonify([
        {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'visibility': campaign.visibility,
            'flagged': campaign.flagged
        }
        for campaign in campaigns
    ]), 200



# Flag a Campaign (Admin Action)
@admin_bp.route('/flag-campaign/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def flag_campaign(campaign_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch the campaign by ID
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.flagged = "Flagged"  # Set the campaign as flagged
        db.session.commit()
        return jsonify({'message': 'Campaign flagged successfully!'}), 200
    return jsonify({'error': 'Campaign not found'}), 404

# Unflag a Campaign (Admin Action)
@admin_bp.route('/unflag-campaign/<int:campaign_id>', methods=['PUT'])
@jwt_required()
def unflag_campaign(campaign_id):
    # Check if the user is an admin
    if not is_admin():
        return jsonify({'error': 'Access forbidden: Admins only!'}), 403

    # Fetch the campaign by ID
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.flagged = "Active"  # Set the campaign as active (unflagged)
        db.session.commit()
        return jsonify({'message': 'Campaign unflagged successfully!'}), 200
    return jsonify({'error': 'Campaign not found'}), 404

