# HiveBox-DevOps

This project contains a Python application that prints the current app version using semantic versioning.

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop) installed locally.

## How to Build and Run the Docker Container

Follow these steps to build and run the Docker container locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/HiveBox-DevOps.git
cd HiveBox-DevOps
```

### 2. Build the Docker Image
```bash 
docker build -t app-version:latest .
```

### 3. Run the Docker Container
```bash
docker run --rm app-version:latest
```