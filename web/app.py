from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, User, Locations  # Import db and User model
from class_fun import classification
from desc import describe_input
from location_fun import location
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        # Verify the hashed password
        if user and user.check_password(password):
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!')
            return redirect(url_for('main_page'))  # Redirect to the main page
        elif not user:
            flash('Username not found. Would you like to register instead?')
            return render_template('login.html', show_register_button=True)
        else:
            flash('Invalid password. Please try again.')

    return render_template('login.html', show_register_button=False)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        location = request.form['location']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return render_template('register.html')

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.')
            return render_template('register.html')

        # Add the user to the database
        new_user = User(username=username, location=location)
        new_user.set_password(password)  # Hash and store password
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/main')
def main_page():
    if 'user_id' not in session:
        flash('You must log in to access this page.')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('main.html', username=user.username, location=user.location)



@app.route('/process_text', methods=['POST'])
def process_text():
    user_input = request.form['user_input']  # Get input text from the user
    
    # Process the text with your ML model
    output_text = classification(user_input)
    desc = describe_input(user_input)

    # Extract sub-locations (list of strings)
    sub_location_names = location(user_input)

    # Convert sub-location names to dictionaries with coordinates
    sub_locations = []
    for loc_name in sub_location_names:
        location_data = get_sub_locations(loc_name)  # Get coordinates
        if location_data:  # Add only if valid coordinates are returned
            sub_locations.append(location_data)

    # Save each location to the database if not already present
    for loc in sub_locations:
        existing_location = Locations.query.filter_by(
            name=loc['name'], latitude=loc['lat'], longitude=loc['lng']
        ).first()

        if not existing_location:  # Add only if the location doesn't already exist
            location_entry = Locations(
                name=loc['name'],
                latitude=loc['lat'],
                longitude=loc['lng']
            )
            db.session.add(location_entry)

    db.session.commit()

    # Return the processed class and description
    return {'Class': output_text, 'Description': desc, 'SubLocations': sub_locations}


# Helper function to extract sub-locations
geolocator = Nominatim(user_agent="location_extractor")

def get_sub_locations(location_name):
    """
    Convert a location name into geographical coordinates.

    :param location_name: The name of the location (e.g., "Beirut").
    :return: A dictionary with location details (name, lat, lng), or None if not found.
    """
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        # Geocode the location name
        location = geolocator.geocode(location_name)
        if location:
            return {
                "name": location_name,
                "lat": location.latitude,
                "lng": location.longitude,
            }
    except Exception as e:
        print(f"Error geocoding {location_name}: {e}")

    return None





@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    flash('You have been logged out.')
    return redirect(url_for('login'))

# Route for dashboard (placeholder)
@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"

@app.route('/')
def home():
    return redirect(url_for('main_page'))  # Redirect to the main page


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the necessary tables in the database
    app.run(debug=True)
