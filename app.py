from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # Corrigido: SQLAlchemy (não SQLALchemy)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# URL do banco PostgreSQL (exemplo: Render)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@host:porta/nome_do_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Corrigido

# Modelo de dados
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Corrigido: era Integer, agora String
    done = db.Column(db.Boolean, default=False)

# Criação da tabela no primeiro acesso
@app.before_first_request
def create_tables():
    db.create_all()  # Corrigido: faltavam parênteses

# Rota GET - listar tarefas
@app.route('/tasks', methods=["GET"])  # Corrigido: era @ap
def get_tasks():                       # Corrigido: nome errado
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

# Rota POST - adicionar tarefa
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()  # Corrigido: .get_json(), não request.json()
    task = Task(title=data["title"])  # Corrigido: "titile" e uso da variável correta
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201  # Corrigido: usava variáveis inexistentes

# Rota PUT - atualizar tarefa
@app.route("/tasks/<int:task_id>", methods=["PUT"])  # Corrigido: era "/task/"
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)  # Corrigido: era Tak
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404  # Corrigido: código 401 → 404
    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done})

# Rota DELETE - remover tarefa
@app.route("/tasks/<int:task_id>", methods=["DELETE"])  # Corrigido: era "/task/"
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa excluída"}), 200

# Iniciar servidor
if __name__ == "__main__":  # Corrigido: era ===
    app.run(debug=True)
