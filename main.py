import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime, date
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Date, Float, ForeignKey, func
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
    categorias: Mapped[list["Categorias"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Income(UserMixin, db.Model):
    __tablename__ = 'income'
    income_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categories_id: Mapped[int] = mapped_column(ForeignKey("categorias.id", ondelete="CASCADE"))
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
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    nombre: Mapped[str] = mapped_column(String(1000), unique=True)
    tipo: Mapped[str] = mapped_column(String(10))
    fecha_creacion: Mapped[str] = mapped_column(Date)
    incomes: Mapped[list["Income"]] = relationship(back_populates="categorias", cascade="all, delete-orphan")
    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="categorias", cascade="all, delete-orphan")
    user: Mapped["User"] = relationship(back_populates="categorias")

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
    #db.drop_all()
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
    total_ingresos = db.session.execute(db.select(func.sum(Income.monto))).scalar()
    total_egresos = db.session.execute(db.select(func.sum(Outcome.monto))).scalar()
    gastos_categoria = db.session.execute(
        db.select(
            Categorias.nombre,
            func.sum(Outcome.monto).label('total_monto')
        )
        .join(Categorias)
        .group_by(Categorias.nombre)
        .order_by(Categorias.nombre)
    ).all()
    print(gastos_categoria)
    descripciones = []
    montos = []
    for categoria in gastos_categoria:
        categoria = categoria[0]
        descripciones.append(categoria)
    for monto in gastos_categoria:
        monto = monto[1]
        montos.append(monto)

    print(descripciones)
    print(montos)

    if total_ingresos is None:
        total_ingresos = 0
    if total_egresos is None:
        total_egresos = 0
    return render_template("dashboard.html", logged_in=current_user.is_authenticated, total=total_ingresos, total_egresos=total_egresos, gastos_categoria=gastos_categoria, descripciones=descripciones, montos=montos)

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
    ingresos = db.session.execute(db.select(Income).order_by(Income.fecha_creacion)).scalars().all()
    egresos = db.session.execute(db.select(Outcome).order_by(Outcome.fecha_creacion)).scalars().all()
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("movimientos.html", logged_in=current_user.is_authenticated, ingresos=ingresos, egresos=egresos)

@app.route('/metas')
@login_required
def metas():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("metas.html", logged_in=current_user.is_authenticated)

@app.route('/nueva_meta', methods=["GET", "POST"])
@login_required
def nueva_meta():
    if request.method == "POST":
        user_id = current_user.id
        descripcion = request.form.get("descripcion")
        monto_final_str = request.form.get("ahorro_potencial")
        monto_actual_str = request.form.get("ahorro_real")
        fecha_creacion_str = request.form.get("fecha_creacion")
        fecha_programada_str = request.form.get("fecha_programada")

        # --- Validaciones de campos (IMPORTANTE: devolver jsonify en errores) ---
        if not descripcion or not monto_final_str or not monto_actual_str or not fecha_creacion_str or not fecha_programada_str:
            return jsonify({"success": False, "message": "Todos los campos son obligatorios."}), 400

        try:
            monto_final = float(monto_final_str)
            monto_actual = float(monto_actual_str)
            if monto_final <= 0:
                return jsonify({"success": False, "message": "El monto objetivo debe ser positivo."}), 400
            if monto_actual < 0:
                return jsonify({"success": False, "message": "El ahorro actual no puede ser negativo."}), 400
            if monto_actual > monto_final:
                return jsonify({"success": False, "message": "El ahorro actual no puede ser mayor que el monto objetivo."}), 400

            fecha_creacion = datetime.strptime(fecha_creacion_str, '%Y-%m-%d').date()
            fecha_programada = datetime.strptime(fecha_programada_str, '%Y-%m-%d').date()

            if fecha_programada < fecha_creacion:
                return jsonify({"success": False, "message": "La fecha límite no puede ser anterior a la fecha de creación."}), 400

        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Formato de monto o fecha inválido."}), 400

        # --- Lógica de límite de metas (si aplica, también con jsonify) ---
        # Ejemplo: Si tienes un límite de 3 metas para el plan gratuito
        limite_metas_gratuitas = 3
        current_metas = db.session.execute(
            db.select(Metas).where(Metas.user_id == current_user.id)
        ).scalars().all()
        current_metas_count = len(current_metas)
        if current_metas_count >= limite_metas_gratuitas:
            return jsonify({"success": False, "message": f"Has alcanzado el límite de {limite_metas_gratuitas} metas. Pásate a Premium para crear metas ilimitadas!"}), 403 # 403 Forbidden

        # --- Si todo es válido, crear y guardar la meta ---
        try:
            new_meta = Metas(
                user_id=user_id,
                descripcion=descripcion,
                fecha_creacion=fecha_creacion,
                fecha_programada=fecha_programada,
                ahorro_actual=monto_actual,
                ahorro_potencial=monto_final
            )
            db.session.add(new_meta)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Meta agregada con éxito!",
                "category": { # 'category' es un nombre un poco confuso aquí, podrías usar 'meta'
                    "id": new_meta.meta_id,
                    "nombre": new_meta.descripcion,
                    "fecha_programada": new_meta.fecha_programada.strftime('%Y-%m-%d') # Formatear para JSON
                }
            }), 201 # 201 Created
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Error interno al guardar la meta: {str(e)}"}), 500

    return render_template("nueva_meta.html", logged_in=current_user.is_authenticated)



