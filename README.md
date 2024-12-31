<h1 align="center">ToDo List <img src="https://github.com/user-attachments/assets/b810adbb-ec82-47a5-93e7-e96d064f284c" alt="ToDo list icon" width="24" height="24"></h1>

The ToDo-List is a web-based application designed to help users efficiently manage their daily tasks. One of the main functionalities is the user management system (through login, registration and secure sessions), which allows each registered user to have a private task list. Once successfully logged in, user can view their list, add new tasks to it (by providing title, description or due date) and delete tasks they no longer need. The app also allows users to update the status of tasks, marking them as completed or pending, as well as changing task details completely. Additionally, the ToDo-List includes a search feature, enabling users to filter tasks by keywords, making it easy to locate specific item even in large lists. With its straightforward and user-friendly design, this project offers a comprehensive set of tools to efficiently manage tasks and enhance personal productivity.

<div align="center">
    <img src="https://github.com/user-attachments/assets/c251b202-82c5-44c7-bf11-70b62f6f7b7d" width="640" height="360" />
</div>

## Features

- User authentication with register and log in pages
- Task management with CRUD operations
- Search functionality by task name

## Technologies Used

- **Backend**: Python (Django)
- **Frontend**: HTML, CSS
- **Database**: SQLite

## Installation (on Windows)

1. Clone the repository
    ```bash
    git clone https://github.com/SwieciloM/ToDo-List.git
    cd ToDo-list
    ```
2. Create a virtual environment and activate it
    ```bash
    python -m venv .env
    .env\Scripts\activate
    ```
3. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Apply migrations to set up the database
    ```bash
    python manage.py migrate
    ```
5. Start the development server
    ```bash
    python manage.py runserver
    ```
6. Open the application in your browser at http://127.0.0.1:8000

## Usage

1. Register an account (or log in) to access your personal dashboard
2. Create new task with title and optional description, due date
3. Update task or mark it as completed
4. Delete task that is no longer needed

<div align="center">
    <img src="https://github.com/user-attachments/assets/cadd4443-36c2-41aa-aa90-e1eb6eefb269" width="350" height="325" />
</div>

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
