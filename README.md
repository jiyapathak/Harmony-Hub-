# MusicHub Flask Login Application

A complete Flask-based login system with user authentication, CSV storage, and a beautiful musical theme.

## Features

- ✅ User Registration (Sign Up)
- ✅ User Login with Email Verification
- ✅ Password Hashing for Security
- ✅ Session Management
- ✅ CSV-based User Storage
- ✅ Beautiful Animated UI
- ✅ Form Validation
- ✅ Error Handling

## Project Structure

```
your_project/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── users.csv             # User data storage (auto-created)
│
└── templates/
    ├── index.html        # Login/Signup page
    └── home.html         # Dashboard after login
```

## Installation & Setup

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed on your system.

### Step 2: Create Project Directory
```bash
mkdir musichub
cd musichub
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create Folder Structure
```bash
# Create templates folder
mkdir templates
```

### Step 6: Add Files
- Save `app.py` in the root directory
- Save `index.html` in the `templates` folder
- Save `home.html` in the `templates` folder
- Save `requirements.txt` in the root directory

### Step 7: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

## How It Works

### User Registration (Sign Up)
1. User fills out the signup form with:
   - Full Name
   - Email
   - Password
   - Confirm Password
2. Flask validates the data
3. Password is hashed using Werkzeug's security functions
4. User data is stored in `users.csv`

### User Login
1. User enters email and password
2. Flask checks if user exists in CSV
3. Password is verified using hash comparison
4. Session is created with user information
5. User is redirected to home page

### Session Management
- User sessions are managed using Flask's session
- Protected routes check if user is logged in
- Logout clears the session

## CSV File Structure

The `users.csv` file stores user data with the following columns:

| full_name | email | password_hash | created_at |
|-----------|-------|---------------|------------|
| John Doe | john@example.com | hashed_password | 2024-01-15 10:30:00 |

## Security Features

1. **Password Hashing**: Passwords are hashed using `generate_password_hash()`
2. **Session Secret**: Uses Flask's secret key for session management
3. **Password Verification**: Uses `check_password_hash()` for secure comparison
4. **Input Validation**: Server-side validation for all form inputs

## API Endpoints

### `/` (GET)
- Main page - displays login/signup forms
- Redirects to home if already logged in

### `/signup` (POST)
- Accepts JSON: `{full_name, email, password, confirm_password}`
- Creates new user account
- Returns success/error message

### `/login` (POST)
- Accepts JSON: `{identifier, password}`
- Authenticates user
- Creates session
- Returns success/error message

### `/home` (GET)
- Protected route - requires login
- Displays dashboard
- Shows user information

### `/logout` (GET)
- Clears user session
- Redirects to login page

## Customization

### Change Secret Key
In `app.py`, change this line:
```python
app.secret_key = 'your-secret-key-here-change-this'
```
Use a random, secure string in production.

### Change CSV File Location
Modify the `USERS_CSV` variable in `app.py`:
```python
USERS_CSV = 'path/to/your/users.csv'
```

### Styling
- Edit CSS in `templates/index.html` for login page
- Edit CSS in `templates/home.html` for dashboard

## Troubleshooting

### "Module not found" Error
```bash
pip install Flask werkzeug
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### CSV File Not Creating
Check write permissions in the directory.

## Future Enhancements

- Password reset functionality
- Email verification
- Database integration (SQLite/PostgreSQL)
- Profile management
- Remember me functionality
- OAuth social login

## Important Notes

⚠️ **For Development Only**: This setup uses CSV files and is suitable for learning and small projects. For production applications, use a proper database (SQLite, PostgreSQL, MySQL) and additional security measures.

⚠️ **Change Secret Key**: Always use a strong, random secret key in production.

⚠️ **HTTPS**: Use HTTPS in production to encrypt data transmission.

## Testing the Application

1. Start the server
2. Go to `http://127.0.0.1:5000/`
3. Click "Sign Up" tab
4. Create a new account
5. Login with your credentials
6. You'll be redirected to the home page
7. Click "Logout" to end session

## Support

If you encounter any issues:
1. Check that all files are in the correct folders
2. Ensure Flask is installed correctly
3. Check console for error messages
4. Verify port 5000 is not in use

Enjoy your MusicHub application! 🎵🎶