# @app.route('/nueva_meta', methods=["GET", "POST"])
# @login_required
# def nueva_meta():
#     # result = db.session.execute(db.select(BlogPost))
#     #posts = result.scalars().all()
#     if request.method == "POST":
#         user_id = current_user.id
#         descripcion = request.form.get("descripcion")
#         monto_final = request.form.get("ahorro_potencial")
#         monto_actual = request.form.get("ahorro_real")
#         fecha = request.form.get("fecha_creacion")
#         fecha_programada = request.form.get("fecha_programada")
#         new_meta = Metas(user_id=user_id,descripcion=descripcion, fecha_creacion=fecha, fecha_programada=fecha_programada,
#                          ahorro_actual=monto_actual, ahorro_potencial=monto_final)
#         db.session.add(new_meta)
#         db.session.commit()
#         return jsonify({
#             "success": True,
#             "message": "Meta agregada con exito!",
#             "category": {
#                 "id": new_meta.meta_id,
#                 "nombre": new_meta.descripcion,
#                 "fecha programada": new_meta.fecha_programada
#             }
#         }), 201
#     return render_template("nueva_meta.html", logged_in=current_user.is_authenticated)
#


@app.route('/ingresos', methods=["GET", "POST"])
@login_required
def ingresos():
    categorias = db.session.execute(
    db.select(Categorias).where(Categorias.tipo == "Ingreso").order_by(Categorias.nombre)).scalars().all()
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
        return redirect(url_for("movimientos"))
    return render_template("ingresos.html", logged_in=current_user.is_authenticated, categorias=categorias,)


