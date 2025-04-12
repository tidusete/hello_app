# Hello App - API with PostgreSQL

## Project Overview

In this project, we are building a simple API application that performs read and write operations on a PostgreSQL database. For the initial implementation, I chose **Python** over **Go** due to my familiarity with Python. The goal was to keep the solution simple and efficient while focusing on providing a solid foundation for future scalability.

### Why Python?

Although **Go** would be a great choice for handling concurrency through goroutines in a more performant way, I opted for Python to leverage my existing expertise. This allows me to focus on the core functionality without spending additional time on learning Go.

For simplicity, I chose to implement synchronous calls in Python rather than exploring asynchronous approaches. This decision was made to keep the initial version of the app manageable and to avoid introducing unnecessary complexity.

### Database: PostgreSQL

The application uses **PostgreSQL** as the database. This choice was made for the following reasons:

- **Scalability**: Although the queries in the app are simple at the moment, PostgreSQL provides the flexibility to grow. As the project evolves, it will be easy to add more complex queries or establish relationships between different data entities.
- **Reliability**: PostgreSQL’s robust support for transactions ensures consistency and data integrity, making it an excellent choice for applications that require reliable data management.

### API Framework: FastAPI

To implement the API, I chose **FastAPI** due to its many benefits:

- It integrates seamlessly with Python type hints, improving code clarity and enabling automatic validation of request data.
- FastAPI provides high performance, making it well-suited for building APIs that need to handle high loads, all while maintaining excellent developer productivity.

### Enhancing Performance with Redis

In a production environment, I would introduce **Redis** to improve performance. Specifically, Redis can be used to cache results for frequently accessed queries, such as retrieving users who have a birthday today. This would reduce the number of database reads, thus improving response times and reducing load on the database.

By caching queries that are likely to be repeated within a short time frame (e.g., birthday-related data), we can enhance performance without compromising the system’s reliability.

### Considerations for Background Tasks and Queues

In scenarios where transactional consistency and immediate read-after-write results are critical, I prefer connecting directly to the database instead of using a queue system. This ensures that the data is immediately available after a successful write, avoiding potential consistency issues or delays.

However, as the project grows and more background tasks are required, introducing a message queue (e.g., RabbitMQ or Celery) could become a valuable addition. A queue system would allow us to offload non-critical tasks and enhance the scalability of the app.

![Flowchart - Frame 1.jpg](Hello%20App%20-%20API%20with%20PostgreSQL%201d377a16c0538076a0e1e1a51b0ed561/Flowchart_-_Frame_1.jpg)

## How to build the application yourself.

In case you want to start to develop locally, you will have to first create your virtual environment and install all the required libraries, launch a postgresql instance on docker and run the hello_app project.

In order to do it, you can do the following using the [uv](https://github.com/astral-sh/uv) package and project manager for python.

Run this command in order to create a `venv + install all the required libraries` 

```jsx
uv sync
source .venv/bin/activate
```

Now we will generate the file `.env` which will be used by your application whenever you are developing locally thanks to the library `dotenv`.

```
DATABASE_URL=postgresql://hello:secret@localhost:5432/hello
POSTGRES_DB=hello
POSTGRES_USER=hello
POSTGRES_PASSWORD=secret
```

Run the PostgreSQL Docker:

```jsx
docker run --name postgresdb \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_USER=hello \
  -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -p 5432:5432 \
  -d postgres:16
```

And after that we can already start developing on our Hello_APP locally with this command:

```jsx
fastapi dev app/main.py --host 0.0.0.0
```

## Using Docker compose

In case that you want to fully test your application on a container world, you will have to run a docker compose. This feature will allow you to test your application deployed on a container environment.

```jsx
docker compose up --build
```

TIP: If you just want to focus on docker compose you can run the following command:

`docker-compose up -d postgres`

And it will just start the PostgreSQL, allowing you to work directly from your IDE.

## Deploying on kubernetes

If you want to deploy directly on kubernetes you just have to connect to your cluster and launch the following command:

```jsx
kubectl -f gitops_repo/deployment.yml
```

Another strategy is to use helm because it allows you to modify some values:

```jsx
helm template hello-app ./deployment > output.yml
kubectl -f output.yml
```

Due to the nature of Kubernetes readiness and liveness probes, your application may encounter a CrashLoopBackOff if it is unable to connect to the database or may be automatically restarted if it enters a deadlock state. It is important to configure these probes properly to ensure early detection of issues and prevent unnecessary restarts, ensuring application availability and stability

## Pipeline Structure:

We will basically have 2 workflows. Development and releases.

For development we will launch all this jobs:

- Lint. (Run linters)
- Test (Run tests)
- Build-dev (Builds the image to dev registry)
- Deploy-dev (Optional Deploys to dev ) # not implemented
- Scan-image (Run scanners to check the code)

For Releases:

- Build-prod (Builds & push the image to prod registry)
- Update-gitops (Runs a template tooling like helm and pushes to the gitops repo)
- Test-gitops (Check the metrics defined on the system to ensure proper deployment)
- Promote_release (Promote the new version to other environments if Test-gitops OK)
- Rollback_release (Rollback the new version an ensure stability)

## Cloud Design TBD