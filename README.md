# ☁️ Cloud-Based AI Analytics Deployment

![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3%20%7C%20RDS%20%7C%20ECR%20%7C%20CloudWatch-orange?logo=amazonaws)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green?logo=githubactions)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-REST%20API-lightgrey?logo=flask)

A production-grade, cloud-based machine learning analytics platform deployed on AWS. This project demonstrates a complete DevOps lifecycle — from local development to automated cloud deployment — using Docker, GitHub Actions CI/CD, and AWS services.

---

## 📋 Project Overview

This project deploys a **Random Forest ML model** as a REST API on AWS. The architecture includes:
- A **Flask API** serving real-time predictions
- **Docker** containers for consistent environments
- A **3-stage CI/CD pipeline** that automatically tests, builds, and deploys on every code push
- **Auto Scaling** to handle variable traffic
- **CloudWatch** monitoring with email alerts

---

## 🏗️ Architecture

```
Developer (Local)
       │
       │  git push
       ▼
  GitHub Repository
       │
       │  Triggers GitHub Actions
       ▼
┌─────────────────────────────────┐
│       CI/CD Pipeline            │
│  [Test] → [Build] → [Deploy]   │
└─────────────────────────────────┘
       │                    │
       │ Push Image         │ SSH Deploy
       ▼                    ▼
  Amazon ECR          Amazon EC2
  (Docker Registry)   (Auto Scaling Group)
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
             Amazon S3   Amazon RDS  CloudWatch
           (Model Store) (Database)  (Monitoring)
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Cloud Provider | AWS (us-east-2 / Ohio) |
| Compute | EC2 (Amazon Linux 2023, t2.micro) |
| Container Registry | Amazon ECR |
| Storage | Amazon S3 |
| Database | Amazon RDS (PostgreSQL) |
| Monitoring | Amazon CloudWatch + SNS |
| Scaling | EC2 Auto Scaling Group |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Application | Python 3.11, Flask |
| ML Framework | scikit-learn (RandomForestClassifier) |
| Production Server | Gunicorn |

---

## 📁 Project Structure

```
cloud-analytics-deployment/
│
├── app/                          # Application source code
│   ├── main.py                   # Flask API (health + predict endpoints)
│   ├── model.py                  # ML model training and inference
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Container build instructions
│
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_app.py               # Pytest unit tests
│
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD pipeline (test → build → deploy)
│
├── docs/                         # Project documentation
│   ├── architecture-diagram.png  # System architecture diagram
│   ├── Project_Implementation_Guide.docx
│   └── Project_Log.docx          # Step-by-step log with errors & fixes
│
├── docker-compose.yml            # Local development setup
├── .gitignore
└── README.md
```

---

## 🚀 CI/CD Pipeline

Every push to `main` triggers a 3-stage automated pipeline:

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  TEST    │────▶│  BUILD   │────▶│  DEPLOY  │
│          │     │          │     │          │
│ pytest   │     │ docker   │     │ SSH into │
│ 3 tests  │     │ build +  │     │ EC2 and  │
│          │     │ push ECR │     │ restart  │
└──────────┘     └──────────┘     └──────────┘
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `EC2_HOST` | EC2 public IP address |
| `EC2_USERNAME` | `ec2-user` |
| `EC2_SSH_KEY` | Contents of your `.pem` key file |

---

## 🔧 Local Development

### Prerequisites
- Docker Desktop installed and running
- AWS CLI configured (`aws configure`)

### Run locally

```bash
# Clone the repository
git clone https://github.com/Suyog-Desai/cloud-analytics-deployment.git
cd cloud-analytics-deployment

# Build and start with Docker Compose
docker-compose up -d --build

# Test the API
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

## 📡 API Endpoints

### Health Check
```
GET /health
```
```json
{"status": "healthy"}
```

### Predict
```
POST /predict
Content-Type: application/json

{"features": [5.1, 3.5, 1.4, 0.2]}
```
```json
{"prediction": 0}
```

| Input | Description |
|---|---|
| features[0] | Sepal length (cm) |
| features[1] | Sepal width (cm) |
| features[2] | Petal length (cm) |
| features[3] | Petal width (cm) |

| Output | Flower Type |
|---|---|
| 0 | Iris Setosa |
| 1 | Iris Versicolor |
| 2 | Iris Virginica |

---

## ☁️ AWS Infrastructure

### Services Used

**EC2** — Hosts the Docker container running the Flask API. Attached IAM role provides access to S3, ECR, and CloudWatch without hardcoded credentials.

**S3** — Stores the trained `model.pkl` artifact. Versioning and SSE-S3 encryption enabled.

**RDS (PostgreSQL)** — Provisioned for persistent storage of prediction logs and request history.

**ECR** — Private Docker registry storing all versioned container images.

**Auto Scaling Group** — Automatically adds EC2 instances when CPU exceeds 70%, scales down when load drops. Min: 1, Max: 3 instances.

**CloudWatch** — Collects CPU, memory, and disk metrics via CloudWatch Agent. Custom metric `HTTP5xxErrors` sent from the app via boto3. Alarms configured with SNS email notifications.

---

## 📊 Monitoring & Alerts

| Alarm | Threshold | Action |
|---|---|---|
| High CPU | > 80% for 5 min | SNS email + trigger scale out |
| High Memory | > 85% | SNS email notification |
| HTTP 5xx Errors | > 10 in 1 minute | SNS email + trigger scale out |

---

## 🔒 Security

- IAM roles used instead of hardcoded credentials
- EC2 runs Docker containers as non-root user
- RDS not publicly accessible — only reachable from EC2 security group
- SSH key-based authentication only (no passwords)
- S3 bucket blocks all public access

---

## 📄 Documentation

| Document | Description |
|---|---|
| `docs/Project_Implementation_Guide.docx` | Complete step-by-step setup guide |
| `docs/Project_Log.docx` | Full implementation log with errors and resolutions |

---

## 👤 Author

**Suyog Desai**
- GitHub: [@Suyog-Desai](https://github.com/Suyog-Desai)

---

## 📅 Timeline

Built as part of Cloud & DevOps portfolio — February 2026
