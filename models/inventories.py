from app import db

class InventoryModel(db.Model):
    __tablename__='inventories'
    id = db.Column(db.Integer,primary_key=True)
    invname = db.Column(db.String(60),nullable=False)
    invtype = db.Column(db.String(45),nullable=False)
    bp = db.Column(db.Float,nullable=False)
    sp = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer,nullable=False)
    rp = db.Column(db.Integer,nullable=False)
    sales=db.relationship('SalesModel', backref='inventory',lazy=True)

    @classmethod
    def updatestock(cls,id,quantity):
        record = cls.query.filter_by(id=id).first()
        if record.stock < quantity:
            return False
        else:

            if record:
                record.stock=record.stock-quantity
                db.session.commit()
                return True
            else:
                return False

    @classmethod
    def editstock(cls,id,chname,chtype,chbp,chsp,chstock,chreoder):
        editables=cls.query.filter_by(id=id).first()
        if editables:
            editables.invname=chname
            editables.invtype=chtype
            editables.bp=chbp
            editables.sp=chsp
            editables.stock=chstock
            editables.rp=chreoder
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def getTypeCount(cls,type):
        typeCount=cls.query.filter_by(invtype=type).count()
        return typeCount
    @classmethod
    def salesOverTime(cls):

        pass

