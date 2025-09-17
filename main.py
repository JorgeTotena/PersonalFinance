import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Date, Float, ForeignKey
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
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    birth_date: Mapped[str] = mapped_column(Date)
    incomes: Mapped[list["Income"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    metas: Mapped[list["Metas"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reportes: Mapped[list["Reportes"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Income(UserMixin, db.Model):
    __tablename__ = 'income'
    income_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categories_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    monto: Mapped[Float] = mapped_column(Float)
    descripcion: Mapped[str] = mapped_column(String(1000))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    user: Mapped["User"] = relationship(back_populates="incomes")
    categorias: Mapped["Categorias"] = relationship(back_populates="incomes")


class Outcome(UserMixin, db.Model):
    __tablename__ = 'outcome'
    outcome_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categories_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    monto: Mapped[float] = mapped_column(Float)
    descripcion: Mapped[str] = mapped_column(String(1000))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    user: Mapped["User"] = relationship(back_populates="outcomes")
    categorias: Mapped["Categorias"] = relationship(back_populates="outcomes")


class Metas(UserMixin, db.Model):
    __tablename__ = 'metas'
    meta_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    descripcion: Mapped[str] = mapped_column(String(1000))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    fecha_programada: Mapped[str] = mapped_column(Date)
    ahorro_actual: Mapped[float] = mapped_column(Float)
    ahorro_potencial: Mapped[float] = mapped_column(Float)
    user: Mapped["User"] = relationship(back_populates="metas")

class Categorias(UserMixin, db.Model):
    __tablename__ = 'categorias'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(1000))
    tipo: Mapped[str] = mapped_column(String(10))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    incomes: Mapped[list["Income"]] = relationship(back_populates="categorias", cascade="all, delete-orphan")
    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="categorias", cascade="all, delete-orphan")

class Reportes(UserMixin, db.Model):
    __tablename__ = 'reportes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    periodo_inicio: Mapped[str] = mapped_column(Date)
    periodo_fin: Mapped[str] = mapped_column(Date)
    total_ingresos: Mapped[float] = mapped_column(Float)
    total_egresos: Mapped[float] = mapped_column(Float)
    saldo_neto: Mapped[float] = mapped_column(Float)
    descripcion: Mapped[str] = mapped_column(String(1000))
    user: Mapped["User"] = relationship(back_populates="reportes")




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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()

@app.route('/dashboard')
@login_required
def dashboard():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("dashboard.html", logged_in=current_user.is_authenticated)

@app.route('/cuenta', methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        current_password = request.form.get("currentPassword")
        email = request.form.get('email')
        new_password = request.form.get('newPassword')
        user = db.session.execute(db.select(User).where(User.email == current_user.email)).scalar()
        if not check_password_hash(user.password, current_password):
            flash("La contraseña actual es incorrecta. Inténtalo de nuevo.", "danger")
            return redirect(url_for('account'))
        hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        user.password = hashed_new_password
        db.session.commit()

        flash("¡Contraseña actualizada con éxito!", "success")
        return redirect(url_for('account'))
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("account.html", logged_in=current_user.is_authenticated)

@app.route('/edit_account', methods=["GET", "POST"])
@login_required
def edit_account():
    if request.method == "POST":
        email = request.form.get('email')
        nombre = request.form.get('name')
        fecha = request.form.get('fecha')
        user = db.session.execute(db.select(User).where(User.email == current_user.email)).scalar()
        user.name = nombre
        user.birth_date = fecha
        db.session.commit()
        return(redirect(url_for("account")))
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("edit_account.html", logged_in=current_user.is_authenticated)

@app.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        email = request.form.get('email')
        user = db.session.execute(db.select(User).where(User.email == current_user.email)).scalar()
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for("index"))
    return render_template("account.html", logged_in=current_user.is_authenticated)

@app.route('/movimientos')
@login_required
def movimientos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("movimientos.html", logged_in=current_user.is_authenticated)

@app.route('/metas')
@login_required
def metas():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("metas.html", logged_in=current_user.is_authenticated)

@app.route('/ingresos', methods=["GET", "POST"])
@login_required
def ingresos():
    if request.method == "POST":
        user_id = current_user.id
        monto = request.form.get("monto")
        descripcion = request.form.get("descripcion")
        fecha  = request.form.get("fecha")
        categoria = db.session.execute(db.select(Categorias).where(Categorias.nombre == request.form.get("categoria"))).scalar()
        new_income = Income(user_id =user_id, monto=monto, descripcion=descripcion,
                        fecha_creacion=fecha,
                        categorias=categoria)
        db.session.add(new_income)
        db.session.commit()
    return render_template("ingresos.html", logged_in=current_user.is_authenticated)

@app.route('/egresos')
@login_required
def egresos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("egresos.html", logged_in=current_user.is_authenticated)
if __name__ == "__main__":
    app.run(debug=True, port=5001)