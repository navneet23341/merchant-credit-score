# MerchantScore — AI Credit Intelligence for Indian MSMEs

> India has 63 million MSMEs. Less than 15% have access to formal credit.
> Banks don't understand merchant businesses. MerchantScore changes that.

## What it does

MerchantScore analyzes a merchant's Razorpay transaction data across 
15 financial signals and generates:

- Real-time credit score (300-900)
- Full explainability — why is your score what it is
- 6-month trajectory — where your score is headed
- Working capital recommendation — exactly what you qualify for
- Hinglish explanation — so every merchant understands

## The Problem

A restaurant owner in Jaipur processes ₹3 lakh/month through Razorpay.
Her transaction data shows consistent revenue, low refund rate, 
high repeat customers. She's creditworthy.

But the bank sees: no collateral, no salary slip, no credit history.
Loan rejected.

MerchantScore reads what the bank can't.

## Tech Stack

- Python, XGBoost, SHAP
- FastAPI backend
- React frontend  
- Razorpay Test APIs

## Dataset

1000 synthetic merchants across 15 categories and 10 Indian cities.
15 financial signals engineered from transaction patterns.

## Credit Signals

1. Revenue consistency score
2. Monthly revenue growth rate
3. Refund rate
4. Chargeback rate
5. Customer repeat rate
6. Payment method diversity
7. Failed payment rate
8. Settlement velocity
9. Dispute resolution rate
10. Late settlement frequency
11. Revenue concentration risk
12. Average transaction value
13. Monthly transaction volume
14. Peak season ratio
15. Years active on platform

# MerchantScore — AI Credit Intelligence for Indian MSMEs

> An end-to-end AI-powered merchant credit intelligence platform that converts transaction and business signals into a credit score, explains the score, simulates possible improvements, provides working-capital recommendations, and generates a simple Hinglish explanation.

---

## Overview

Small and medium-sized merchants often have useful financial signals hidden inside their transaction activity:

* revenue consistency
* revenue growth
* refund behaviour
* chargebacks
* customer repeat rate
* payment diversity
* failed payments
* settlement behaviour
* dispute resolution
* transaction volume
* average transaction value

Traditional credit evaluation may not fully capture these signals.

**MerchantScore** uses these merchant-level signals to build an AI-powered credit intelligence system.

For a selected merchant, the platform provides:

* Credit score
* Credit tier
* Explainability using SHAP
* Historical score trajectory
* Projected 3-month score
* Interactive what-if stress testing
* Working-capital recommendation
* AI-generated Hinglish explanation

The project contains a React dashboard, FastAPI backend, trained ML models, SHAP explainability, and an OpenRouter-powered natural-language explanation layer.

---

# Features

## 1. Merchant Credit Scoring

The system uses a trained XGBoost regression model to estimate a merchant's credit score from financial and transaction-related signals.

The model works with 15 core signals:

1. Revenue consistency
2. Revenue growth rate
3. Refund rate
4. Chargeback rate
5. Customer repeat rate
6. Payment diversity
7. Failed payment rate
8. Settlement velocity
9. Dispute resolution rate
10. Late settlement frequency
11. Revenue concentration risk
12. Average transaction value
13. Monthly transaction volume
14. Peak season ratio
15. Years active

The resulting score is used as the merchant's model-based credit score.

---

## 2. Credit Tier Classification

A separate classification model assigns a credit tier to the merchant.

The score and tier are shown together in the dashboard so that the user can understand both the numerical score and its broader credit category.

---

## 3. SHAP Explainability

The platform does not only produce a score.

It also answers:

> **"Why did this merchant receive this score?"**

SHAP (SHapley Additive exPlanations) is used to identify the contribution of individual features.

For example, the system can show that:

```text
Dispute Resolution Rate      +21.5
Revenue Consistency          +14.7
Revenue Growth                +8.2
Payment Diversity             -0.6
```

Positive values push the score upward while negative values push it downward.

This makes the ML prediction more interpretable.

---

## 4. Score Trajectory

