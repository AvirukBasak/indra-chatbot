# Indra Chatbot Backend
- Auth API
  - Auth for frontend at `/auth`
- Chat room API
  - Naural text
  - Speech
  - MCQ responses
- Database
  - Auth
  - Docs
- RASA Link


## Gettig Started
Open this project root in Powershell and run
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```
You MUST use a virtual environment as we'll be installing an ungodly number of packages and dependencies.


## Install dependecies

### PIP
Run the following after activating your environment:
```
python setup.py
```

## Setting MongoDB URI
Create a `.env.local` inside this `server` directory and give it an entry in followong format
```
MONGODB_URI='mongodb+srv://<username>:<passswd>@<some_domain>/?retryWrites=true&w=majority'
```
You will find the above URI in MongoDB Atlas (you'll need to hunt a little for it or create a new cluster if you don't have one).


Alternatively, for local MongoDB server instance
```
MONGODB_URI='mongodb://127.0.0.1:27017'
```

**Note**: DO NOT use `0.0.0.0` for the IP address for MongoDB local server will refuse connections.


## API Documentation

### Overview

The Authentication API provides endpoints for user authentication and verification. It is designed to be used in a stateless backend system and involves two main operations: `AUTH` and `VERIFY`. The API is intended to secure user sessions and provides tokens for backend and frontend authentication.

Use Postman for testing.

### Endpoints

#### 1. Authentication (AUTH)

- **Description**: This operation is used for initial user authentication and is executed once only to signup or login the user.

- **Request Method**: POST

- **Request Endpoint**: `/auth`

- **Request Body (JSON)**:
  ```json
  {
    "op": "AUTH",
    "email": "user-mail",
    "passwd": "user-password"
  }
  ```

- **Response Body (JSON)**:
  ```json
  {
    "btoken": "token-to-use-in-backend",
    "ftoken": "token-to-save-in-frontend"
  }
  ```

- **Response Codes**:
  - 200 OK: Successful authentication
  - 401 Unauthorized: Authentication failed

- **Notes**:
  - The `btoken` is intended for backend use and remains unique for each user. This token should NEVER go to any frontend.
  - The `ftoken` should be saved in the frontend and will change on each new authentication.

#### 2. Verification (VERIFY)

- **Description**: This operation is used to validate the user during a session and can be executed multiple times.

- **Request Method**: POST

- **Request Endpoint**: `/verify`

- **Request Body (JSON)**:
  ```json
  {
    "op": "VERIFY",
    "ftoken": "token-to-save-in-frontend"
  }
  ```

- **Response Body (JSON)**:
  ```json
  {
    "email": "user-mail" or null,
    "btoken": "token-to-use-in-backend" or null
  }
  ```

- **Response Codes**:
  - 200 OK: User successfully verified
  - 401 Unauthorized: Verification failed

- **Notes**:
  - The `email` field will contain the user's email address if a valid user is found, or it will be null if the user is not found or verification fails.
  - The `btoken` will be provided if a valid user is found, otherwise, it will be null.

### API Error Codes
Here are the error codes that may be encountered when using the Authentication API:

- `post:missing_body`
- `post:missing_field_op`
- `post:invalid_op`
- `auth:missing_field_email`
- `auth:missing_field_passwd`
- `auth:incorrect_passwd`
- `verify:missing_field_ftoken`

### MongoDB Document Schema

The Authentication API relies on a MongoDB document schema to store user information. The schema is as follows:

```json
{
  "email": "string",
  "passwd": "string",
  "btoken": "string",
  "ftoken": ["string"]
}
```

- `email`: The user's email address.
- `passwd`: The user's password (hashed and securely stored).
- `btoken`: Is intended for backend use and remains unique for each user. This token should NEVER go to any frontend.
- `ftoken`: An array of tokens used for frontend verification (changes on each new authentication).

### Usage Guidelines

- Ensure that user passwords are securely hashed and stored.
- Safeguard the `btoken` value as they are crucial for user authentication.
- Use the `VERIFY` operation to validate users during their session.
- Handle authentication and verification errors gracefully, returning appropriate HTTP status codes.
