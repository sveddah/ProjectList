class User:
    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

class Project:
    def __init__(self, id, name, description, due_date):
        self.id = id
        self.name = name
        self.description = description
        self.due_date = due_date

class Task:
    def __init__(self, id, project_id, name, description, due_date, status):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.status = status

