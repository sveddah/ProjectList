document.addEventListener('DOMContentLoaded', function() {
    // Walidacja formularza dodania projektu
    const addProjectForm = document.querySelector('form[action="/add_project"]');
    if (addProjectForm) {
        addProjectForm.addEventListener('submit', function(event) {
            const name = addProjectForm.querySelector('input[name="name"]').value.trim();
            const dueDate = addProjectForm.querySelector('input[name="due_date"]').value;
            if (!name || !dueDate) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }

    // Walidacja formularza rejestracji
    const registerForm = document.querySelector('form[action="/register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const email = registerForm.querySelector('input[name="email"]').value.trim();
            const username = registerForm.querySelector('input[name="username"]').value.trim();
            const password = registerForm.querySelector('input[name="password"]').value;
            if (!email || !username || !password) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }

    // Walidacja formularza logowania
    const loginForm = document.querySelector('form[action="/login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const username = loginForm.querySelector('input[name="username"]').value.trim();
            const password = loginForm.querySelector('input[name="password"]').value;
            if (!username || !password) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }

    // Walidacja formularza edycji
    const editProjectForm = document.querySelector('form[action^="/edit_project"]');
    if (editProjectForm) {
        editProjectForm.addEventListener('submit', function(event) {
            const name = editProjectForm.querySelector('input[name="name"]').value.trim();
            const dueDate = editProjectForm.querySelector('input[name="due_date"]').value;
            if (!name || !dueDate) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }

    // Walidacja dodania zadania w edycji
    const addTaskForm = document.querySelector('form[action^="/add_task"]');
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', function(event) {
            const name = addTaskForm.querySelector('input[name="name"]').value.trim();
            if (!name) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }

    // Walidacja formularza edycji (zadanie)
    const editTaskForm = document.querySelector('form[action^="/edit_task"]');
    if (editTaskForm) {
        editTaskForm.addEventListener('submit', function(event) {
            const name = editTaskForm.querySelector('input[name="name"]').value.trim();
            if (!name) {
                alert('Please fill out all required fields.');
                event.preventDefault();
            }
        });
    }
});
