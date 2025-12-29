import os
import uuid
from fastapi import FastAPI
from kubernetes import client, config

# Hard-disable proxy usage (important for corporate / minikube setups)
for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(var, None)

app = FastAPI(title="Kubernetes Job Scheduler API")


def get_batch_client():
    try:
        config.load_incluster_config()
    except Exception as e:
        print("Kubernetes config error:", e)
        return None
    return client.BatchV1Api()


@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/jobs")
def list_jobs():
    batch_v1 = get_batch_client()
    if not batch_v1:
        return {"error": "Kubernetes not configured"}

    jobs = batch_v1.list_namespaced_job(namespace="default")
    return [
        {
            "name": job.metadata.name,
            "succeeded": job.status.succeeded,
            "failed": job.status.failed,
            "active": job.status.active,
        }
        for job in jobs.items
    ]


@app.get("/jobs/{job_name}")
def get_job(job_name: str):
    batch_v1 = get_batch_client()
    if not batch_v1:
        return {"error": "Kubernetes not configured"}

    job = batch_v1.read_namespaced_job(
        name=job_name,
        namespace="default"
    )

    return {
        "name": job.metadata.name,
        "succeeded": job.status.succeeded,
        "failed": job.status.failed,
        "active": job.status.active,
    }


@app.post("/jobs")
def create_job():
    batch_v1 = get_batch_client()
    if not batch_v1:
        return {"error": "Kubernetes not configured"}

    job_name = f"api-job-{uuid.uuid4().hex[:6]}"

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            backoff_limit=1,
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[
                        client.V1Container(
                            name="hello",
                            image="busybox",
                            command=["sh", "-c", "echo Hello from API Job"]
                        )
                    ],
                )
            ),
        ),
    )

    batch_v1.create_namespaced_job(
        namespace="default",
        body=job
    )

    return {"status": "job created", "job_name": job_name}
