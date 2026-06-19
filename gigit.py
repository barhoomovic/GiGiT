# This is a sample Python script.
from flask import Flask, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from model import db, User, Gig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gigit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# -------------------------
# HOME PAGE
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------------
# LOGIN PAGE
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template('login.html', error="User not found")

        if not check_password_hash(user.password, password):
            return render_template('login.html', error="Incorrect password")

        return redirect('/find_gigs')

    return render_template('login.html')


# -------------------------
# REGISTER PAGE
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# -------------------------
# FIND GIGS + MUSICIANS
# -------------------------
@app.route('/find_gigs')
def find_gigs():
    gigs = Gig.query.all()
    musicians = User.query.filter_by(role='musician').all()
    return render_template('find_gigs.html', gigs=gigs, musicians=musicians)

@app.route('/upload_gig', methods=['GET', 'POST'])
def upload_gig():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        location = request.form['location']
        posted_by = request.form['posted_by']

        new_gig = Gig(
            title=title,
            description=description,
            date=date,
            location=location,
            posted_by=posted_by
        )

        db.session.add(new_gig)
        db.session.commit()

        return redirect('/find_gigs')

    return render_template('upload_gig.html')

@app.route('/map')
def map_page():
    users = User.query.all()

    # Convert each user to a dictionary
    user_data = []
    for user in users:
        user_data.append({
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "location": user.location,
            "latitude": getattr(user, "latitude", None),
            "longitude": getattr(user, "longitude", None)
        })

    return render_template("map.html", users=user_data)

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
