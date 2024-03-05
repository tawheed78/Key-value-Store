<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
  </a>

  <h3 align="center">Key Value Store</h3>

  <p align="center">
    This project implements a simple key-value store using FastAPI, Huey as a Redis queue, and Redis as the data store.
  </p></div>
<!-- ABOUT THE PROJECT -->

## Overview

The project consists of several components:

- FastAPI: Provides the REST API endpoints for interacting with the key-value store.
- Huey: Manages asynchronous task execution using Redis as a queue.
- Redis: Used as the data store for the key-value pairs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Prerequisites

Before running the project, ensure you have the following dependencies installed:

- Python 3.9 or higher
- Docker (optional, for running with Docker Compose)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-keyvalue-store.git
   cd fastapi-keyvalue-store

2. Create and activate a virtual environment:

   ```bash
    python3 -m venv venv
    source venv/bin/activate
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

   
## Running Locally

1. Make sure you have a Redis server running locally.
2. Start the FastAPI application:
   ```sh
   uvicorn main:app --reload
   ```
3. In another terminal, start the Huey consumer:
   ```sh
   python huey_consumer.py routers.data_router.huey -w 4
   ```
The FastAPI application should now be accessible at http://localhost:8000.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Running with Docker Compose

To run the application with Docker Compose:

1. Make sure you have Docker and Docker Compose installed.
2. Start the containers:
```sh
docker-compose up --build
```

The FastAPI application should now be accessible at http://localhost:8000.


## Usage
Once the application is running, you can interact with it using HTTP requests. Here are some example requests:

Get data by key:

```bash
curl http://localhost:8000/get-data?key=mykey
```

Store data:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "mykey", "value": "myvalue"}' http://localhost:8000/store-data
```

Update data:

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key": "mykey", "value": "newvalue"}' http://localhost:8000/update-data?key=mykey
```

Delete data:

```bash
curl -X DELETE http://localhost:8000/delete-data?key=mykey
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.
