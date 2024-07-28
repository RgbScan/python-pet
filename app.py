from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

# Создание таблиц при инициализации приложения
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description')
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        task.done = not task.done
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
