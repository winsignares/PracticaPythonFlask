from flask import Flask,render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# settings
app.secret_key = "mysecretkey"

#trabajamos con la bd 
db = SQLAlchemy(app)

ma = Marshmallow(app)

#creamos el modelo en la base de dato
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
#terminamos la conexion y los modelos

#ahora definimos las rutas
@app.route('/tasks', methods=['Post'])
def create_task():
  title = request.json['title']
  description = request.json['description']

  new_task= Task(title, description)

  db.session.add(new_task)
  db.session.commit()

  return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)

  title = request.json['title']
  description = request.json['description']

  task.title = title
  task.description = description

  db.session.commit()

  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task)


@app.route('/', methods=['GET'])
def index():
   
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    #return jsonify(result)
    return render_template('index.html', contacts = result)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        new_task= Task(title, description)

        db.session.add(new_task)
        db.session.commit()
        flash('Contact Added successfully')
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_task2(id):
    if request.method == 'GET':
      task = Task.query.get(id)
      
      return render_template('edit-contact.html', contact = task)

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        task = Task.query.get(id)

        task.title = title
        task.description = description

        db.session.commit()
        
        flash('Contact Updated Successfully')
       
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
