from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Pega a URL do banco no ambiente (Render define variável de ambiente DATABASE_URL)
database_url = os.environ.get("DATABASE_URL")

# Render pode enviar URL com prefixo postgres://, ajusta para postgresql:// para SQLAlchemy
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.title = data.get("title", task.title)
    task.done = data.get("done", task.done)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
