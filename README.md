# Self-Optimizing Kubernetes Advisor

## 1. Overview

The Self-Optimizing Kubernetes Advisor helps platform engineering teams and SREs right-size workloads and optimize Kubernetes clusters. It continuously analyzes telemetry data (from Prometheus and kube-state-metrics) and provides actionable optimization suggestions, such as autoscaling recommendations, QoS class adjustments, and cost-saving opportunities. The system can optionally perform autonomous remediation, making it FinOps-native and reducing manual intervention.

---

## 2. Architecture and Components

### 2.1 High-Level Architecture

```
K8s Cluster
  └─> Metrics Agent ──> AWS MSK (Kafka) ──> Lambda (Flask App) ──> API Gateway ──> Frontend
                                              │
                                              └─> (Optional) Kubernetes API for remediation
```

### 2.2 Components
- **Metrics Agent (Kubernetes):** Collects metrics from Prometheus and kube-state-metrics, publishes to AWS MSK (Kafka).
- **AWS MSK (Kafka):** Message bus for telemetry data.
- **Flask Backend (AWS Lambda):** Consumes metrics from Kafka, analyzes, exposes REST API for recommendations/remediation.
- **API Gateway:** Exposes backend as a public API for the frontend and other clients.
- **Frontend (React):** Dashboard for cluster health, recommendations, and cost insights. Allows users to approve/trigger remediations.
- **(Optional) Remediation Engine:** Applies recommended changes to the Kubernetes cluster via the Kubernetes API.

---

## 3. Local Development & Demo

### 3.1 Backend (Flask)
- Can be started as a regular Flask app without Kafka/MSK for demo purposes, using default/test data.
- **Steps:**
  1. Navigate to the `backend` directory.
  2. (Optional) Create a virtual environment:
     - Windows (PowerShell):
       ```powershell
       python -m venv venv
       .\venv\Scripts\Activate
       ```
     - Mac:
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```
  3. Install dependencies:
     ```
     pip install -r requirements.txt
     ```
  4. Start the Flask app:
     - Windows (PowerShell):
       ```powershell
       $env:FLASK_APP = "app.py"
       flask run
       ```
     - Mac:
       ```bash
       export FLASK_APP=app.py
       flask run
       ```
- The app will serve recommendations at `http://localhost:5000/recommendations` using default test data.
- **Note:** In PowerShell, do not use `&&` to chain commands. Set environment variables and run commands on separate lines. If you encounter a script execution policy error, run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Note on favicon.ico 404:**
  - When running locally, you may see a 404 error for `/favicon.ico` in your Flask logs. This is normal and does not affect your app’s functionality. Browsers request a favicon by default.
  - If you want to remove this warning, add the following route to your `app.py`:
    ```python
    @app.route('/favicon.ico')
    def favicon():
        from flask import send_from_directory
        import os
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    ```
  - Then, place a `favicon.ico` file in your `backend/static/` directory.

### 3.2 Frontend (React)
- **Node.js and npm are required.**
  - Download and install from: https://nodejs.org/
  - After installation, close and reopen your terminal.
  - Verify installation:
    ```powershell
    node --version
    npm --version
    ```
- The frontend can be run locally and pointed to the local backend.
- In `frontend/src/App.tsx`, set the fetch URL to `http://localhost:5000/recommendations`.
- **Steps:**
  1. Navigate to the `frontend` directory.
  2. If you see an error http://localhost:5000/recommendationsabout a missing `package.json` file, create a new React app:
     - Go to your project root:
       ```powershell
       cd ..
       Remove-Item -Recurse -Force frontend
       npx create-react-app frontend --template typescript
       ```
     - Copy your existing `src/App.tsx` into the new `frontend/src/App.tsx` (overwrite the default one).
     - Navigate back to the frontend directory:
       ```powershell
       cd frontend
       ```
  3. Run `npm install`.
  4. Run `npm start`.
- The dashboard will be available at `http://localhost:3000`.
- **Troubleshooting:**
  - If you encounter JSON parse errors or missing script errors when running npm commands, your `package.json` may be malformed or missing. In this case, delete the `frontend` directory and recreate it as above.
  - Confirm that `npm start` works and the UI loads in your browser.

### 3.3 Demo UI
- A static HTML mockup of the UI is available at `frontend/public/demo-ui.html`.
  - Open this file directly in your browser, or visit `http://localhost:3000/demo-ui.html` if the React dev server is running.

---

## 4. Production Deployment (AWS)

### 4.1 Infrastructure Components
- **AWS MSK (Kafka):** For ingesting and streaming metrics.
- **AWS Lambda:** Runs the Flask backend for analysis and API.
- **API Gateway:** Exposes REST endpoints for the frontend.
- **(Optional) DynamoDB/RDS:** For persistent storage if needed.
- **VPC, Subnets, Security Groups:** For secure networking.

### 4.2 Deployment Steps
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

### 4.3 Quick Terraform Deployment
- Update subnet and security group IDs in `infra/main.tf`.
- Place your Lambda deployment package (`lambda_app.zip`) in the root directory.
- Run:
  ```
  terraform init
  terraform apply
  ```
- Note the outputs for API Gateway and MSK endpoints.

---

## 5. Reconfiguration

- **Kafka Broker/Topic:** Update the `KAFKA_BROKER` and `KAFKA_TOPIC` environment variables in the Lambda function configuration.
- **Analysis Logic:** Modify `backend/analysis.py` to adjust thresholds, add new rules, or integrate ML models.
- **Frontend API Endpoint:** Update the API endpoint in `frontend/src/App.tsx` to point to your deployed API Gateway URL.
- **Infrastructure:** Edit `infra/main.tf` to change resource sizes, networking, or add new AWS resources. Re-run `terraform apply` to update infrastructure.
- **Agent Configuration:** Update the agent’s configuration in your Kubernetes cluster to change metric sources or Kafka endpoints.

---

## 6. Additional Resources
- For more details, see the `infra/README.md` and comments in the codebase.
- For troubleshooting, see the notes in the Local Development & Demo section above.