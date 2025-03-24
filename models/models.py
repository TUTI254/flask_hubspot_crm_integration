from datetime import datetime
from utils.extensions import db

class Contact(db.Model):
    """Model for storing HubSpot contacts."""
    __tablename__ = "contacts"

    id: int = db.Column(db.Integer, primary_key=True)
    hubspot_id: str = db.Column(db.String(50), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    firstname: str = db.Column(db.String(80), nullable=False)
    lastname: str = db.Column(db.String(80), nullable=False)
    phone: str = db.Column(db.String(20))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.email}>"

class Deal(db.Model):
    """Model for storing HubSpot deals."""
    __tablename__ = "deals"

    id: int = db.Column(db.Integer, primary_key=True)
    hubspot_id: str = db.Column(db.String(50), unique=True, nullable=False)
    dealname: str = db.Column(db.String(120), nullable=False)
    amount: float = db.Column(db.Float, nullable=False)
    dealstage: str = db.Column(db.String(80), nullable=False)
    contact_id: int = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contact = db.relationship("Contact", backref=db.backref("deals", lazy=True))

    def __repr__(self):
        return f"<Deal {self.dealname}>"

class Ticket(db.Model):
    """Model for storing HubSpot support tickets."""
    __tablename__ = "tickets"

    id: int = db.Column(db.Integer, primary_key=True)
    hubspot_id: str = db.Column(db.String(50), unique=True, nullable=False)
    subject: str = db.Column(db.String(200), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    category: str = db.Column(db.String(50), nullable=False)
    pipeline: str = db.Column(db.String(50), nullable=False)
    hs_ticket_priority: str = db.Column(db.String(50), nullable=False)
    hs_pipeline_stage: str = db.Column(db.String(50), nullable=False)
    contact_id: int = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    deal_ids = db.Column(db.ARRAY(db.Integer))  # Array of associated deal IDs
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contact = db.relationship("Contact", backref=db.backref("tickets", lazy=True))

    def __repr__(self):
        return f"<Ticket {self.subject}>"
