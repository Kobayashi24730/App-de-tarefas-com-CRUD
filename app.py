from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# URL do banco de dados
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    database_url = "sqlite:///tasks.db"  # fallback local

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de tarefa
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Rota para listar todas as tarefas
@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": task.id, "title": task.title, "done": task.done}
        for task in tasks
    ])

# Rota para criar nova tarefa
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data.get("title", ""))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done}), 201

# Rota para atualizar uma tarefa
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done})

# Rota para deletar uma tarefa
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa deletada com sucesso"})

# Cria as tabelas manualmente ao iniciar
with app.app_context():
    db.create_all()

# Roda localmente
if __name__ == "__main__":
    app.run(debug=True)