The dashboard visualizes the merchant's score trajectory.

The system uses the merchant's stored historical score trajectory and projected 3-month score to show:

```text
Historical Score
       ↓
Current Score
       ↓
Projected Score
```

This helps the merchant understand whether their credit profile is improving or declining.

---

## 5. What-If Stress Testing

The stress tester allows the user to modify important merchant signals and see how the ML model responds.

Currently the dashboard allows simulation of signals such as:

* Refund rate
* Failed payment rate
* Customer repeat rate

For example:

```text
Current:

Refund rate       = 8%
Repeat customers  = 36%
Failed payments   = 1%

Current score = 774
```

The user can change the values and the backend sends the modified feature vector through the trained regression model.

The system then returns:

```text
Current score      → 774
Projected score    → 789
Score improvement  → +15
```

This makes the model actionable rather than purely descriptive.

---

## 6. Working Capital Recommendation

The platform also provides a working-capital recommendation for the merchant.

The recommendation is based on the recommendation fields already present in the merchant dataset.

It provides:

* Eligibility
* Maximum recommended amount
* Interest rate
* Recommended tenure
* Recommendation tier

Example:

```text
Eligible:             Yes
Maximum amount:       ₹10,00,000
Interest rate:        15%
Tenure:               18 months
Recommendation tier:  Standard
```

The recommendation tier is separate from the ML credit tier.

For example:

```text
Credit tier:
Good

Recommendation tier:
Standard
```

These represent different concepts.

---

## 7. AI Hinglish Explanation

The platform uses an LLM through OpenRouter to convert the technical credit analysis into a simple Hinglish explanation.

Instead of showing only:

```text
Dispute Resolution Rate: +21.51
Payment Diversity: -0.63
```

the merchant receives an explanation such as:

```text
Aapka score 773.54 hai...
```

The explanation is generated from the model's actual factors and is intended to make the result easier for a merchant to understand.

---

# System Architecture

```text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │                      │
                         │  Merchant Dashboard  │
                         └──────────┬───────────┘
                                    │
                              HTTP / REST API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │                      │
                         │  Merchant APIs       │
                         │  Score APIs          │
                         │  SHAP APIs           │
                         │  Stress Test API     │
                         │  AI Explanation API  │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌────────────┐  ┌───────────────┐
             │ XGBoost    │  │    SHAP    │  │ Recommendation│
             │ ML Models  │  │Explainability│ │    Rules/Data │
             └─────┬──────┘  └──────┬─────┘  └───────┬───────┘
                   │                 │                │
                   └─────────────────┼────────────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │ Merchant Dataset │
                           │                  │
                           │ 1000 synthetic   │
                           │ merchants        │
                           └──────────────────┘

                                     │
                                     ▼
                              ┌──────────────┐
                              │  OpenRouter  │
                              │     LLM      │
                              └──────┬───────┘
                                     │
                                     ▼
                              Hinglish Explanation
```

---

# End-to-End Data Flow

When a user searches for a merchant:

```text
1. User enters Merchant ID
              ↓
2. React sends request to FastAPI
              ↓
3. FastAPI retrieves merchant data
              ↓
4. ML service prepares the 15 model features
              ↓
5. XGBoost regression model predicts credit score
              ↓
6. Classification model predicts credit tier
              ↓
7. SHAP calculates feature contributions
              ↓
8. Stress-test information is generated
              ↓
9. Working-capital recommendation is retrieved
              ↓
10. Dashboard data is returned to React
              ↓
11. React renders the merchant dashboard
              ↓
12. Hinglish explanation is generated through OpenRouter
```

---

# What-If Stress Test Flow

The stress tester follows a slightly different path:

```text
User changes slider
       ↓
React sends modified values
       ↓
POST /api/merchant/{merchant_id}/stress-test
       ↓
FastAPI validates the request
       ↓
ML service retrieves original merchant features
       ↓
Selected features are replaced
       ↓
XGBoost regression model predicts new score
       ↓
Current score vs projected score
       ↓
Result returned to React
       ↓
Dashboard updates
```

