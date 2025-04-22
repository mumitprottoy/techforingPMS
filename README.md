
# Project Management System API

This is a Project Management System (PMS) that allows teams to collaborate on projects. It provides API to manage users, projects, tasks, and comments. The API will be consumed by the front-end web application and mobile application.

This is developed using Django and Django REST Framework. It includes endpoints for user authentication, projects, tasks, and comments. The project uses SQLite as the database and runs locally on `localhost:8000` or `127.0.0.1:8000`.

[See project description](https://docs.google.com/document/d/1RpBGriJr0dwJHXsEg3_4j8q6HxwHsYcsH0dP5YyITv4/edit?usp=sharing)

## Prerequisites

Before you begin, ensure that you have the following installed on your local machine:

- Python (version 3.8 or higher)
- pip (Python package installer)

## Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the repository

```bash
https://github.com/mumitprottoy/techforingPMS.git
cd techforingPMS
```

### 2. Create a virtual environment

It's recommended to use a virtual environment to manage dependencies. You can create one by running the following commands:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

- On Windows:

```bash
.\venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install the required dependencies

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r "requirements.txt"
```

### 5. Apply migrations

Run the following command to apply database migrations and set up your SQLite database:

```bash
python manage.py migrate
```


### 6. Create a superuser (optional)

If you want to access the Django admin interface, you can create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set the username, email, and password.

### 7. Run the development server

Start the Django development server by running:

```bash
python manage.py runserver
```

This will start the server at `localhost:8000`. You should now be able to access the API at `http://localhost:8000/`.


Here's the API documentation in markdown format that you can add to your GitHub repository `README.md`:


# Project Management System API Documentation

This is a REST API for a Project Management System built using Django and Django REST Framework. The API allows users to manage projects, tasks, and comments efficiently.

## Database Schema

### Users Table
- **id**: Primary Key
- **username**: String (Unique)
- **email**: String (Unique)
- **password**: String
- **first_name**: String
- **last_name**: String
- **date_joined**: DateTime

### Projects Table
- **id**: Primary Key
- **name**: String
- **description**: Text
- **owner**: Foreign Key (to Users)
- **created_at**: DateTime

### Project Members Table
- **id**: Primary Key
- **project**: Foreign Key (to Projects)
- **user**: Foreign Key (to Users)
- **role**: String (Admin, Member)

### Tasks Table
- **id**: Primary Key
- **title**: String
- **description**: Text
- **status**: String (To Do, In Progress, Done)
- **priority**: String (Low, Medium, High)
- **assigned_to**: Foreign Key (to Users, nullable)
- **project**: Foreign Key (to Projects)
- **created_at**: DateTime
- **due_date**: DateTime

### Comments Table
- **id**: Primary Key
- **content**: Text
- **user**: Foreign Key (to Users)
- **task**: Foreign Key (to Tasks)
- **created_at**: DateTime

---

## API Endpoints

### Users

#### 1. Register User
- **Endpoint**: `POST /api/users/register/`
- **Description**: Create a new user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "date_joined": "datetime"
  }
  ```

#### 2. Login User
- **Endpoint**: `POST /api/users/login/`
- **Description**: Authenticate a user and return a token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "refresh_token": "string",
    "access_token": "string",
  }
  ```

#### 3. Get User Details
- **Endpoint**: `GET /api/users/{id}/`
- **Description**: Retrieve details of a specific user.
- **Response**:
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "date_joined": "datetime"
  }
  ```

#### 4. Update User
- **Endpoint**: `PUT /api/users/{id}/` or `PATCH /api/users/{id}/`
- **Description**: Update user details.
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```

#### 5. Delete User
- **Endpoint**: `DELETE /api/users/{id}/`
- **Description**: Delete a user account.

---

### Projects

