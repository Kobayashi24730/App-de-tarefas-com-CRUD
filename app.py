from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Criação da tabela no primeiro acesso
@app.before_first_request
def create_tables():
    db.create_all()

# Rota GET - listar tarefas
@app.route('/tasks', methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

# Rota POST - adicionar tarefa
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201

# Rota PUT - atualizar tarefa
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done})

# Rota DELETE - remover tarefa
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa excluída"}), 200

# Início apenas para execução local
if __name__ == "__main__":
    app.run()
