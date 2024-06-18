import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

# Database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'drtfg67gb'  # Set a secure secret key here

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# # Models
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)

# User Model with Authentication
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Routes for Authentication
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('manage_meetings'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Models
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('meetings', lazy=True))
 
class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    meeting = db.relationship('Meeting', backref=db.backref('participants', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('participants', lazy=True))

# API Endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user_to_dict(user) for user in users])

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room_to_dict(room) for room in rooms])

@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([meeting_to_dict(meeting) for meeting in meetings])

@app.route('/api/participants', methods=['GET'])
def get_participants():
    participants = Participant.query.all()
    return jsonify([participant_to_dict(participant) for participant in participants])

def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

def room_to_dict(room):
    return {
        'id': room.id,
        'room_name': room.room_name,
        'capacity': room.capacity
    }

def meeting_to_dict(meeting):
    return {
        'id': meeting.id,
        'title': meeting.title,
        'description': meeting.description,
        'start_time': meeting.start_time.isoformat(),
        'end_time': meeting.end_time.isoformat(),
        'room_id': meeting.room_id
    }

def participant_to_dict(participant):
    return {
        'id': participant.id,
        'meeting_id': participant.meeting_id,
        'user_id': participant.user_id
    }

# Frontend Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/admin/meetings', methods=['GET', 'POST'])
def manage_meetings():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        room_id = request.form['room_id']
        participants = request.form.getlist('participants')

        # Validate input
        if not all([title, start_time, end_time, room_id]):
            flash('All fields are required', 'error')
            return redirect(url_for('manage_meetings'))

        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date/time format', 'error')
            return redirect(url_for('manage_meetings'))

        # Check for meeting collision
        if is_meeting_collision(start_time, end_time, room_id):
            flash('Meeting time overlaps with existing meetings!', 'error')
            return redirect(url_for('manage_meetings'))
        
         # Check if the number of participants exceeds room capacity
        if not is_room_capacity_sufficient(room_id, len(participants)):
            room = Room.query.get(room_id)
            flash(f'The number of participants exceeds the room capacity of {room.capacity}!', 'error')
            return redirect(url_for('manage_meetings'))

        # Check if the meeting duration exceeds the limit (e.g., 4 hours)
        max_duration = timedelta(hours=4)
        if (end_time - start_time) > max_duration:
            flash('Meeting duration cannot exceed 4 hours!', 'error')
            return redirect(url_for('manage_meetings'))

        # Create new meeting
        new_meeting = Meeting(title=title, description=description, start_time=start_time, end_time=end_time, room_id=room_id)
        db.session.add(new_meeting)
        db.session.commit()

        # Add participants to the meeting
        for user_id in participants:
            participant = Participant(meeting_id=new_meeting.id, user_id=user_id)
            db.session.add(participant)
        
        db.session.commit()
        flash('Meeting created successfully!', 'success')
        return redirect(url_for('manage_meetings'))

    rooms = Room.query.all()
    meetings = Meeting.query.all()
    users = User.query.all()
    return render_template('manage_meetings.html', rooms=rooms, meetings=meetings, users=users)

def is_meeting_collision(start_time, end_time, room_id):
    # Check if there's any overlapping meeting in the same room
    overlapping_meetings = Meeting.query.filter(
        Meeting.room_id == room_id,
        ((Meeting.start_time < end_time) & (Meeting.end_time > start_time))
    ).all()

    return len(overlapping_meetings) > 0

def is_room_capacity_sufficient(room_id, participant_count):
    room = Room.query.get(room_id)
    return participant_count <= room.capacity

# Helper functions for templates (same as before)
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/meetings')
def meetings():
    return render_template('meetings.html')

@app.route('/participants')
def participants():
    return render_template('participants.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
