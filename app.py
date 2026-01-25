from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from zoneinfo import ZoneInfo

def para_brasil(dt_utc):
    return dt_utc.replace(tzinfo=ZoneInfo("UTC")) \
                 .astimezone(ZoneInfo("America/Sao_Paulo"))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(
    app,
    engine_options={
        "pool_pre_ping": True
    }
)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/apagar/<int:registro_id>", methods=["POST"])
def apagar(registro_id):
    registro = Registro.query.get_or_404(registro_id)

    db.session.delete(registro)
    db.session.commit()

    return redirect(url_for("registros"))


@app.route("/registrar/<tipo>", methods=["GET", "POST"])
def registrar(tipo):
    if request.method == "POST":
        produto = request.form["produto"]
        quantidade = float(request.form["quantidade"])

        registro = Registro(
            tipo=tipo,
            produto=produto,
            quantidade=quantidade
        )

        db.session.add(registro)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("registrar.html", tipo=tipo)

@app.route("/registros")
def registros():
    dados = Registro.query.order_by(Registro.data_registro.desc()).all()
    for r in dados:
        r.data_registro_br = para_brasil(r.data_registro)
    return render_template("registros.html", registros=dados)

if __name__ == "__main__":
    app.run(debug=True)
