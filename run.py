# Description: This file is used to run the backend server
# and the backend server is used to provide the api for the frontend
# and the backend server is also used to provide the socket communication between the server and the client
# and the backend server is also used to provide the database for the frontend
# and the backend server is also used to provide the email service for the frontend
# and the backend server is also used to provide the session for the frontend
# and the backend server is also used to provide the user management for the frontend
# and the backend server is also used to provide the admin management for the frontend
from app import app, socketio
app.run(debug=True, host='0.0.0.0', port=8800)