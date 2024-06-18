from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db
from models import User, Project, Task
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicjalizacja bazy danych
init_db()

# Strona główna - wyświetlanie listy projektów
@app.route('/')
def index():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Pobierz wszystkie projekty
    cursor.execute('SELECT * FROM project')
    projects_data = cursor.fetchall()

    projects = [Project(*project) for project in projects_data]

    conn.close()

    return render_template('index.html', projects=projects)

# Rejestracja użytkownika
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('projects.db')
        cursor = conn.cursor()

        # Dodanie nowego użytkownika do bazy danych
        cursor.execute('INSERT INTO user (email, username, password) VALUES (?, ?, ?)', (email, username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

# Logowanie użytkownika
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('projects.db')
        cursor = conn.cursor()

        # Znalezienie użytkownika w bazie danych
        cursor.execute('SELECT * FROM user WHERE username=?', (username,))
        user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[3], password):
            session['user_id'] = user_data[0]
            session['username'] = user_data[2]
            conn.close()
            return redirect(url_for('index'))

        conn.close()

    return render_template('login.html')

# Wylogowanie użytkownika
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Dodawanie projektu
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['due_date']

        conn = sqlite3.connect('projects.db')
        cursor = conn.cursor()

        # Dodaj nowy projekt do bazy danych
        cursor.execute('INSERT INTO project (name, description, due_date) VALUES (?, ?, ?)', (name, description, due_date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_project.html')

# Lista projektów
@app.route('/project_list')
def project_list():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Pobierz wszystkie projekty
    cursor.execute('SELECT * FROM project')
    projects_data = cursor.fetchall()

    projects = [Project(*project) for project in projects_data]

    conn.close()

    return render_template('project_list.html', projects=projects)

# Informacje o projekcie
@app.route('/project_info/<int:project_id>')
def project_info(project_id):
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Pobierz informacje o projekcie
    cursor.execute('SELECT * FROM project WHERE id=?', (project_id,))
    project_data = cursor.fetchone()

    if not project_data:
        conn.close()
        return 'Project not found', 404

    project = Project(*project_data)

    # Pobierz zadania dla tego projektu
    cursor.execute('SELECT * FROM task WHERE project_id=?', (project_id,))
    tasks_data = cursor.fetchall()
    tasks = [Task(*task[:6]) for task in tasks_data]

    # Pobierz członków projektu
    cursor.execute('''
        SELECT user.id, user.username FROM user
        JOIN project_member ON user.id = project_member.user_id
        WHERE project_member.project_id = ?
    ''', (project_id,))
    members = cursor.fetchall()

    conn.close()

    return render_template('project_info.html', project=project, tasks=tasks, members=members)

# Edycja projektu
@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        due_date = request.form['due_date']

        # Zaktualizuj dane projektu w bazie danych
        cursor.execute('UPDATE project SET name=?, description=?, due_date=? WHERE id=?', (name, description, due_date, project_id))
        conn.commit()

        conn.close()

        return redirect(url_for('project_info', project_id=project_id))

    # Pobierz dane projektu do formularza
    cursor.execute('SELECT * FROM project WHERE id=?', (project_id,))
    project_data = cursor.fetchone()

    if not project_data:
        conn.close()
        return 'Project not found', 404

    project = Project(*project_data)

    # Pobierz dostępnych użytkowników do przypisania do projektu
    cursor.execute('SELECT id, username FROM user')
    users = cursor.fetchall()

    # Pobierz członków projektu
    cursor.execute('''
        SELECT user.id, user.username FROM user
        JOIN project_member ON user.id = project_member.user_id
        WHERE project_member.project_id = ?
    ''', (project_id,))
    members = cursor.fetchall()

    # Pobierz zadania projektu
    cursor.execute('SELECT * FROM task WHERE project_id=?', (project_id,))
    tasks_data = cursor.fetchall()
    tasks = [Task(*task[:6]) for task in tasks_data]

    conn.close()

    return render_template('edit_project.html', project=project, users=users, members=members, tasks=tasks)

# Dodawanie członka do projektu
@app.route('/add_member/<int:project_id>', methods=['POST'])
def add_member(project_id):
    user_id = request.form['user_id']

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Dodaj członka do projektu
    cursor.execute('INSERT INTO project_member (project_id, user_id) VALUES (?, ?)', (project_id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('edit_project', project_id=project_id))

# Dodawanie zadania do projektu
@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    name = request.form['name']
    description = request.form['description']
    due_date = request.form['due_date']

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Dodaj nowe zadanie do bazy danych
    cursor.execute('INSERT INTO task (project_id, name, description, due_date) VALUES (?, ?, ?, ?)', (project_id, name, description, due_date))
    conn.commit()
    conn.close()

    return redirect(url_for('edit_project', project_id=project_id))

# Przypisanie zadania do użytkownika -- nieuzywwane
@app.route('/assign_task/<int:task_id>', methods=['POST'])
def assign_task(task_id):
    user_id = request.form['user_id']
    project_id = request.form['project_id']

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Przypisz użytkownika do zadania w bazie danych
    cursor.execute('INSERT INTO task_assignees (task_id, user_id) VALUES (?, ?)', (task_id, user_id))
    conn.commit()

    conn.close()

    # Przekieruj do strony z informacjami o projekcie
    return redirect(url_for('project_info', project_id=project_id))


if __name__ == '__main__':
    app.run(debug=True)
