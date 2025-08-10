import os
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345678"
Bootstrap5(app)


# CREATE DATABASE
# class Base(DeclarativeBase):
#     pass
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:02072023Lj.@localhost:5432/mi_app_db"
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)
#
# class Users(db.Model):
#     pass


@app.route('/')
def index():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("index.html")

@app.route('/planes')
def planes():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("pricing.html")

@app.route('/contacto')
def contacto():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("contact.html")

@app.route('/login')
def login():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        nombre = request.form.get('name')
        password = request.form.get('password')
        fecha = request.form.get('fecha')
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("dashboard.html")

@app.route('/cuenta')
def account():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("account.html")

@app.route('/movimientos')
def movimientos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("movimientos.html")

@app.route('/metas')
def metas():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("metas.html")

@app.route('/ingresos')
def ingresos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("ingresos.html")

@app.route('/egresos')
def egresos():
    # result = db.session.execute(db.select(BlogPost))
    #posts = result.scalars().all()
    return render_template("egresos.html")
if __name__ == "__main__":
    app.run(debug=True, port=5001)