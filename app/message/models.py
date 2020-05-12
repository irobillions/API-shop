from app.factory import db


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content_message = db.Column(db.Text, nullable=False)
    send_at = db.Column(db.DateTime(), nullable=False)
    read_at = db.Column(db.DateTime, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
