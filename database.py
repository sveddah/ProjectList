import sqlite3

# Inicjalizacja połączenia z bazą danych
def init_db():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    # Utwórz tabele
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            due_date DATE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            due_date DATE NOT NULL,
            assigned_to INTEGER,
            status TEXT NOT NULL DEFAULT 'not started',
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (assigned_to) REFERENCES user(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_member (
            project_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (project_id, user_id),
            FOREIGN KEY (project_id) REFERENCES project(id),
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_assignees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(task_id) REFERENCES task(id),
            FOREIGN KEY(user_id) REFERENCES user(id)
)
    ''')
    

    conn.commit()
    conn.close()

# Usuń tabele (do debugowania)
def drop_db():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS user')
    cursor.execute('DROP TABLE IF EXISTS project')
    cursor.execute('DROP TABLE IF EXISTS task')
    cursor.execute('DROP TABLE IF EXISTS project_member')
    cursor.execute('DROP TABLE IF EXISTS task_assignees')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
