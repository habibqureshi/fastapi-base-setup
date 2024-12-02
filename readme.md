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

## Authors

- [@habibqureshi](https://github.com/habibqureshi)
