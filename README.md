# Calendar-Meet-Mingle
Calendar Management System, helps you to book spaces, schedule meetings, etc.

<PROJECT IN PROGRESS>

# App Documentation

## Overview
This Flask application manages meetings in various rooms. It includes user authentication, CRUD operations for meetings, and API endpoints to retrieve data.

## Dependencies
- Flask: Micro web framework for Python
- Flask-SQLAlchemy: Flask extension for SQLAlchemy ORM
- Flask-Login: Provides user session management
- Werkzeug: Includes password hashing utilities
- PostgreSQL: Database system for storing meeting, room, and user data

## Setup
### Environment Variables:
- DB_HOST: PostgreSQL host address
- DB_PORT: PostgreSQL port
- DB_NAME: PostgreSQL database name
- DB_USER: PostgreSQL username
- DB_PASSWORD: PostgreSQL password

### Configuration:
- SQLALCHEMY_DATABASE_URI: Connection URI for PostgreSQL database
- SQLALCHEMY_TRACK_MODIFICATIONS: Disable modification tracking
- SECRET_KEY: Secure key for session management

## Models
- **User:**
  - Attributes: id, name, email, password_hash
  - Methods: set_password(), check_password()

- **Room:**
  - Attributes: id, room_name, capacity

- **Meeting:**
  - Attributes: id, title, description, start_time, end_time, room_id

- **Participant:**
  - Attributes: id, meeting_id, user_id

## Routes
### Authentication
- /login: Login endpoint for users
- /logout: Logout endpoint

### API Endpoints
- /api/users: GET all users
- /api/rooms: GET all rooms
- /api/meetings: GET all meetings
- /api/participants: GET all participants

### Frontend Routes
- /: Home page
- /base: Base template
- /admin/meetings: Manage meetings (POST to create, GET to view)

## Functions
### Utility Functions:
- user_to_dict(), room_to_dict(), meeting_to_dict(), participant_to_dict(): Convert objects to dictionaries for JSON serialization
- datetimeformat(): Template filter for formatting datetime objects

### Validation Functions:
- is_meeting_collision(): Check for overlapping meetings in the same room
- is_room_capacity_sufficient(): Validate if room capacity meets participant count

## Templates
- Templates are stored in templates/ directory and include:
  - base.html: Base template
  - index.html: Home page
  - login.html: Login page
  - manage_meetings.html: Meeting management page
  - Other templates: users.html, rooms.html, meetings.html, participants.html

## Running the App
- Execute `python app.py` to start the Flask development server.

## Notes
- Ensure PostgreSQL server is running and environment variables are correctly set.
- Secure the SECRET_KEY and database credentials in production environments.
