```bash
gcloud auth login
gcloud config set project sales-engineering-282713
gcloud config set run/region asia-southeast1-a
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
gcloud artifacts repositories create piiservice \
 --repository-format=docker \
 --location=asia-southeast1 \
 --description="piiservice"
docker pull docker.cloudsmith.io/kong/ai-pii/service:v0.1.2-en
docker tag docker.cloudsmith.io/kong/ai-pii/service:v0.1.2-en \
 asia-southeast1-docker.pkg.dev/sales-engineering-282713/piiservice/ai-pii-service:v0.1.2-en
gcloud auth configure-docker \
 asia-southeast1-docker.pkg.dev
docker push asia-southeast1-docker.pkg.dev/sales-engineering-282713/piiservice/ai-pii-service:v0.1.2-en
```
