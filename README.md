# AI_models

## Self-Optimizing Kubernetes Advisor

### 1. What is this application meant to do?

The Self-Optimizing Kubernetes Advisor is designed to help platform engineering teams and SREs right-size workloads and optimize Kubernetes clusters. It continuously analyzes telemetry data (from Prometheus and kube-state-metrics) and provides actionable optimization suggestions, such as autoscaling recommendations, QoS class adjustments, and cost-saving opportunities. The system can optionally perform autonomous remediation, making it FinOps-native and reducing manual intervention.

---

### 2. Detailed Architecture

#### **Components:**
- **Metrics Agent (Kubernetes):**
  - Collects metrics from Prometheus and kube-state-metrics.
  - Publishes metrics to AWS MSK (Kafka).
- **AWS MSK (Kafka):**
  - Serves as the message bus for telemetry data.
- **Flask Backend (AWS Lambda):**
  - Consumes metrics from Kafka.
  - Runs advanced analysis to detect anomalies, right-sizing opportunities, and cost optimizations.
  - Exposes REST API endpoints for recommendations and remediation.
- **API Gateway:**
  - Exposes the backend as a public API for the frontend and other clients.
- **Frontend (React):**
  - Displays cluster health, recommendations, and cost insights.
  - Allows users to approve or trigger remediations.
- **(Optional) Remediation Engine:**
  - Applies recommended changes to the Kubernetes cluster via the Kubernetes API.

#### **Architecture Diagram:**

```
K8s Cluster
  └─> Metrics Agent ──> AWS MSK (Kafka) ──> Lambda (Flask App) ──> API Gateway ──> Frontend
                                              │
                                              └─> (Optional) Kubernetes API for remediation
```

---

### 2a. Frontend Technology and Usage

The frontend is built using **React** and **TypeScript** for a modern, responsive, and maintainable user interface. It provides:
- A dashboard displaying real-time recommendations for Kubernetes workload optimization.
- Tabular views of pods, their resource usage, and actionable suggestions.
- Integration with the backend API (via API Gateway) to fetch recommendations and trigger remediations.

**How to use/configure:**
- The main entry point is `frontend/src/App.tsx`.
- To run locally: navigate to the `frontend` directory and use `npm install` followed by `npm start`.
- To deploy: run `npm run build` and upload the contents of the `build/` directory to your static hosting (e.g., S3 + CloudFront).
- To point the frontend to your backend, update the API endpoint in `frontend/src/App.tsx` to your deployed API Gateway URL.

---

### 2b. Local Demo: Running on Windows and Mac

This application can be run locally for demo purposes on both Windows and Mac machines, using default parameters and simulated data.

#### **Backend (Flask) Local Demo**
- The backend can be started as a regular Flask app without Kafka/MSK for demo purposes.
- It will use default, estimated metrics for analysis and recommendations.
- To run locally:
  1. Navigate to the `backend` directory.
  2. (Optional) Create a virtual environment:
     - Windows: `python -m venv venv && venv\Scripts\activate`
     - Mac: `python3 -m venv venv && source venv/bin/activate`
  3. Install dependencies: `pip install -r requirements.txt`
  4. Start the Flask app:
     - Windows: `set FLASK_APP=app.py && flask run`
     - Mac: `export FLASK_APP=app.py && flask run`
- The app will serve recommendations at `http://localhost:5000/recommendations` using default test data.

#### **Frontend Local Demo**
- The frontend can be run locally and pointed to the local backend.
- In `frontend/src/App.tsx`, set the fetch URL to `http://localhost:5000/recommendations`.
- To run:
  1. Navigate to the `frontend` directory.
  2. Run `npm install`.
  3. Run `npm start`.
- The dashboard will be available at `http://localhost:3000`.

#### **Default Parameters and Estimation**
- When running locally, the backend will use simulated metrics data (see `test_analysis.py` for examples).
- Default cost estimation: `$10 per vCPU` and `$2.5 per GB RAM` per month.
- The analysis engine will provide recommendations based on these simulated values, allowing you to demo the full workflow without a real Kubernetes cluster or Kafka setup.

---

### 3. Infrastructure Details & AWS Deployment

#### **Infrastructure Components:**
- **AWS MSK (Kafka):** For ingesting and streaming metrics.
- **AWS Lambda:** Runs the Flask backend for analysis and API.
- **API Gateway:** Exposes REST endpoints for the frontend.
- **(Optional) DynamoDB/RDS:** For persistent storage if needed.
- **VPC, Subnets, Security Groups:** For secure networking.

#### **Deployment Steps:**
1. **Backend (Lambda):**
   - Package the Flask app and dependencies into a zip file (`lambda_app.zip`).
   - Deploy using Terraform (see `infra/main.tf`).
   - Set environment variables for Kafka broker and topic.
   - Attach Lambda to the same VPC/subnets/security groups as MSK.
2. **Kafka (MSK):**
   - Provisioned via Terraform (`infra/main.tf`).
   - Update subnet and security group IDs as per your AWS setup.
3. **API Gateway:**
   - Created and integrated with Lambda via Terraform.
4. **Frontend:**
   - Build the React app (`npm run build`).
   - Deploy to S3 + CloudFront or any static hosting.
   - Configure the frontend to use the API Gateway endpoint.
5. **Agent:**
   - Deploy the agent in your Kubernetes cluster.
   - Configure it to send metrics to your MSK brokers.

#### **Quick Terraform Deployment:**
- Update subnet and security group IDs in `infra/main.tf`.
- Place your Lambda deployment package (`lambda_app.zip`) in the root directory.
- Run:
  ```
  terraform init
  terraform apply
  ```
- Note the outputs for API Gateway and MSK endpoints.

---

### 4. How to Reconfigure This Application

- **Kafka Broker/Topic:**
  - Update the `KAFKA_BROKER` and `KAFKA_TOPIC` environment variables in the Lambda function configuration.
- **Analysis Logic:**
  - Modify `backend/analysis.py` to adjust thresholds, add new rules, or integrate ML models.
- **Frontend API Endpoint:**
  - Update the API endpoint in `frontend/src/App.tsx` to point to your deployed API Gateway URL.
- **Infrastructure:**
  - Edit `infra/main.tf` to change resource sizes, networking, or add new AWS resources.
  - Re-run `terraform apply` to update infrastructure.
- **Agent Configuration:**
  - Update the agent’s configuration in your Kubernetes cluster to change metric sources or Kafka endpoints.

---

For more details, see the `infra/README.md` and comments in the codebase.