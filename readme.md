# Base setup for fastapi

This is a base project for fast api it includes following features

## Features

- Authentication with JWT
- Authorization
- User / Role / Permission crud
- Custom logger
- Docker file

## Run Locally

Clone the project

```bash
  git clone https://github.com/habibqureshi/fastapi-base-setup.git
```

Go to the project directory

```bash
  cd fastApiBaseSetup
```

Python Version : `Python 3.X.X`
FastApi Version : `0.115.0`

Install dependencies

```bash
  pip install
```

Activate env

```bash
  source  env/bin/activate
```

Deactivate env

```bash
  deactivate
```

Start the server

```bash
  uvicorn main:app --reload --port 8000
```

SQL schema

```bash
 use base-setup.sql file
```

## Running on Docker

Build image

```bash
   docker build -t fastapibase .
```

Run container

```bash
  docker run -p 8000:8000 fastapibase
```

Run container in background

```bash
  docker run -d -p 8000:8000 fastapibase
```

Run container in background with env

```bash
  docker run -e VARIABLE=VALUE -d -p 8000:8000 fastapibase
```

## Custom logger output

![image](https://github.com/user-attachments/assets/add07161-523b-4969-8154-31c6cb421e97)

## Folder structure

![image](https://github.com/user-attachments/assets/090782e1-acc7-490b-9266-551b97c84884)

## Environment Variables

All environment variables are defined in config.py with default values. These variables will be exported and consistently used throughout the application. This approach eliminates the need to remember variable names and ensures uniformity across the app.

`OPEN_END_POINTS`

`JWT_SECRET_KEY`

`JWT_ALGORITHM`

`JWT_REFRESH_SECRET_KEY`

`DB_URL`

## Authors

- [@habibqureshi](https://github.com/habibqureshi)
