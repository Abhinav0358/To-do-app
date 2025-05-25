from flask import Flask ,render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '1234'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.title}', '{self.date_created}')"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        todo_title = request.form.get('task')
        if todo_title:
            new_todo = Todo(title=todo_title)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please enter a todo title.', 'danger')
            return redirect(url_for('home'))
    else:
        todos=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.title = request.form.get('task')
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('update.html', task=todo)
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
