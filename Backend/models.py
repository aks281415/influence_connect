from datetime import datetime
from sqlalchemy import CheckConstraint
from db import db

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'Admin', 'Sponsor', 'Influencer'
    flagged = db.Column(db.String)  # Status of user (Active or Flagged)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role in ['Sponsor', 'Influencer'] and not self.flagged:
            self.flagged = 'Flagged'

    __table_args__ = (
        CheckConstraint("role IN ('Admin', 'Sponsor', 'Influencer')", name='check_role'),
    )

    # Relationships
    sponsor = db.relationship('Sponsor', uselist=False, back_populates='user')
    influencer = db.relationship('Influencer', uselist=False, back_populates='user')

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'


# Sponsor Model
class Sponsor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    #company_name = db.Column(db.String)
    industry = db.Column(db.String)
    sponsor_type = db.Column(db.String)

    # Relationships
    user = db.relationship('User', back_populates='sponsor')  # Linking back to the User
    campaigns = db.relationship('Campaign', backref='sponsor')

    def __repr__(self):
        return f'<Sponsor {self.company_name}>'


# Influencer Model
class Influencer(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    category = db.Column(db.String) 
    expertise = db.Column(db.String) 
    reach = db.Column(db.Integer) 

    # Relationships
    user = db.relationship('User', back_populates='influencer')  # Linking back to the User
    ad_requests = db.relationship('AdRequest', backref='influencer')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.user.username,
            'expertise': self.expertise,
            'category': self.category,
            'reach': self.reach
        }

    def __repr__(self):
        return f'<Influencer {self.user.username} - {self.expertise}>'


# Campaign Model
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.String)  
    end_date = db.Column(db.String) 
    budget = db.Column(db.Float)
    visibility = db.Column(db.String)  # 'public', 'private'
    goals = db.Column(db.String)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False) 
    flagged = db.Column(db.String, default="Active")  # Campaign status (Active/Flagged)
    category = db.Column(db.String) 

    __table_args__ = (
        CheckConstraint("visibility IN ('public', 'private')", name='check_visibility'),
    )

    # Relationships
    ad_requests = db.relationship('AdRequest', backref='campaign')

    def __repr__(self):
        return f'<Campaign {self.name} - {self.category} - {self.visibility}>'


# AdRequest Model (Merged)
class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to the campaign (which is created by a sponsor)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    
    # Foreign key to the influencer (who receives the ad request)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    
    # Ad-specific details
    requirements = db.Column(db.String, nullable=True) 
    payment_amount = db.Column(db.Float, nullable=False)
    
    # Communication between the sponsor and influencer
    messages = db.Column(db.String)  

    status = db.Column(db.String, default='Pending')  # Pending, Accepted, Rejected
    
    # When the ad request was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional field to track completion
    completed = db.Column(db.Boolean, default=False)

    is_negotiated = db.Column(db.Boolean, default=False)
    negotiated_payment_amount = db.Column(db.Float, nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('Pending', 'Accepted', 'Rejected')", name='check_status'),
    )

    def __repr__(self):
        return f'<AdRequest {self.id} - {self.status}>'
