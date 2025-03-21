from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    """Model for storing HubSpot contacts."""
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    hubspot_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.email}>"

class Deal(db.Model):
    """Model for storing HubSpot deals."""
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True)
    hubspot_id = db.Column(db.String(50), unique=True, nullable=False)
    dealname = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    dealstage = db.Column(db.String(80), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contact = db.relationship("Contact", backref=db.backref("deals", lazy=True))

    def __repr__(self):
        return f"<Deal {self.dealname}>"

class Ticket(db.Model):
    """Model for storing HubSpot support tickets."""
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    hubspot_id = db.Column(db.String(50), unique=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    pipeline = db.Column(db.String(50), nullable=False)
    hs_ticket_priority = db.Column(db.String(50), nullable=False)
    hs_pipeline_stage = db.Column(db.String(50), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    deal_ids = db.Column(db.ARRAY(db.Integer))  # Array of associated deal IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contact = db.relationship("Contact", backref=db.backref("tickets", lazy=True))

    def __repr__(self):
        return f"<Ticket {self.subject}>"