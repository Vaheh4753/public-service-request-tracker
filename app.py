from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
	if 'user_id' not in session:
            return redirect(url_for('login'))
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists. Try logging in."

        # Create new user
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))  # or redirect to login page
    return render_template('register.html')


app.secret_key = '0a23b3d7f387290cfcb7485df06b04180482bc1d65ba2902609de12d3dbf9411'
  # Needed for session management

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('home'))  # or dashboard
        else:
            return "Invalid email or password"

    return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)
