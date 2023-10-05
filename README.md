# Indra Chatbot
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
- React Frontend


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

- [Auth](#auth)
- [Chat](#chat)
- [Rasa](#rasa)
