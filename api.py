from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLALchemy
from flask_cors import CORS

app =Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@host:porta//home_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLALchemy(app)

class Task(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.Integer(200), nullable=False)
	done = db.Column(db.Boolean,default=False)
	
@app.before_first_request
def create_tables():
	db.create_all
	
@ap.route('/tasks', methods=["GET"])
def get_tesks():
	tasks = Task.query.all()
	return jsonify([{"id": t.id,"title": t.title,"done": t.done} for t in tasks])
	
@app.route("/tasks", methods=["POST"])
def add_task():
	data = request.json()
	task = Task(title=data["titile"])
	db.session.add(task)
	db.session.commit()
	return jsonify({"id": id,"title": title,"done": done}), 201

@app.route("/task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
	data = request.json()
	task = Tak.query.get(task_id)
	if not task:
		return jsonify({"error": "Tarefa nao encontrada"}), 401
	task.title = data.get("title", task.title)
	task.done = data.get("done", task.done)
	db.session.commit()
	return jsonify ({"id": task.id,"title": task.title,"done": task.done})
	
@app.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
	task= Task.query.get(task_id)
	if not task:
		return jsonify({"error": "Tarefa nao encontrada"}), 404
	db.session.delete(task)
	db.session.commit()
	return jsonify ({"message": "Tarefa excluida"}), 200
	
if __name__ === "__main__":
	app.run(debug=True)