This means the stress tester is connected to the actual trained model rather than using a frontend-only scoring formula.

---

# Project Structure

```text
merchant-credit-score/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   └── services/
│       ├── __init__.py
│       └── ml_service.py
│
├── data/
│   ├── merchant_dataset.csv
│   └── ml_training_data.csv
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── ScoreBreakdown.jsx
│   │   │   ├── ScoreTrajectory.jsx
│   │   │   ├── HinglishExplanation.jsx
│   │   │   ├── StressTester.jsx
│   │   │   └── CapitalRecommendation.jsx
│   │   │
│   │   └── App.jsx
│   │
│   └── ...
│
├── ml/
│   ├── train_model.py
│   ├── shap_explainer.py
│   ├── stress_test.py
│   │
│   └── artifacts/
│       ├── model.pkl
│       ├── regression_model.pkl
│       ├── classification_model.pkl
│       ├── feature_columns.pkl
│       ├── tier_mapping.pkl
│       ├── metrics.json
│       ├── shap_values.csv
│       └── ...
│
├── generate_dataset.py
├── test_nvidia.py
├── .gitignore
└── README.md
```

The repository keeps the trained ML artifacts in Git because the backend needs the trained models at runtime. The virtual environment, Python cache files, Node modules, build output, and environment files are ignored.

---

# Dataset

The current project uses a **synthetic dataset of 1,000 merchants**.

The dataset contains merchant/business information, transaction signals, credit-related fields, score trajectory information, and working-capital recommendation fields.

The dataset is designed for demonstrating the complete ML product workflow.

It is **not real customer financial data**.

---

# Dataset Assumptions

The following assumptions are made by the project.

### 1. Synthetic merchant data

The dataset is synthetic and is intended for development, experimentation, and demonstration.

The resulting scores should therefore **not be interpreted as real lending decisions**.

### 2. Transaction signals represent merchant behaviour

The 15 features are treated as meaningful indicators of merchant financial health.

Examples include:

```text
Revenue consistency
Refund rate
Chargeback rate
Customer repeat rate
Failed payment rate
Settlement behaviour
```

### 3. Historical patterns are informative

The model assumes that past merchant behaviour contains useful information about creditworthiness.

### 4. Model score is an estimate

The credit score is an ML prediction, not a legally or financially authoritative credit score.

### 5. Working-capital recommendations are illustrative

The financing recommendation fields are intended to demonstrate a recommendation workflow.

They should not be interpreted as actual loan approval terms.

### 6. No real-time financial verification

The current system does not independently verify bank statements, GST records, credit bureau data, collateral, identity, or other external financial information.

### 7. No production lending decision

This project is a technical demonstration and should not be used to make real lending decisions without proper validation, governance, compliance, monitoring, and financial-risk controls.

---

# Machine Learning Pipeline

## Training

The training pipeline uses the merchant training dataset and separates the relevant feature columns from the target variables.

Two models are trained:

### Regression

Predicts the numerical credit score.

```text
Input:
15 merchant signals

        ↓

XGBoost Regressor

        ↓

Predicted credit score
```

### Classification

Predicts the credit tier.

```text
Input:
15 merchant signals

        ↓

XGBoost Classifier

        ↓

Credit tier
```

The trained models are saved as `.pkl` artifacts and loaded by the FastAPI backend.

---

# Explainability Pipeline

```text
Merchant
   ↓
Feature Vector
   ↓
Trained XGBoost Model
   ↓
SHAP TreeExplainer
   ↓
Feature Contributions
   ↓
Positive / Negative Factors
   ↓
Dashboard
```

This allows the system to expose the features that had the largest influence on the predicted score.

---

# API

