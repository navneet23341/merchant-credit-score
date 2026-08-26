from pathlib import Path
import argparse
import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MERCHANT_DATA_PATH = (
    BASE_DIR / "data" / "merchant_dataset.csv"
)

ARTIFACT_DIR = (
    BASE_DIR / "ml" / "artifacts"
)

OUTPUT_DIR = (
    ARTIFACT_DIR / "merchant_explanations"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


MODEL_PATH = (
    ARTIFACT_DIR / "regression_model.pkl"
)

FEATURES_PATH = (
    ARTIFACT_DIR / "feature_columns.pkl"
)


# ============================================================
# DISPLAY NAMES
# ============================================================

FEATURE_DISPLAY_NAMES = {

    "monthly_revenue":
        "Monthly Revenue",

    "revenue_growth_rate":
        "Revenue Growth",

    "revenue_consistency":
        "Revenue Consistency",

    "refund_rate":
        "Refund Rate",

    "chargeback_rate":
        "Chargeback Rate",

    "settlement_velocity_days":
        "Settlement Speed",

    "customer_repeat_rate":
        "Customer Repeat Rate",

    "payment_diversity_score":
        "Payment Diversity",

    "peak_season_ratio":
        "Peak Season Ratio",

    "failed_payment_rate":
        "Failed Payment Rate",

    "avg_transaction_value":
        "Average Transaction Value",

    "transaction_volume_monthly":
        "Monthly Transaction Volume",

    "dispute_resolution_rate":
        "Dispute Resolution Rate",

    "late_settlement_frequency":
        "Late Settlement Frequency",

    "revenue_concentration_risk":
        "Revenue Concentration Risk",
}


# ============================================================
# HELPERS
# ============================================================

def format_feature_value(
    feature,
    value,
):

    percentage_features = {

        "revenue_growth_rate",
        "revenue_consistency",
        "refund_rate",
        "chargeback_rate",
        "customer_repeat_rate",
        "peak_season_ratio",
        "failed_payment_rate",
        "dispute_resolution_rate",
        "revenue_concentration_risk",
    }

    if feature in percentage_features:

        return f"{value:.1%}"

    if feature == "monthly_revenue":

        return f"₹{value:,.0f}"

    if feature == "avg_transaction_value":

        return f"₹{value:,.0f}"

    if feature == "transaction_volume_monthly":

        return f"{value:,.0f}"

    if feature == "settlement_velocity_days":

        return f"{value:.1f} days"

    if feature == "late_settlement_frequency":

        return f"{value:.1%}"

    if feature == "payment_diversity_score":

        return f"{value:.2f}"

    return f"{value:.2f}"


def create_explanation_text(
    feature,
    shap_value,
    feature_value,
):

    name = FEATURE_DISPLAY_NAMES.get(
        feature,
        feature.replace("_", " ").title(),
    )

    value_text = format_feature_value(
        feature,
        feature_value,
    )

    magnitude = abs(shap_value)

    # Features where HIGH values are generally risky
    # and LOW values are generally beneficial.
    inverse_features = {
        "refund_rate",
        "chargeback_rate",
        "failed_payment_rate",
        "late_settlement_frequency",
        "settlement_velocity_days",
        "revenue_concentration_risk",
    }

    # Features where HIGH values are generally beneficial
    # and LOW values are generally risky.
    positive_features = {
        "revenue_growth_rate",
        "revenue_consistency",
        "customer_repeat_rate",
        "payment_diversity_score",
        "dispute_resolution_rate",
        "monthly_revenue",
        "transaction_volume_monthly",
    }

    if shap_value >= 0:

        if feature in inverse_features:

            return (
                f"Low {name.lower()} "
                f"({value_text}) helped your score "
                f"by {magnitude:.1f} points."
            )

        elif feature in positive_features:

            return (
                f"High {name.lower()} "
                f"({value_text}) helped your score "
                f"by {magnitude:.1f} points."
            )

        else:

            return (
                f"{name} ({value_text}) "
                f"helped your score "
                f"by {magnitude:.1f} points."
            )

    else:

        if feature in inverse_features:

            return (
                f"High {name.lower()} "
                f"({value_text}) reduced your score "
                f"by {magnitude:.1f} points."
            )

        elif feature in positive_features:

            return (
                f"Low {name.lower()} "
                f"({value_text}) reduced your score "
                f"by {magnitude:.1f} points."
            )

        else:

            return (
                f"{name} ({value_text}) "
                f"reduced your score "
                f"by {magnitude:.1f} points."
            )


# ============================================================
# LOAD MODEL + FEATURES
# ============================================================

def load_artifacts():

    print("Loading regression model...")

    model = joblib.load(
        MODEL_PATH
    )

    feature_columns = joblib.load(
        FEATURES_PATH
    )

    return model, feature_columns


# ============================================================
# LOAD MERCHANT
# ============================================================

def load_merchant(
    merchant_id,
    feature_columns,
):

    if not MERCHANT_DATA_PATH.exists():

        raise FileNotFoundError(
            f"Merchant dataset not found:\n"
            f"{MERCHANT_DATA_PATH}"
        )

    merchants = pd.read_csv(
        MERCHANT_DATA_PATH
    )

    if "merchant_id" not in merchants.columns:

        raise ValueError(
            "merchant_dataset.csv must contain "
            "'merchant_id'."
        )

    matches = merchants[
        merchants["merchant_id"].astype(str)
        == str(merchant_id)
    ]

    if matches.empty:

        raise ValueError(
            f"Merchant '{merchant_id}' "
            f"was not found."
        )

    merchant = matches.iloc[0]

    # Only use the exact 15 model features.
    merchant_features = (
        merchant[feature_columns]
        .astype(float)
        .to_frame()
        .T
    )

    return merchant, merchant_features


# ============================================================
# GENERATE SHAP EXPLANATION
# ============================================================

def explain_merchant(
    merchant_id,
):

    print(
        f"\nGenerating explanation "
        f"for merchant: {merchant_id}"
    )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model, feature_columns = (
        load_artifacts()
    )

    # --------------------------------------------------------
    # Load merchant
    # --------------------------------------------------------

    merchant, merchant_features = (
        load_merchant(
            merchant_id,
            feature_columns,
        )
    )

    # --------------------------------------------------------
    # Predict score
    # --------------------------------------------------------

    predicted_score = float(
        model.predict(
            merchant_features
        )[0]
    )

    # Keep score inside expected range
    predicted_score = max(
        0,
        min(
            1000,
            predicted_score,
        ),
    )

    # --------------------------------------------------------
    # SHAP
    # --------------------------------------------------------

    print("Calculating SHAP values...")

    explainer = shap.TreeExplainer(
        model
    )

    shap_explanation = explainer(
        merchant_features
    )

    shap_values = (
        shap_explanation.values[0]
    )

    base_value = float(
        shap_explanation.base_values[0]
    )

    # --------------------------------------------------------
    # Build explanation dataframe
    # --------------------------------------------------------

    explanation_df = pd.DataFrame({

        "feature": feature_columns,

        "feature_value": [
            float(
                merchant_features.iloc[0][feature]
            )
            for feature in feature_columns
        ],

        "shap_value": shap_values,

    })

    explanation_df[
        "absolute_impact"
    ] = explanation_df[
        "shap_value"
    ].abs()

    explanation_df = (
        explanation_df
        .sort_values(
            "absolute_impact",
            ascending=False,
        )
    )

    # --------------------------------------------------------
    # Positive / negative factors
    # --------------------------------------------------------

    positive = (
        explanation_df[
            explanation_df["shap_value"] > 0
        ]
        .head(5)
    )

    negative = (
        explanation_df[
            explanation_df["shap_value"] < 0
        ]
        .head(5)
    )

    positive_factors = []

    for _, row in positive.iterrows():

        positive_factors.append({

            "feature": row["feature"],

            "display_name":
                FEATURE_DISPLAY_NAMES.get(
                    row["feature"],
                    row["feature"],
                ),

            "value":
                float(row["feature_value"]),

            "impact":
                float(row["shap_value"]),

            "explanation":
                create_explanation_text(
                    row["feature"],
                    row["shap_value"],
                    row["feature_value"],
                ),
        })

    negative_factors = []

    for _, row in negative.iterrows():

        negative_factors.append({

            "feature": row["feature"],

            "display_name":
                FEATURE_DISPLAY_NAMES.get(
                    row["feature"],
                    row["feature"],
                ),

            "value":
                float(row["feature_value"]),

            "impact":
                float(row["shap_value"]),

            "explanation":
                create_explanation_text(
                    row["feature"],
                    row["shap_value"],
                    row["feature_value"],
                ),
        })

    # --------------------------------------------------------
    # SHAP waterfall plot
    # --------------------------------------------------------

    print("Generating waterfall plot...")

    plt.figure(
        figsize=(12, 8)
    )

    shap.plots.waterfall(
        shap_explanation[0],
        max_display=10,
        show=False,
    )

    plt.title(
        f"Why Merchant {merchant_id} "
        f"Received a Score of "
        f"{predicted_score:.0f}",
        fontsize=16,
        pad=20,
    )

    plt.tight_layout()

    plot_path = (
        OUTPUT_DIR
        / f"{merchant_id}_waterfall.png"
    )

    plt.savefig(
        plot_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    # --------------------------------------------------------
    # Save JSON
    # --------------------------------------------------------

    result = {

        "merchant_id":
            str(merchant_id),

        "credit_score":
            round(
                predicted_score,
                2,
            ),

        "shap_base_value":
            round(
                base_value,
                2,
            ),

        "positive_factors":
            positive_factors,

        "negative_factors":
            negative_factors,

        "waterfall_plot":
            str(plot_path),

    }

    json_path = (
        OUTPUT_DIR
        / f"{merchant_id}_explanation.json"
    )

    with open(
        json_path,
        "w",
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
        )

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        f"MERCHANT: {merchant_id}"
    )

    print(
        f"CREDIT SCORE: "
        f"{predicted_score:.0f}"
    )

    print(
        "=" * 70
    )

    print("\nPOSITIVE FACTORS:")

    for factor in positive_factors:

        print(
            f"  ↑ "
            f"{factor['display_name']}: "
            f"+{factor['impact']:.1f}"
        )

    print("\nRISK FACTORS:")

    for factor in negative_factors:

        print(
            f"  ↓ "
            f"{factor['display_name']}: "
            f"{factor['impact']:.1f}"
        )

    print("\nSaved:")

    print(
        f"  ✓ {plot_path}"
    )

    print(
        f"  ✓ {json_path}"
    )

    return result


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Generate SHAP explanation "
            "for a merchant."
        )
    )

    parser.add_argument(
        "--merchant-id",
        required=True,
        help="Merchant ID to explain",
    )

    args = parser.parse_args()

    explain_merchant(
        args.merchant_id
    )