#### 1. List Projects
- **Endpoint**: `GET /api/projects/`
- **Description**: Retrieve a list of all projects.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "string",
      "description": "string",
      "owner": "user_id",
      "created_at": "datetime"
    }
  ]
  ```

#### 2. Create Project
- **Endpoint**: `POST /api/projects/`
- **Description**: Create a new project.
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "owner": "user_id"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "owner": "user_id",
    "created_at": "datetime"
  }
  ```

#### 3. Retrieve Project
- **Endpoint**: `GET /api/projects/{id}/`
- **Description**: Retrieve details of a specific project.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "description": "string",
    "owner": "user_id",
    "created_at": "datetime"
  }
  ```

#### 4. Update Project
- **Endpoint**: `PUT /api/projects/{id}/` or `PATCH /api/projects/{id}/`
- **Description**: Update project details.
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "owner": "user_id"
  }
  ```

#### 5. Delete Project
- **Endpoint**: `DELETE /api/projects/{id}/`
- **Description**: Delete a project.

---

### Tasks

#### 1. List Tasks
- **Endpoint**: `GET /api/projects/{project_id}/tasks/`
- **Description**: Retrieve a list of all tasks in a project.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "status": "To Do",
      "priority": "Medium",
      "assigned_to": "user_id",
      "project": "project_id",
      "created_at": "datetime",
      "due_date": "datetime"
    }
  ]
  ```

#### 2. Create Task
- **Endpoint**: `POST /api/projects/{project_id}/tasks/`
- **Description**: Create a new task in a project.
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "status": "To Do",
    "priority": "Medium",
    "assigned_to": "user_id",
    "due_date": "datetime"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "string",
    "description": "string",
    "status": "To Do",
    "priority": "Medium",
    "assigned_to": "user_id",
    "project": "project_id",
    "created_at": "datetime",
    "due_date": "datetime"
  }
  ```

#### 3. Retrieve Task
- **Endpoint**: `GET /api/tasks/{id}/`
- **Description**: Retrieve details of a specific task.
- **Response**:
  ```json
  {
    "id": 1,
    "title": "string",
    "description": "string",
    "status": "To Do",
    "priority": "Medium",
    "assigned_to": "user_id",
    "project": "project_id",
    "created_at": "datetime",
    "due_date": "datetime"
  }
  ```

#### 4. Update Task
- **Endpoint**: `PUT /api/tasks/{id}/` or `PATCH /api/tasks/{id}/`
- **Description**: Update task details.
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "status": "To Do",
    "priority": "Medium",
    "assigned_to": "user_id",
    "due_date": "datetime"
  }
  ```

#### 5. Delete Task
- **Endpoint**: `DELETE /api/tasks/{id}/`
- **Description**: Delete a task.

---

### Comments

#### 1. List Comments
- **Endpoint**: `GET /api/tasks/{task_id}/comments/`
- **Description**: Retrieve a list of all comments on a task.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "content": "string",
      "user": "user_id",
      "task": "task_id",
      "created_at": "datetime"
    }
  ]
  ```

#### 2. Create Comment
- **Endpoint**: `POST /api/tasks/{task_id}/comments/`
- **Description**: Create a new comment on a task.
- **Request Body**:
  ```json
  {
    "content": "string",
    "user": "user_id"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "content": "string",
    "user": "user_id",
    "task": "task_id",
    "created_at": "datetime"
  }
  ```

#### 3. Retrieve Comment
- **Endpoint**: `GET /api/comments/{id}/`
- **Description**: Retrieve details of a specific comment.
- **Response**:
  ```json
  {
    "id": 1,
    "content": "string",
    "user": "user_id",
    "task": "task_id",
    "created_at": "datetime"
  }
  ```

#### 4. Update Comment
- **Endpoint**: `PUT /api/comments/{id}/` or `PATCH /api/comments/{id}/`
- **Description**: Update comment details.
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```

#### 5. Delete Comment
- **Endpoint**: `DELETE /api/comments/{id}/`
- **Description**: Delete a comment.

