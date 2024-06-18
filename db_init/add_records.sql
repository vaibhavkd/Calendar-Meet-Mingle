-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    room_id INT REFERENCES rooms(id)
);

CREATE TABLE IF NOT EXISTS participants (
    id SERIAL PRIMARY KEY,
    meeting_id INT REFERENCES meetings(id),
    user_id INT REFERENCES users(id)
);

-- Insert dummy users
INSERT INTO users (name, email, password_hash) VALUES ('Alice Johnson', 'alice@example.com', 'scrypt:32768:8:1$oqtihBMXQ3AW0eea$32301d11c00a48db347c5b6705e88716f5ecca045ea2ecc6387bcab40e7d8423f0c83c9570431764f8bb051088d7ed7f9ec0ff8381915cf58f191788ba4940da');
INSERT INTO users (name, email, password_hash) VALUES ('Bob Smith', 'bob@example.com', 'scrypt:32768:8:1$mkVBMtsTzDVK2LU6$c3cdbb1c502f0d818ea8d0a25e4f8e9c0b383cef3c82784549e37502f74fd8593db7d75169599bd42ece58cecbded582a31b4ddbcb1239d0dc7594ebce097ecc');
INSERT INTO users (name, email, password_hash) VALUES ('Charlie Brown', 'charlie@example.com', 'scrypt:32768:8:1$bHD6PH7LkW0aieV8$a0a43d72f28d9b2a80fd6f898fd40015876a9d5b57773a53565a8e1fc7785aa4122f8db7a3cc2a9758b5ca5eed6657cb548176a6fc7d92a8bbda32681784ca7e');
INSERT INTO users (name, email, password_hash) VALUES ('David Wilson', 'david@example.com', 'scrypt:32768:8:1$UKTYXuvD5EDxVfMP$29471152e724c8975f8b528a7a929ca449f0210d9cff333654b3e914db8cacc20cd249b639fe409507d571411b9992b0591bb170cf3bc7a0012b2ef6b2acc5a9');
INSERT INTO users (name, email, password_hash) VALUES ('Eve Davis', 'eve@example.com', 'scrypt:32768:8:1$1vs1NXUwSZJfjHd1$5017f438561ca2dba2f59751838d3d508a4b85bfd044919055efe5ca1d68530a965e4b8ccdc3f208dd8d9a27b8d0900162130f730a2fd4edb51ab5a97cacfde3');

-- Insert dummy rooms
INSERT INTO rooms (room_name, capacity) VALUES ('Conference Room A', 10);
INSERT INTO rooms (room_name, capacity) VALUES ('Conference Room B', 20);
INSERT INTO rooms (room_name, capacity) VALUES ('Conference Room C', 15);
INSERT INTO rooms (room_name, capacity) VALUES ('Meeting Room 1', 8);
INSERT INTO rooms (room_name, capacity) VALUES ('Meeting Room 2', 12);

-- Insert dummy meetings
INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Team Meeting', 'Discuss project progress', '2024-06-15 10:00:00', '2024-06-15 11:00:00', 1);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Client Call', 'Call with the client to review requirements', '2024-06-15 14:00:00', '2024-06-15 15:00:00', 2);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Project Kickoff', 'Initial project kickoff meeting', '2024-06-16 09:00:00', '2024-06-16 10:00:00', 3);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Design Review', 'Review design specifications', '2024-06-16 11:00:00', '2024-06-16 12:00:00', 4);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Weekly Sync', 'Weekly team sync-up', '2024-06-17 13:00:00', '2024-06-17 14:00:00', 5);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Budget Planning', 'Plan the budget for next quarter', '2024-06-18 10:00:00', '2024-06-18 11:30:00', 1);

INSERT INTO meetings (title, description, start_time, end_time, room_id) 
VALUES ('Sprint Planning', 'Plan the next sprint tasks', '2024-06-19 15:00:00', '2024-06-19 16:00:00', 2);

-- Insert dummy participants
INSERT INTO participants (meeting_id, user_id) VALUES (1, 1); -- Alice in Team Meeting
INSERT INTO participants (meeting_id, user_id) VALUES (1, 2); -- Bob in Team Meeting
INSERT INTO participants (meeting_id, user_id) VALUES (2, 1); -- Alice in Client Call
INSERT INTO participants (meeting_id, user_id) VALUES (2, 3); -- Charlie in Client Call
INSERT INTO participants (meeting_id, user_id) VALUES (3, 2); -- Bob in Project Kickoff
INSERT INTO participants (meeting_id, user_id) VALUES (3, 4); -- David in Project Kickoff
INSERT INTO participants (meeting_id, user_id) VALUES (4, 1); -- Alice in Design Review
INSERT INTO participants (meeting_id, user_id) VALUES (4, 5); -- Eve in Design Review
INSERT INTO participants (meeting_id, user_id) VALUES (5, 3); -- Charlie in Weekly Sync
INSERT INTO participants (meeting_id, user_id) VALUES (5, 4); -- David in Weekly Sync
INSERT INTO participants (meeting_id, user_id) VALUES (5, 5); -- Eve in Weekly Sync
INSERT INTO participants (meeting_id, user_id) VALUES (6, 1); -- Alice in Budget Planning
INSERT INTO participants (meeting_id, user_id) VALUES (6, 2); -- Bob in Budget Planning
INSERT INTO participants (meeting_id, user_id) VALUES (7, 3); -- Charlie in Sprint Planning
INSERT INTO participants (meeting_id, user_id) VALUES (7, 4); -- David in Sprint Planning
INSERT INTO participants (meeting_id, user_id) VALUES (7, 5); -- Eve in Sprint Planning
