from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy  
from flask_cors import CORS  
import os  

app = Flask(__name__)  
CORS(app)
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    database_url = "sqlite:///tasks.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

db = SQLAlchemy(app)  

class User(db.Model):  
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(80), unique=True, nullable=False)  
    password = db.Column(db.String(120), nullable=False)    

class Task(db.Model):  
    __tablename__ = 'tasks'  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(200), nullable=False)  
    done = db.Column(db.Boolean, default=False)  
    complete = db.Column(db.Boolean, default=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

# Lista todas as tarefas (sem autenticação)
@app.route("/tasks", methods=["GET"])  
def list_tasks():  
    tasks = Task.query.all()
    return jsonify([  
        {"id": task.id, "title": task.title, "done": task.done, "complete": task.complete, "user_id": task.user_id}  
        for task in tasks  
    ])  

# Cria nova tarefa (sem autenticação)
@app.route("/tasks", methods=["POST"])  
def create_task():  
    data = request.get_json()  
    new_task = Task(title=data.get("title", ""), user_id=data.get("user_id", 0))  
    db.session.add(new_task)  
    db.session.commit()  
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done, "complete": new_task.complete}), 201  

# Atualiza tarefa (sem autenticação)
@app.route("/tasks/<int:task_id>", methods=["PUT"])  
def update_task(task_id):  
    task = Task.query.get(task_id)  
    if not task:  
        return jsonify({"error": "Tarefa não encontrada"}), 404  
    data = request.get_json()  
    task.title = data.get("title", task.title)  
    task.done = data.get("done", task.done)  
    db.session.commit()  
    return jsonify({"id": task.id, "title": task.title, "done": task.done, "complete": task.complete})  

# Marca tarefa como completa (sem autenticação)
@app.route("/complete/<int:task_id>", methods=["PUT"])  
def complete_task(task_id):  
    task = Task.query.get(task_id)  
    if not task:  
        return jsonify({"error": "Tarefa não encontrada"}), 404  
    data = request.get_json()  
    task.complete = data.get("complete", task.complete)  
    db.session.commit()  
    return jsonify({"id": task.id, "title": task.title, "complete": task.complete})  

# Busca tarefas por título (sem autenticação)
@app.route("/tasks/search", methods=["GET"])  
def search_tasks():  
    query = request.args.get("q", "").lower()  
    results = Task.query.filter(Task.title.ilike(f"%{query}%")).all()  
    return jsonify([  
        {"id": task.id, "title": task.title, "done": task.done, "complete": task.complete}  
        for task in results  
    ])  

# Deleta tarefa (sem autenticação)
@app.route("/tasks/<int:task_id>", methods=["DELETE"])  
def delete_task(task_id):  
    task = Task.query.get(task_id)  
    if not task:  
        return jsonify({"error": "Tarefa não encontrada"}), 404  
    db.session.delete(task)  
    db.session.commit()  
    return jsonify({"message": "Tarefa deletada com sucesso"})  

with app.app_context():  
    db.create_all()  

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000)
