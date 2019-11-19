from app import db
# from sqlalchemy.sql import func
from datetime import datetime


class SalesModel(db.Model):
    __tablename__='sales'
    id = db.Column(db.Integer,primary_key=True)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    qyt = db.Column(db.Integer, nullable=False)
    # created_time = db.Column(db.DateTime(timezone=True),server_default=func.now())
    time_created = db.Column(db.DateTime,default=datetime.utcnow)
