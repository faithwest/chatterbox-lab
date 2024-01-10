from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask import Flask, jsonify, request
from models import Message 

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

app = Flask(__name__)


#GET
@app.route('/messages')
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])


#POST
@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    if not body or not username:
        return jsonify({'error': 'Missing body or username'}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


#PATCH
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    body = request.json.get('body')

    if body:
        message.body = body
        db.session.commit()

    return jsonify(message.to_dict())


#DELETE
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted'})


class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
     id = db.Column(db.Integer, primary_key=True)
     body = db.Column(db.Text)
     username = db.Column(db.String(80))
     created_at = db.Column(db.DateTime, server_default=db.func.now())

     def to_dict(self):
         return {
             'id': self.id,
             'body': self.body,
             'username': self.username,
             'created_at': self.created_at.isoformat()
         }

#RETRIEVE
messages = Message.query.order_by(Message.created_at).all()

#CREATING
new_message = Message(body=body, username=username)
db.session.add(new_message)
db.session.commit()

#UPDATING
message.body = new_body
db.session.commit()

#DELETE
db.session.delete(message)
db.session.commit()

