from pathlib import Path
import json
import ast

import os

from dotenv import load_dotenv
from openai import OpenAI


import joblib
import pandas as pd

import numpy as np
import shap 

load_dotenv()

# NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# print("NVIDIA KEY FOUND:", bool(NVIDIA_API_KEY))

# nvidia_client = OpenAI(
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key=NVIDIA_API_KEY,
# )

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)
# ============================================================
# PATHS
# ============================================================

# backend/services/ml_service.py
#       ↓
# backend
#       ↓
# project root

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
ARTIFACT_DIR = BASE_DIR / "ml" / "artifacts"

MERCHANT_DATA_PATH = DATA_DIR / "merchant_dataset.csv"

REGRESSION_MODEL_PATH = (
    ARTIFACT_DIR / "regression_model.pkl"
)

CLASSIFICATION_MODEL_PATH = (
    ARTIFACT_DIR / "classification_model.pkl"
)

FEATURE_COLUMNS_PATH = (
    ARTIFACT_DIR / "feature_columns.pkl"
)

TIER_MAPPING_PATH = (
    ARTIFACT_DIR / "tier_mapping.pkl"
)


# ============================================================
# LOAD MODELS ONCE
# ============================================================

print("Loading ML artifacts...")

regression_model = joblib.load(
    REGRESSION_MODEL_PATH
)

classification_model = joblib.load(
    CLASSIFICATION_MODEL_PATH
)

feature_columns = joblib.load(
    FEATURE_COLUMNS_PATH
)

tier_mapping = joblib.load(
    TIER_MAPPING_PATH
)

merchants_df = pd.read_csv(
    MERCHANT_DATA_PATH
)

print(
    f"Loaded {len(merchants_df)} merchants."
)

print("ML service ready.")

# ============================================================
# SHAP EXPLAINER
# ============================================================

shap_explainer = shap.TreeExplainer(
    regression_model
)


# ============================================================
# MERCHANT LOOKUP
# ============================================================

def get_merchant(
    merchant_id: str,
):

    matches = merchants_df[
        merchants_df["merchant_id"].astype(str)
        == str(merchant_id)
    ]

    if matches.empty:
        return None

    return matches.iloc[0]


# ============================================================
# FEATURE VECTOR
# ============================================================

def get_features(
    merchant,
):

    return (
        merchant[feature_columns]
        .astype(float)
        .to_frame()
        .T
    )


# ============================================================
# SCORE
# ============================================================

def predict_score(
    merchant,
):

    features = get_features(
        merchant
    )

    score = float(
        regression_model.predict(
            features
        )[0]
    )

    # Keep score inside 0–1000.

    score = max(
        0,
        min(
            1000,
            score,
        ),
    )

    return round(
        score,
        2,
    )


# ============================================================
# TIER
# ============================================================

def predict_tier(
    merchant,
):

    features = get_features(
        merchant
    )

    prediction = (
        classification_model.predict(
            features
        )[0]
    )

    # Convert numpy integer / float safely
    prediction_id = int(prediction)

    tier = tier_mapping[
        "id_to_tier"
    ][prediction_id]

    return str(tier)


# ============================================================
# COMPLETE SCORE RESULT
# ============================================================

def get_score(
    merchant_id: str,
):

    merchant = get_merchant(
        merchant_id
    )

    if merchant is None:
        return None

    score = predict_score(
        merchant
    )

    tier = predict_tier(
        merchant
    )

    return {

        "merchant_id":
            str(merchant_id),

        "credit_score":
            score,

        "credit_tier":
            tier,

    }


# ============================================================
# SHAP EXPLANATION
# ============================================================