# --- RUTA DE CATEGORÍAS DE INGRESOS (AJAX) ---
@app.route('/categorias_ingresos', methods=["POST"])
@login_required
def categorias_ingresos():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if not nombre or nombre.strip() == "":
            return jsonify({"success": False, "message": "El nombre de la categoría es requerido."}), 400

        try:
            fecha_creacion = date.today()
            tipo = "Ingreso"

            # Verificar si ya existe una categoría con ese nombre para este usuario y tipo
            existing_category = db.session.execute(
                db.select(Categorias).where(
                    Categorias.user_id == current_user.id,
                    Categorias.nombre == nombre,
                    Categorias.tipo == tipo
                )
            ).scalar()

            if existing_category:
                return jsonify({"success": False, "message": f"La categoría '{nombre}' ya existe para ingresos."}), 409

            new_category = Categorias(
                user_id=current_user.id,
                nombre=nombre,
                fecha_creacion=fecha_creacion,
                tipo=tipo
            )
            db.session.add(new_category)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Categoría de ingreso añadida con éxito!",
                "category": {
                    "id": new_category.id,
                    "nombre": new_category.nombre,
                    "tipo": new_category.tipo
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Error al añadir la categoría de ingreso: {str(e)}"}), 500
    return jsonify({"success": False, "message": "Método no permitido para esta operación."}), 405



@app.route('/egresos', methods=["GET", "POST"])
@login_required
def egresos():
    categorias = db.session.execute(
    db.select(Categorias).where(Categorias.tipo == "Egreso").order_by(Categorias.nombre)).scalars().all()
    if request.method == "POST":
        user_id = current_user.id
        monto = request.form.get("monto")
        descripcion = request.form.get("descripcion")
        fecha = request.form.get("fecha")
        categoria = db.session.execute(db.select(Categorias).where(Categorias.nombre == request.form.get("categoria"))).scalar()
        new_outcome = Outcome(user_id=user_id, monto=monto, descripcion=descripcion,
                            fecha_creacion=fecha,
                            categorias=categoria)
        db.session.add(new_outcome)
        db.session.commit()
        return redirect(url_for("movimientos"))
    return render_template("egresos.html", logged_in=current_user.is_authenticated, categorias=categorias)


# --- RUTA DE CATEGORÍAS DE EGRESOS (AJAX) ---
@app.route('/categorias_egresos', methods=["POST"])  # Solo POST para añadir via AJAX
@login_required
def categorias_egresos():
    # No necesitamos lógica GET aquí si esta ruta es solo para el modal AJAX POST.
    # Si quieres que /categorias_egresos cargue una página, haz otra ruta o maneja el GET.
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if not nombre or nombre.strip() == "":
            return jsonify({"success": False, "message": "El nombre de la categoría es requerido."}), 400

        try:
            fecha_creacion = date.today()  # Usar date.today() para Mapped[Date]
            tipo = "Egreso"

            # Verificar si ya existe una categoría con ese nombre para este usuario y tipo
            existing_category = db.session.execute(
                db.select(Categorias).where(
                    Categorias.user_id == current_user.id,
                    Categorias.nombre == nombre,
                    Categorias.tipo == tipo
                )
            ).scalar()

            if existing_category:
                return jsonify({"success": False, "message": f"La categoría '{nombre}' ya existe para egresos."}), 409

            new_category = Categorias(
                user_id=current_user.id,
                nombre=nombre,
                fecha_creacion=fecha_creacion,
                tipo=tipo
            )
            db.session.add(new_category)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Categoría de egreso añadida con éxito!",
                "category": {
                    "id": new_category.id,
                    "nombre": new_category.nombre,
                    "tipo": new_category.tipo
                }
            }), 201  # Created

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Error al añadir la categoría de egreso: {str(e)}"}), 500

    # Esta ruta NO DEBERÍA SER LLAMADA con GET por el modal.
    # Si esta ruta es solo para AJAX, considera eliminar el 'GET' de methods=["GET", "POST"]
    # y si alguien accede directamente con GET, podrías devolver un error 405.
    return jsonify({"success": False, "message": "Método no permitido para esta operación."}), 405

@app.route("/categorias/eliminar/<int:category_id>", methods=["DELETE"])
@login_required
def delete_category(category_id):
    category_to_delete = db.session.execute(
        db.select(Categorias).where(
            Categorias.id == category_id,
            Categorias.user_id == current_user.id  # Importante: Seguridad
        )
    ).scalar()

    if not category_to_delete:
        return jsonify(
            {"success": False, "message": "Categoría no encontrada o no tienes permiso para eliminarla."}), 404

    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        return jsonify({"success": True, "message": "Categoría eliminada con éxito."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al eliminar la categoría: {e}"}), 500
    return redirect(url_for("home"))
    return render_template("ingresos.html", logged_in=current_user.is_authenticated)

if __name__ == "__main__":
    app.run(debug=True, port=5001)