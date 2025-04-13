# Hello App - API with PostgreSQL

## Purpose

Hello App is a simple REST API designed to store users names and dates of birth, and return personalized birthday messages. The API supports two main operations:

- Save/Update a User's Date of Birth
    - Request: `PUT /hello/<username>`
    - Body: `{ "dateOfBirth": "YYYY-MM-DD" }`
    - Response: `204 No Content`
    - Validation:
        - `<username>` must only contain alphabetic characters.
        - `dateOfBirth` must be a date prior to today.
- Retrieve a Birthday Message
    - Request: `GET /hello/<username>`
    - Response: `200 OK`
    - Examples:
        - If the user's birthday is today:
            
            ```json
            { "message": "Hello, <username>! Happy birthday!" }
            ```
            
        - If the user's birthday is in N days:
            
            ```json
            { "message": "Hello, <username>! Your birthday is in N day(s)" }
            ```
            

The application uses a storage backend (PostgreSQL) to persist user data.

## Project Overview

In this project, we are building a simple API application that performs read and write operations on a PostgreSQL database. For the initial implementation, I chose Python over Go due to my familiarity with Python. The goal was to keep the solution simple and efficient while focusing on providing a solid foundation for future scalability.

### Why Python?

Although Go would be a great choice for handling concurrency through goroutines in a more performant way, I opted for Python to leverage my existing expertise. This allows me to focus on the core functionality without spending additional time on learning Go.

For simplicity, I chose to implement synchronous calls in Python rather than exploring asynchronous approaches. This decision was made to keep the initial version of the app manageable and to avoid introducing unnecessary complexity.

### Database: PostgreSQL

The application uses PostgreSQL as the database. This choice was made for the following reasons:

- Scalability: Although the queries in the app are simple at the moment, PostgreSQL provides the flexibility to grow. As the project evolves, it will be easy to add more complex queries or establish relationships between different data entities.
- Reliability: PostgreSQL’s robust support for transactions ensures consistency and data integrity, making it an excellent choice for applications that require reliable data management.

### API Framework: FastAPI

To implement the API, I chose FastAPI due to its many benefits:

- It integrates seamlessly with Python type hints, improving code clarity and enabling automatic validation of request data.
- FastAPI provides high performance, making it well-suited for building APIs that need to handle high loads, all while maintaining excellent developer productivity.
- It automatically generates OpenAPI-compliant interactive documentation (Swagger UI), which is extremely useful for quickly testing and visualizing API endpoints during development and debugging.

### Enhancing Performance with Redis

In a production environment, I would introduce Redis to improve performance. Specifically, Redis can be used to cache results for frequently accessed queries, such as retrieving users who have a birthday today. This would reduce the number of database reads, thus improving response times and reducing load on the database.

By caching queries that are likely to be repeated within a short time frame (e.g., birthday-related data), we can enhance performance without compromising the system’s reliability.

### Considerations for Background Tasks and Queues

In scenarios where transactional consistency and immediate read-after-write results are critical, I prefer connecting directly to the database instead of using a queue system. This ensures that the data is immediately available after a successful write, avoiding potential consistency issues or delays.

However, as the project grows and more background tasks are required, introducing a message queue (e.g., RabbitMQ or Celery) could become a valuable addition. A queue system would allow us to offload non-critical tasks and enhance the scalability of the app.

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

To deploy the application on a Kubernetes cluster, connect to your cluster and apply the deployment manifest with:

```jsx
kubectl -f gitops_repo/deployment.yml
```

Alternatively, you can use Helm, which offers the flexibility to override configuration values easily:

```
helm template hello-app ./deployment > output.yml
kubectl -f output.yml
```

In Kubernetes, readiness and liveness probes are essential for monitoring the health of your application. If the application fails to connect to the database or enters an unhealthy state (such as a deadlock), Kubernetes may trigger a `CrashLoopBackOff` or restart the pod.

To avoid unnecessary restarts and to ensure high availability, it’s important to configure these probes properly. They allow for early detection of issues, ensuring that only healthy instances serve traffic.

To guarantee that the application starts with a ready and initialized environment, an InitContainer is deployed alongside the application. This InitContainer handles the following tasks before the main application container starts:

- Verifies the database is accessible and running.
- Executes any required pre-migration scripts or database initialization routines.

By using an InitContainer, we can prevent startup issues related to missing database schemas or pending migrations, ensuring that the main application container runs in a reliable and consistent state.

Another improvement would be to add a `network policy` that only allows communication between the Hello App and the PostgreSQL DB through private endpoints and not through the public IP restricting the outbound connections from the Hello App.

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
- Rollback_release (Rollback the new version an ensure stability if Test-gitops KO)

## Cloud Design AWS EKS & RDS Architecture

![AWS-Architecture.png](https://github.com/tidusete/hello_app/blob/main/AWS-Architecture.png)

### Network

This infrastructure design leverages Amazon EKS for container orchestration and Amazon RDS for managed databases, built for high availability and security within a multi-AZ VPC setup.

- Public Subnets: Host NAT Gateways, an Application Load Balancer (ALB), and optionally a bastion host or VPN gateway.
- Private Subnets: Host EKS Worker Nodes. No direct internet access. Outbound traffic is routed via NAT Gateways.
- DB Subnets: Fully private, hosting RDS instances with no internet access.

### Security & Access

- Security Groups enforce strict access between components.
- EKS API access can be either:
    - Public: With security groups restricting IP access.
    - Private: Via bastion host / VPN (e.g. Tailscale) in a public subnet.
- AWS Secrets Manager Access: Worker Nodes access Secrets Manager through a VPC Interface Endpoint, ensuring private, secure API communication without traversing the public internet.

### RDS Setup

- Multi-AZ Deployment: Primary RDS instance replicates synchronously to a standby in another AZ for automatic failover.
- Read Replicas (optional): Asynchronous replicas to distribute read traffic and improve scalability. Can be promoted if needed.
- Automatic Backups: You can turn on automated backups, or manually create your own backup snapshots that can be used later for a restore.

### AWS Secrets Manager Integration

- IAM Roles for Service Accounts (IRSA): Kubernetes ServiceAccounts are annotated with IAM roles granting fine-grained Secrets Manager permissions.
- VPC Interface Endpoint: A private endpoint for Secrets Manager is provisioned inside the VPC, allowing EKS Worker Nodes to securely access secrets without using NAT Gateways or the public internet.

Note: In GitOps environments (e.g., ArgoCD), this integration enables controllers or secret injectors to securely fetch secrets at deployment time, without exposing them in plain text within the Git repository.