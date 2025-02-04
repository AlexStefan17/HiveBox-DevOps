# HiveBox-DevOps

This project contains a Python application that prints the current app version using semantic versioning.

## Requirements

- [Docker](https://www.docker.com/products/docker-desktop) installed locally.

## How to Build and Run the Docker Container

Follow these steps to build and run the Docker container locally.

### 1. Clone the Repository

First, clone this repository to your local machine and go inside the cloned directory:

```bash
git clone https://github.com/your-username/HiveBox-DevOps.git
cd HiveBox-DevOps
```

### 2. Build the Docker Image
```bash 
docker build -t hive:latest .
```

### 3. Run the Docker Container
```bash
docker run --rm --name Hive-Flask -p 5000:5000 hive:latest
```

### 4. How to pylint
```bash
pylint src/
```

## Kubernetes

### Prerequisites
- install Kubernetes
- install Kind

### 1. Create kind cluster
```
kind create cluster --config kind-config.yaml
```
### 2. Activate Ingress NGINX
```
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
```

### 3. Upload docker image to the cluster
```
docker build -t hivebox-app:latest .
kind load docker-image hivebox-app:latest --name hivebox-cluster
```
### 4. Apply all manifests
```
kubectl apply -f k8s
```
### 5. Configure hostname resolution
sudo bash -c 'echo "127.0.0.1 hivebox.local" >> /etc/hosts'

### 6. How to delete cluster
```
kind delete cluster --name hivebox-cluster
```