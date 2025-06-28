from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  
from werkzeug.security import generate_password_hash, check_password_hash  
from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy  
from flask_cors import CORS  
import os  

app = Flask(__name__)  
CORS(app)  

database_url = os.environ.get("DATABASE_URL")  
if not database_url:  
    database_url = "sqlite:///tasks.db"   

app.config["SQLALCHEMY_DATABASE_URI"] = database_url  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
app.config["JWT_SECRET_KEY"] = "991652"  

jwt = JWTManager(app)  
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

@app.route("/register", methods=["POST"]) 
def register(): 
    data = request.get_json()  
    username = data.get('username')  
    password = data.get('password')  

    if User.query.filter_by(username=username).first():  
        return jsonify({"msg": "Usuário já existe."}), 409  
    hashed_password = generate_password_hash(password)  
    new_user = User(username=username, password=hashed_password)  
    db.session.add(new_user)  
    db.session.commit()  
    return jsonify({"msg": "Usuário registrado!"}), 201

@app.route("/login", methods=["POST"])  
def login():  
    data = request.get_json()  
    username = data.get('username') 
    password = data.get('password')  

    user = User.query.filter_by(username=username).first()  

    if user and check_password_hash(user.password, password):  
        token = create_access_token(identity=user.id)  
        return jsonify(access_token=token), 200  

    return jsonify({"msg": "Credenciais inválidas"}), 401  

@app.route("/tasks", methods=["GET"])  
@jwt_required() 
def list_tasks():  
    user_id = get_jwt_identity()  
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([  
        {"id": task.id, "title": task.title, "done": task.done, "complete": task.complete}  
        for task in tasks  
    ])  

@app.route("/tasks", methods=["POST"])  
@jwt_required()  
def create_task():  
    data = request.get_json()  
    user_id = get_jwt_identity()  
    new_task = Task(title=data.get("title", ""), user_id=user_id)  
    db.session.add(new_task)  
    db.session.commit()  
    return jsonify({"id": new_task.id, "title": new_task.title, "done": new_task.done, "complete": new_task.complete}), 201  

@app.route("/tasks/<int:task_id>", methods=["PUT"])  
@jwt_required()  
def update_task(task_id):  
    task = Task.query.get(task_id)  
    if not task:  
        return jsonify({"error": "Tarefa não encontrada"}), 404  
    data = request.get_json()  
    task.title = data.get("title", task.title)  
    task.done = data.get("done", task.done)  
    db.session.commit()  
    return jsonify({"id": task.id, "title": task.title, "done": task.done, "complete": task.complete})  

@app.route("/complete/<int:task_id>", methods=["PUT"])  
@jwt_required()  
def complete_task(task_id):  
    task = Task.query.get(task_id)  
    if not task:  
        return jsonify({"error": "Tarefa não encontrada"}), 404  
    data = request.get_json()  
    task.complete = data.get("complete", task.complete)  
    db.session.commit()  
    return jsonify({"id": task.id, "title": task.title, "complete": task.complete})  

@app.route("/tasks/search", methods=["GET"])  
@jwt_required()  
def search_tasks():  
    query = request.args.get("q", "").lower()  
    results = Task.query.filter(Task.title.ilike(f"%{query}%")).all()  
    return jsonify([  
        {"id": task.id, "title": task.title, "done": task.done, "complete": task.complete}  
        for task in results  
    ])  

@app.route("/tasks/<int:task_id>", methods=["DELETE"])  
@jwt_required() 
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
    app.run(debug=True)