def get_explanation(merchant_id: str):

    merchant = get_merchant(
        merchant_id
    )

    if merchant is None:
        return None

    features = get_features(
        merchant
    )

    score = predict_score(
        merchant
    )

    # Calculate SHAP values dynamically
    shap_values = shap_explainer(
        features
    )

    values = shap_values.values[0]

    # Base value
    base_value = float(
        np.asarray(
            shap_values.base_values
        ).reshape(-1)[0]
    )

    positive_factors = []
    negative_factors = []

    for feature, value, impact in zip(
        feature_columns,
        features.iloc[0].values,
        values,
    ):

        impact = float(
            impact
        )

        if impact > 0:
            positive_factors.append({
                "feature": feature,
                "value": float(value),
                "impact": round(
                    impact,
                    2
                ),
            })

        elif impact < 0:
            negative_factors.append({
                "feature": feature,
                "value": float(value),
                "impact": round(
                    impact,
                    2
                ),
            })

    # Largest effects first
    positive_factors.sort(
        key=lambda x: x["impact"],
        reverse=True,
    )

    negative_factors.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True,
    )

    return {
        "merchant_id": str(
            merchant_id
        ),

        "credit_score": round(
            score,
            2
        ),

        "shap_base_value": round(
            base_value,
            2
        ),

        "positive_factors":
            positive_factors,

        "negative_factors":
            negative_factors,
    }


# ============================================================
# STRESS TEST
# ============================================================

HIGHER_IS_BETTER = {
    "revenue_growth_rate",
    "revenue_consistency",
    "customer_repeat_rate",
    "payment_diversity_score",
    "dispute_resolution_rate",
    "monthly_revenue",
    "transaction_volume_monthly",
    "avg_transaction_value",
}

LOWER_IS_BETTER = {
    "refund_rate",
    "chargeback_rate",
    "failed_payment_rate",
    "late_settlement_frequency",
    "settlement_velocity_days",
    "revenue_concentration_risk",
}

def get_feature_benchmark(
    feature: str,
    healthy_merchants: pd.DataFrame
):
    values = healthy_merchants[feature].dropna()

    if feature in HIGHER_IS_BETTER:
        return float(values.quantile(0.75))

    if feature in LOWER_IS_BETTER:
        return float(values.quantile(0.25))

    return float(values.median())

def get_stress_test(merchant_id: str):

    merchant = get_merchant(merchant_id)

    if merchant is None:
        return None

    # -----------------------------------------
    # Current merchant features
    # -----------------------------------------

    current_features = get_features(merchant)

    current_score = float(
        regression_model.predict(current_features)[0]
    )

    # -----------------------------------------
    # Find high-quality population
    # -----------------------------------------

    benchmark_threshold = float(
        merchants_df["credit_score"].quantile(0.75)
    )

    healthy_merchants = merchants_df[
        merchants_df["credit_score"] >= benchmark_threshold
    ].copy()

    scenarios = []

    # -----------------------------------------
    # Test every feature independently
    # -----------------------------------------

    for feature in feature_columns:

        current_value = float(
            current_features.iloc[0][feature]
        )

        benchmark_value = get_feature_benchmark(
            feature,
            healthy_merchants
        )

        # Don't recommend a change if already
        # at or beyond the healthy benchmark.
        if feature in HIGHER_IS_BETTER:

            if current_value >= benchmark_value:
                continue

        elif feature in LOWER_IS_BETTER:

            if current_value <= benchmark_value:
                continue

        # -----------------------------------------
        # Modify ONLY this feature
        # -----------------------------------------

        scenario_features = current_features.copy()

        scenario_features.loc[
            scenario_features.index[0],
            feature
        ] = benchmark_value

        projected_score = float(
            regression_model.predict(
                scenario_features
            )[0]
        )

        improvement = (
            projected_score - current_score
        )

        # Only keep actual improvements
        if improvement <= 0:
            continue

        scenarios.append({
            "feature": feature,
            "current_value": current_value,
            "benchmark_value": benchmark_value,
            "projected_score": projected_score,
            "score_improvement": improvement,
        })

    # -----------------------------------------
    # Rank recommendations
    # -----------------------------------------

    scenarios.sort(
        key=lambda x: x["score_improvement"],
        reverse=True
    )

    top_improvements = scenarios[:3]

    return {
        "merchant_id": merchant_id,
        "current_score": round(current_score, 2),

        "benchmark_method":
            "Top 25% of merchants by credit score",

        "benchmark_score_threshold":
            round(benchmark_threshold, 2),

        "benchmark_population_size":
            len(healthy_merchants),

        "top_improvements":
            top_improvements,

        "all_scenarios":
            scenarios,
    }


