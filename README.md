# Kubernetes Job Scheduler & Automation System

## Project Overview
This project demonstrates how to execute and manage batch workloads in Kubernetes
using **Jobs** and **CronJobs**, along with a **FastAPI-based REST API** to submit
and monitor jobs programmatically.

It reflects real-world DevOps and SRE use cases such as:
- Running one-time operational tasks
- Scheduling recurring maintenance jobs
- Triggering Kubernetes Jobs through an API instead of manual YAML applies

---

## Architecture
The system follows a simple request flow:

1. A user sends an HTTP request (for example, using curl).
2. The request is received by a FastAPI application running inside the Kubernetes cluster.
3. FastAPI communicates with the Kubernetes **Batch API** using in-cluster authentication.
4. Kubernetes executes the workload as:
   - A **Job** for one-time execution
   - A **CronJob** for scheduled execution

All components use native Kubernetes primitives.

---

## Features
- One-time batch execution using Kubernetes Jobs
- Scheduled execution using Kubernetes CronJobs
- REST API to:
  - List existing Jobs
  - Create new Jobs dynamically
- FastAPI runs inside the cluster using in-cluster configuration
- Tested on a local Kubernetes cluster (Minikube)

---

## Project Structure
projectB/
├── api/
│ └── app.py # FastAPI application
├── k8s/
│ ├── job.yaml # One-time Job definition
│ ├── cronjob.yaml # Scheduled CronJob definition
│ ├── deployment.yaml # API Deployment
│ └── service.yaml # API Service
└── README.md

## How to Run (Local Kubernetes with Minikube)

### 1. Start Minikube
```bash
minikube start

###2. Build Docker image inside Minikube
eval $(minikube docker-env)
docker build -t job-scheduler-api:latest .


###3. Deploy Kubernetes resources
kubectl apply -f k8s/

###4. Access the API
minikube service job-scheduler-api
This will open the API in your browser or provide a local URL.

###API Usage Examples
Health check
curl http://<service-url>/

List Jobs
curl http://<service-url>/jobs

Create a new Job
curl -X POST http://<service-url>/jobs


Key Learnings

Kubernetes Job and CronJob lifecycle management

In-cluster authentication and API access

Building operational automation using FastAPI

Debugging real-world Kubernetes networking and permissions issues