The FastAPI backend exposes REST endpoints.

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "merchant-credit-intelligence-api"
}
```

---

## List Merchants

```http
GET /api/merchants
```

Returns the available merchants and basic credit information.

---

## Complete Merchant Dashboard

```http
GET /api/merchant/{merchant_id}
```

Returns the complete merchant analysis including:

* Merchant information
* Credit score
* Credit tier
* SHAP explanation
* Score trajectory
* Stress-test information
* Working-capital recommendation

---

## Credit Score

```http
GET /api/merchant/{merchant_id}/score
```

Returns the merchant's predicted credit score and tier.

---

## SHAP Explanation

```http
GET /api/merchant/{merchant_id}/explanation
```

Returns feature-level explanation data.

---

## Stress Test

```http
GET /api/merchant/{merchant_id}/stress-test
```

Returns benchmark-based stress-test scenarios.

---

## Custom Stress Test

```http
POST /api/merchant/{merchant_id}/stress-test
```

Example request:

```json
{
  "changes": {
    "refund_rate": 5,
    "customer_repeat_rate": 50,
    "failed_payment_rate": 1
  }
}
```

The backend modifies the selected features and runs them through the trained regression model.

---

## Hinglish AI Explanation

```http
GET /api/merchant/{merchant_id}/hinglish-explain
```

Generates a simple natural-language explanation using the merchant's credit analysis.

This endpoint requires an OpenRouter API key.

---

# Local Setup

## Requirements

Install:

* Python 3.10+
* Node.js 18+
* npm

---

# 1. Clone the Repository

```bash
git clone https://github.com/navneet23341/merchant-credit-score.git
```

Enter the project:

```bash
cd merchant-credit-score
```

---

# 2. Backend Setup

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

The backend dependencies include FastAPI, Uvicorn, Pandas, NumPy, Scikit-learn, XGBoost, SHAP, Joblib, and Pydantic.

---

# 3. Configure OpenRouter

The Hinglish explanation endpoint requires an OpenRouter API key.

Create:

```text
.env
```

Do **not** commit this file to GitHub.

Set:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

The repository's `.gitignore` already excludes `.env` and `.env.*`.

---

# 4. Start the Backend

From the **project root**:

```bash
uvicorn backend.main:app --reload
```

The API should start at:

```text
http://127.0.0.1:8000
```

Check:

```text
http://127.0.0.1:8000/health
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 5. Frontend Setup

Open a second terminal.

Enter the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

The frontend uses React, Vite, Tailwind CSS, and Recharts.

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 6. Run the Complete Application

You need two processes running.

### Terminal 1 — Backend

```bash
uvicorn backend.main:app --reload
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

Enter a merchant ID such as:

```text
MID_0001
```

and click **Analyse**.

---

# Running the ML Training Pipeline

The repository also contains the model training code.

If you want to retrain the models instead of using the existing artifacts:

```bash
python ml/train_model.py
```

This produces the trained model artifacts used by the backend.

The generated artifacts include model files, feature metadata, evaluation metrics, and explainability-related outputs.

> The existing trained artifacts are already included in the repository, so retraining is not required just to run the application.

---

# Regenerating the Dataset

The project also contains:

```text
generate_dataset.py
```

which can be used to generate the synthetic merchant dataset.

Run:

```bash
python generate_dataset.py
```

If you regenerate the dataset, retraining the ML models may also be necessary to keep the dataset and model artifacts consistent.

---

# Model Evaluation

The project evaluates both regression and classification performance during model training.

Regression metrics include:

* RMSE
* MAE
* R²

Classification metrics include:

* Accuracy
* Macro F1

The generated metrics are stored in:

```text
ml/artifacts/metrics.json
```

---

# Technology Stack

## Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* SHAP
* Joblib

## Backend

* FastAPI
* Pydantic
* Uvicorn

## Frontend

* React
* Vite
* Tailwind CSS
* Recharts

## Generative AI

* OpenRouter API
* LLM-based Hinglish explanation

## Data

* CSV-based synthetic merchant dataset

---

# Deployment Architecture

The application can be deployed as two services:

```text
                    GitHub Repository
                           │
               ┌───────────┴───────────┐
               │                       │
               ▼                       ▼
          Railway                    Vercel
          Backend                   Frontend
               │                       │
               │      HTTPS/API        │
               └───────────────────────┘