# ============================================================
# COMPLETE MERCHANT DATA
# ============================================================

def get_merchant_dashboard(
    merchant_id: str,
):

    merchant = get_merchant(
        merchant_id
    )

    if merchant is None:
        return None

    score_data = get_score(
        merchant_id
    )

    explanation = get_explanation(
        merchant_id
    )

    stress_test = get_stress_test(
        merchant_id
    )

    return {

        "merchant": {

            "merchant_id":
                str(
                    merchant["merchant_id"]
                ),

            "category":
                merchant["category"],

            "city":
                merchant["city"],

            "years_active":
                float(
                    merchant["years_active"]
                ),

            "monthly_revenue":
                float(
                    merchant["monthly_revenue"]
                ),
            "score_trajectory":ast.literal_eval(
                merchant["score_trajectory"]
                ),

            "projected_score_3months":
                float(
                    merchant["projected_score_3months"]
                ),
        },

        "credit": score_data,

        "explanation":
            explanation,

        "stress_test":
            stress_test,

    }

def get_hinglish_explanation(merchant_id: str):

    merchant = get_merchant(merchant_id)

    if merchant is None:
        return None

    score_data = get_score(merchant_id)

    explanation = get_explanation(merchant_id)

    #stress_test = get_stress_test(merchant_id)

    # -----------------------------------------
    # Extract top positive factor
    # -----------------------------------------

    positive_factors = (
        explanation["positive_factors"]
    )

    top_positive = (
        positive_factors[0]
        if positive_factors
        else None
    )

    # -----------------------------------------
    # Extract top negative factor
    # -----------------------------------------

    negative_factors = (
        explanation["negative_factors"]
    )

    top_negative = (
        negative_factors[0]
        if negative_factors
        else None
    )

    # -----------------------------------------
    # Build prompt
    # -----------------------------------------

    prompt = f"""
You are a financial advisor explaining credit scores
to Indian small business owners.

Merchant details:

- Category: {merchant["category"]}
- City: {merchant["city"]}
- Credit Score: {score_data["credit_score"]}

Top positive factor:
{top_positive["feature"] if top_positive else "None"}
(pushes score up {abs(top_positive["impact"]) if top_positive else 0} points)

Top negative factor:
{top_negative["feature"] if top_negative else "None"}
(pulls score down {abs(top_negative["impact"]) if top_negative else 0} points)

Generate a friendly explanation in Hinglish
(mix of Hindi and English).

Keep it simple and under 100 words.
Be encouraging but honest.

Start exactly with:
"Aapka score..."

IMPORTANT:
Only use information explicitly provided above.
Do not invent financial information.
Do not introduce generic financial advice unless it is supported
by the provided factors.
Do not assume reasons for a factor's value.
If the negative factor is None, say that no major negative factor
was identified in the provided analysis.

Do not use markdown.
Do not use bullet points.
Do not mention that you are an AI.

Do not explain what a factor "means" unless that meaning is explicitly
provided in the input.

Do not infer merchant behavior from a feature name.

For example, do not say that a high dispute resolution rate means
the merchant handles customer complaints effectively unless that
information is explicitly provided.

Do not give recommendations or financial advice unless they are
directly supported by the provided factors.

Only describe:
1. The credit score.
2. The provided positive factor and its impact.
3. The provided negative factor and its impact.
4. A simple encouraging conclusion based only on those facts.
"""



    # -----------------------------------------
    # Call OpenRouter
    # -----------------------------------------

    response = openrouter_client.chat.completions.create(
        model="minimax/minimax-m3:free",

        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        temperature=0.7,
        max_tokens=200,
    )

    # -----------------------------------------
    # Extract response
    # -----------------------------------------

    message = response.choices[0].message

    if message is None:
        raise RuntimeError("LLM returned no message")

    explanation_text = message.content

    if not explanation_text:
        raise RuntimeError("LLM returned no text content")

    explanation_text = explanation_text.strip()

    return {
        "merchant_id": str(merchant_id),
        "explanation": explanation_text,
    }