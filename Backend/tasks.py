# tasks.py
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
import csv
import io
from models import Campaign, Influencer, AdRequest, User, Sponsor
from db import db

from app import application, mail

from flask_mail import Message

# Initialize Celery
celery = Celery('tasks', 
                broker='redis://localhost:6379/1',
                backend='redis://localhost:6379/1')

# Configure Celery
celery.conf.update(
    timezone='Asia/Kolkata',
    beat_schedule={
        'daily-reminders': {
            'task': 'tasks.send_daily_reminders',
            'schedule': 60.0
            #'schedule': crontab(hour=18, minute=0)  # 6 PM daily
        },
        'monthly-reports': {
            'task': 'tasks.generate_monthly_reports',
            'schedule': 60.0,
            #'schedule': crontab(0, 0, day_of_month='1')  # 1st of every month
        }
    }
)

def init_celery():
    celery.conf.update(application.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with application.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = init_celery()

@celery.task
def send_daily_reminders():
    print(f"Task started at: {datetime.now()}")
    try:
        current_time = datetime.utcnow()
        
        # Query influencers with pending requests
        influencers = Influencer.query.join(User).all()
        print("Found influencers:", influencers) 
        
        for influencer in influencers:
            # Check for pending requests
            pending_requests = AdRequest.query.filter_by(
                influencer_id=influencer.id,
                status='Pending'
            ).count()
            
            if pending_requests > 0:
                msg = Message(
                    'Pending Ad Requests Reminder',
                    sender=application.config['MAIL_USERNAME'],
                    recipients=[influencer.user.email]
                )
                msg.body = f"""
                Hello {influencer.user.username},
                
                You have {pending_requests} pending ad request(s) waiting for your response.
                Please login to your dashboard to review them.
                
                Best regards,
                The Team
                """
                mail.send(msg)
    except Exception as e:
        print(f"Error in send_daily_reminders: {str(e)}")

@celery.task
def generate_monthly_reports():
    """Generate and send monthly activity reports for sponsors."""
    # from app import app, mail
    # from flask_mail import Message
    
    with application.app_context():
        current_date = datetime.utcnow()
        month_year = current_date.strftime("%B %Y")
        
        sponsors = Sponsor.query.join(User).all()
        for sponsor in sponsors:
            # Get campaign statistics
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
            report_data = []
            
            for campaign in campaigns:
                campaign_stats = {
                    'name': campaign.name,
                    'total_requests': len(campaign.ad_requests),
                    'accepted_requests': sum(1 for r in campaign.ad_requests if r.status == 'Accepted'),
                    'budget_used': sum(r.payment_amount for r in campaign.ad_requests if r.status == 'Accepted')
                }
                report_data.append(campaign_stats)
            
            # Create email content
            html_content = create_monthly_report_html(sponsor, report_data, month_year)
            
            msg = Message(
                f'Monthly Campaign Report - {month_year}',
                sender=application.config['MAIL_USERNAME'],
                recipients=[sponsor.user.email],
                html=html_content
            )
            mail.send(msg)

# @celery.task
# def export_campaign_data(sponsor_id):
#     """Export campaign data as CSV."""
#     # from app import app
    
#     with application.app_context():
#         # Get all campaigns for the sponsor
#         campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
        
#         # Create CSV in memory
#         output = io.StringIO()
#         writer = csv.writer(output)
        
#         # Write headers
#         writer.writerow([
#             'Campaign Name', 'Description', 'Start Date', 'End Date',
#             'Budget', 'Visibility', 'Goals', 'Category', 'Status'
#         ])
        
#         # Write campaign data
#         for campaign in campaigns:
#             writer.writerow([
#                 campaign.name,
#                 campaign.description,
#                 campaign.start_date,
#                 campaign.end_date,
#                 campaign.budget,
#                 campaign.visibility,
#                 campaign.goals,
#                 campaign.category,
#                 campaign.flagged
#             ])
        
#         return output.getvalue()

def create_monthly_report_html(sponsor, report_data, month_year):
    """Helper function to create HTML report."""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: #f8f9fa; padding: 20px; }}
                .campaign {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .stats {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Monthly Campaign Report - {month_year}</h2>
                <p>Dear {sponsor.user.username},</p>
            </div>
            
            <div class="content">
                {''.join(f'''
                <div class="campaign">
                    <h3>{campaign['name']}</h3>
                    <div class="stats">
                        <p>Total Requests: {campaign['total_requests']}</p>
                        <p>Accepted Requests: {campaign['accepted_requests']}</p>
                        <p>Budget Used: ${campaign['budget_used']}</p>
                    </div>
                </div>
                ''' for campaign in report_data)}
            </div>
        </body>
    </html>
    """