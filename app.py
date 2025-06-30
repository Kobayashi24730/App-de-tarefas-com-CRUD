from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tabela associativa Task-Tag
task_tags = db.Table(
    "task_tags",
    db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, default=False)
    complete = db.Column(db.Boolean, default=False)
    tags = db.relationship("Tag", secondary=task_tags, backref=db.backref("tasks", lazy="dynamic"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "complete": self.complete,
            "tags": [tag.to_dict() for tag in self.tags]
        }

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

with app.app_context():
    db.create_all()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title")
    tag_names = data.get("tags", [])
    if not title:
        return jsonify({"error": "Title is required"}), 400

    tags = []
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)

    task = Task(title=title, tags=tags)
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

@app.route("/complete/<int:id>", methods=["PUT"])
def complete_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.complete = data.get("complete", task.complete)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
