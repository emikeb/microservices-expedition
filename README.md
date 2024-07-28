# Microservices Expedition

## Overview

This project demonstrates a microservices architecture with basic and enhanced communication setups. The project is divided into multiple phases, each adding more complexity and features to the microservices.

## Current Features

- Microservices-based architecture, 2 python services:
    - User Service: Manages user data.
    - Product Service: Manages product data.
- Service discovery with Consul
- API Gateway for request routing (python)
- Containerization with Docker
- Each service uses a SQLite database.
- Comprehensive test suite
- Asynchronous communication using RabbitMQ
- Event-Driven Architecture (EDA)

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Poetry
- Make (optional, for running Makefile commands)

### Running the Services

1. Clone the repository


2. **Start the services**:
    ```sh
    docker-compose up -d
    ```

2. **Run the tests**:
    ```sh
    make
    ```

### Makefile Targets

- **all**: Runs the tests and combines coverage reports.
- **all_docker**: Starts the Docker containers, runs the tests, and then stops the containers.

## API Documentation

### API Gateway Endpoints

- **Users**
  - GET `/users`: Retrieve all users
  - POST `/users`: Create a new user
  - GET `/users/{id}`: Retrieve a specific user

- **Products**
  - GET `/products`: Retrieve all products
  - POST `/products`: Create a new product
  - GET `/products/{id}`: Retrieve a specific product

- **Health Check**
  - GET `/health`: Check the health of all services

### Service-specific Endpoints

Each service (User and Product) exposes a `/health` endpoint for individual health checks.

## Contributing

We welcome contributions to the Microservices Expedition project! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/<featurename>`)
3. Commit your changes (`git commit -m 'Add some changes'`)
4. Push to the branch (`git push origin feature/<featurename>`)
5. Open a Pull Request

Feel free to fork this repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
