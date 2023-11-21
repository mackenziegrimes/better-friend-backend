# better-friend
> Simple relationship tracking app to help you be a better friend. 

## Features
- Receive scheduled reminders to reconnect with friends or colleagues you haven't talked to in awhile
- Help remember upcoming events or life updates like birthdays, new jobs, or new family members with detailed note-taking
- Customize and prioritize the most important relationships to keep them healthy no matter the distance

## Stack
- Built on [Python Quart](https://quart.palletsprojects.com/en/latest/index.html) (async Flask) API framework 
- Hosted with [Google Cloud Platform](https://cloud.google.com) Firestore NoSQL document storage

## Routes
Simple CRUD operations (POST, GET, PATCH, DELETE) supported on all resources. 

#### `/users`
App users, with first and last name and email

#### `/users/:userId/persons`
All relationships saved by a specific user, with a customizable reminder frequency and organization by relationship type.

#### `/users/:userId/persons/:personId/connections`
Discrete connections made with a certain friend/family member/colleague, stamped by datetime and supporting customizable notes to remember important news or life updates.

## Install
### Prerequisites
- Python 3.9+
- docker CLI

### Create virtualenv
```
python3 -m venv .venv
```

### Activate it before installing dependencies
```
source .venv/bin/activate
```

### Install all dependencies
```
pip3 install -r requirements.txt
```

### Create .env file
To run locally, you will need access to a [Google Cloud Platform](https://cloud.google.com) Project with a Firestore database, and have the project's service credentials .json file locally (these files are not checked into Git of course). 
- See `/.env.example` for the expected environment variables.
- Further assistance available in GCP documentation for [setting up project authentication](https://cloud.google.com/firestore/docs/create-database-server-client-library)

_Future enhancement: docker-compose container to spin up Firestore instance locally for easier testing._

## Run
```
quart run
```

## Project Structure
### /docs
Exported Insomnia/Postman collection which has all the possible REST routes and the expected arguments for each.

### /src
#### app_wrapper.py
This is the main entry point of the API (after `/app.py`, which is just a requirement of Quart runtime and instantiates `AppWrapper` from this file). 

`AppWrapper` imports all runtime configurations from environment variables or a local `.env` file, then wires up all API routes to their handler Quart "Blueprints"/functions and begins fielding requests.

#### firestore.py
`Firestore` class handles Google Cloud Platform Firestore database connections as well as Model classes which codify data structure.

#### routes
Each subdirectory in this `routes` directory represents one high-level REST resource and contains all the business logic to do Create/Read/Update/Delete (CRUD) operations on that resource. 
- `/users`
- `/users/:userId/persons`
- `/users/:userId/persons/:personId/connections`

For example, `persons/index.py` fields the `/users/:userId/persons/...` route requests and any data operations performed on a `Person` object.