```

### Backend

Deploy the FastAPI application to Railway.

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

The backend requires the trained model artifacts and dataset files.

Add the following environment variable to the deployment:

```text
OPENROUTER_API_KEY
```

### Frontend

Deploy the `frontend/` directory to Vercel.

The frontend should use an environment variable for the backend URL:

```env
VITE_API_URL=https://your-railway-backend-url
```

The frontend then communicates with the deployed FastAPI backend.

---

# Security Notes

Never commit API keys or other secrets.

Do not put:

```text
OPENROUTER_API_KEY
```

directly inside frontend source code.

Use environment variables instead.

The repository ignores environment files such as:

```text
.env
.env.*
```

---

# Limitations

This project is a prototype and has several limitations.

### Synthetic data

The current dataset is synthetic and does not represent real merchant behaviour at production scale.

### No live transaction integration

The current version does not directly ingest live production merchant transactions.

### Limited external financial signals

The system does not currently incorporate:

* Credit bureau history
* GST data
* Bank statements
* Existing loan obligations
* Collateral
* Identity verification
* Macroeconomic conditions

### Model generalization

Strong performance on synthetic data does not guarantee equivalent performance on real-world merchant data.

### Recommendation assumptions

Working-capital recommendations are illustrative and should not be treated as actual loan offers.

### LLM dependency

The Hinglish explanation depends on an external LLM API and therefore requires an API key and network access.

---

# Future Improvements

Possible future improvements include:

* Real merchant transaction ingestion
* Razorpay API integration
* Online feature computation
* Model monitoring
* Model drift detection
* Real-world credit bureau signals
* Fraud-risk detection
* Automated model retraining
* Better recommendation optimization
* Authentication and role-based access
* Database-backed merchant storage
* Production-grade observability
* Fairness and bias evaluation
* Human review for lending decisions

---

# Project Flow Summary

```text
                Merchant ID
                     │
                     ▼
              React Dashboard
                     │
                     ▼
                FastAPI API
                     │
                     ▼
              Merchant Dataset
                     │
                     ▼
             15 Financial Signals
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   XGBoost Regression    XGBoost Classification
          │                     │
          ▼                     ▼
    Credit Score            Credit Tier
          │
          ▼
     SHAP Explainer
          │
          ▼
   Score Explanation
          │
          ├───────────────────────┐
          ▼                       ▼
    Score Trajectory        Stress Testing
          │                       │
          │                       ▼
          │                 Modified Features
          │                       │
          │                       ▼
          │                 ML Prediction
          │                       │
          └───────────┬───────────┘
                      ▼
            Working Capital
             Recommendation
                      │
                      ▼
              OpenRouter LLM
                      │
                      ▼
           Hinglish Explanation
                      │
                      ▼
              Merchant Dashboard
```

---

# Example User Journey

A merchant enters:

```text
MID_0001
```

The system then displays:

```text
Credit Score
773.54

Credit Tier
Good

Monthly Revenue
Merchant-specific revenue

Working Capital
Merchant-specific recommendation
```

The dashboard then provides:

1. **Score Breakdown**
   Shows which financial signals increased or decreased the score.

2. **Score Trajectory**
   Shows historical and projected score movement.

3. **AI Explanation**
   Converts the technical explanation into simple Hinglish.

4. **Working Capital Recommendation**
   Shows eligibility, recommended amount, interest rate, tenure, and recommendation tier.

5. **What-If Stress Tester**
   Allows the merchant to simulate improvements to selected financial signals.

---

# Disclaimer

MerchantScore is an educational and technical prototype.

It is designed to demonstrate how transaction-derived financial signals, machine learning, explainability, stress testing, recommendation logic, and generative AI can be combined into a merchant credit intelligence platform.

The generated credit scores and financing recommendations are **not real credit decisions, loan approvals, or financial advice**.

Any production lending system would require real-world data validation, rigorous model validation, monitoring, security, regulatory compliance, fairness testing, and appropriate human oversight.

---

# License

This project is intended for educational and demonstration purposes.
