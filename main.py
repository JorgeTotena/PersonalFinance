import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Date
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345678"
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
     pass
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:02072023Lj.@localhost:5432/app"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    birth_date: Mapped[str] = mapped_column(Date)

with app.app_context():
    db.create_all()




@app.route('/')
def index():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route('/planes')
def planes():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("pricing.html", logged_in=current_user.is_authenticated)

@app.route('/contacto')
def contacto():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("contact.html", logged_in=current_user.is_authenticated)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        nombre = request.form.get('name')
        password = request.form.get('password')
        fecha = request.form.get('fecha')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash("User is already registered")
            return redirect(url_for('login'))
        else:
            new_user = User(email=email, name=nombre,password=generate_password_hash(password,method='pbkdf2:sha256', salt_length=8),birth_date=fecha)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

    # Check stored password hash against entered password hashed.
        if not user:
            flash("Email incorrecto, intente de nuevo!.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Contraseña incorrecta, intente de nuevo.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template("login.html", logged_in=current_user.is_authenticated)



    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()

@app.route('/dashboard')
@login_required
def dashboard():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("dashboard.html", logged_in=current_user.is_authenticated)

@app.route('/cuenta')
def account():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("account.html", logged_in=current_user.is_authenticated)

@app.route('/movimientos')
def movimientos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("movimientos.html", logged_in=current_user.is_authenticated)

@app.route('/metas')
def metas():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("metas.html", logged_in=current_user.is_authenticated)

@app.route('/ingresos')
def ingresos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("ingresos.html", logged_in=current_user.is_authenticated)

@app.route('/egresos')
def egresos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("egresos.html", logged_in=current_user.is_authenticated)
if __name__ == "__main__":
    app.run(debug=True, port=5001)