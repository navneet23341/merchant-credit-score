from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from backend.services.ml_service import (
    merchants_df,
    get_merchant,
    get_score,
    get_explanation,
    get_stress_test,
    get_merchant_dashboard,
    get_hinglish_explanation,
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Merchant Credit Intelligence API",
    description=(
        "AI-powered merchant credit scoring, "
        "explainability and growth recommendations."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["System"],
)
def health_check():

    return {
        "status": "healthy",
        "service": "merchant-credit-intelligence-api",
    }


# ============================================================
# LIST MERCHANTS
# ============================================================

@app.get(
    "/api/merchants",
    tags=["Merchants"],
)
def list_merchants():

    merchants = []

    for _, merchant in merchants_df.iterrows():

        merchants.append({

            "merchant_id":
                str(
                    merchant["merchant_id"]
                ),

            "category":
                str(
                    merchant["category"]
                ),

            "city":
                str(
                    merchant["city"]
                ),

            "credit_score":
                float(
                    merchant["credit_score"]
                ),

            "credit_tier":
                str(
                    merchant["credit_tier"]
                ),

        })

    return {
        "count": len(merchants),
        "merchants": merchants,
    }


# ============================================================
# COMPLETE MERCHANT DASHBOARD
# ============================================================

@app.get(
    "/api/merchant/{merchant_id}",
    tags=["Merchant"],
)
def merchant_dashboard(
    merchant_id: str,
):

    result = get_merchant_dashboard(
        merchant_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Merchant "
                f"'{merchant_id}' "
                f"not found."
            ),
        )

    return result


# ============================================================
# CREDIT SCORE
# ============================================================

@app.get(
    "/api/merchant/{merchant_id}/score",
    tags=["Merchant"],
)
def merchant_score(
    merchant_id: str,
):

    result = get_score(
        merchant_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Merchant "
                f"'{merchant_id}' "
                f"not found."
            ),
        )

    return result


# ============================================================
# SHAP EXPLANATION
# ============================================================

@app.get(
    "/api/merchant/{merchant_id}/explanation",
    tags=["Explainability"],
)
def merchant_explanation(
    merchant_id: str,
):

    # First make sure merchant exists.

    merchant = get_merchant(
        merchant_id
    )

    if merchant is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Merchant "
                f"'{merchant_id}' "
                f"not found."
            ),
        )

    explanation = get_explanation(
        merchant_id
    )

    if explanation is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "SHAP explanation "
                "not available for "
                f"merchant '{merchant_id}'."
            ),
        )

    return explanation


# ============================================================
# STRESS TEST
# ============================================================

@app.get("/api/merchant/{merchant_id}/stress-test")
def stress_test_merchant(merchant_id: str):

    result = get_stress_test(merchant_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return result

# ============================================================
# HINGLISH AI EXPLANATION
# ============================================================

@app.get(
    "/api/merchant/{merchant_id}/hinglish-explain",
    tags=["AI Explanation"],
)
def merchant_hinglish_explanation(
    merchant_id: str,
):

    result = get_hinglish_explanation(
        merchant_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Merchant "
                f"'{merchant_id}' "
                f"not found."
            ),
        )

    return result