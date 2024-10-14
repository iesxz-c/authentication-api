```markdown
# FastAPI Authentication API

This is a simple authentication API built with FastAPI and SQLModel.

## Features

- User registration and authentication using JWT tokens.
- Secure password storage.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite (default database)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akashkrishnan02/authentication-api.git
   cd authentication-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the server:
```bash
python -m uvicorn app.main:app --reload
```

Access the API at `http://127.0.0.1:8000`.

## API Endpoints

- **Register User**: `POST /register/`
  - **Request Body:**
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string"
    }
    ```
  - **Response:**
    - **201 Created** if registration is successful.
    - **422 Unprocessable Entity** if validation fails.

- **Login User**: `POST /login/`
  - **Request Body:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response:**
    - **200 OK**
      ```json
      {
        "access_token": "your_access_token",
        "token_type": "bearer"
      }
      ```
    - **422 Unprocessable Entity** if validation fails.

- **Get Current User**: `GET /users/me/`
  - **Headers:**
    - `Authorization: Bearer <your_access_token>`
  - **Response:**
    - **200 OK** with user details.
    - **401 Unauthorized** if not authenticated.

- **Root**: `GET /`
  - **Response:**
    - **200 OK**
      ```json
      {
        "message": "FastAPI Auth App Running"
      }
      ```

## Contributing

Feel free to open issues or submit pull requests!

## License

This project is licensed under the MIT License.
```

This version includes the registration endpoint and its details. Let me know if you need any more changes!
