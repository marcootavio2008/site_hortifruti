from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pytz

tz = pytz.timezone("America/Sao_Paulo")
data_registro = datetime.now(tz)
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
    quantidade = db.Column(db.String, nullable=False)
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


@app.route('/registrar/<tipo>', methods=['GET', 'POST'])
def registrar(tipo):
    if request.method == 'POST':
        produto = request.form['produto']
        quantidade = request.form['quantidade']

        data_input = request.form.get('data_registro')

        if data_input:
            data_registro = datetime.fromisoformat(data_input)
        else:
            data_registro = datetime.now()

        registro = Registro(
            tipo=tipo,
            produto=produto,
            quantidade=quantidade,
            data_registro=data_registro
        )

        db.session.add(registro)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('registrar.html', tipo=tipo, now=datetime.now().strftime("%Y-%m-%dT%H:%M"))

@app.route("/registros")
def registros():
    dados = Registro.query.order_by(Registro.data_registro.desc()).all()
    for r in dados:
        r.data_registro_br = r.data_registro
    return render_template("registros.html", registros=dados)

if __name__ == "__main__":
    app.run(debug=True)
