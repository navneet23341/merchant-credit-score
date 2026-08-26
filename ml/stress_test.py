from pathlib import Path
import argparse
import json

import joblib
import pandas as pd


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

MODEL_PATH = (
    ARTIFACT_DIR / "regression_model.pkl"
)

FEATURES_PATH = (
    ARTIFACT_DIR / "feature_columns.pkl"
)

OUTPUT_DIR = (
    ARTIFACT_DIR / "stress_tests"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# FEATURE DISPLAY NAMES
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
# BUSINESS DIRECTION
# ============================================================

# Features where LOWER values generally indicate
# better merchant performance.

LOWER_IS_BETTER = {

    "refund_rate",

    "chargeback_rate",

    "settlement_velocity_days",

    "failed_payment_rate",

    "late_settlement_frequency",

    "revenue_concentration_risk",
}


# Features where HIGHER values generally indicate
# better merchant performance.

HIGHER_IS_BETTER = {

    "monthly_revenue",

    "revenue_growth_rate",

    "revenue_consistency",

    "customer_repeat_rate",

    "payment_diversity_score",

    "dispute_resolution_rate",

    "transaction_volume_monthly",
}


# ============================================================
# LOAD ARTIFACTS
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
# LOAD DATA
# ============================================================

def load_dataset():

    df = pd.read_csv(
        MERCHANT_DATA_PATH
    )

    return df


# ============================================================
# FIND HEALTHY MERCHANTS
# ============================================================

def get_high_quality_merchants(
    df,
):

    # Use the top 25% of merchants by
    # actual credit score as the benchmark group.

    threshold = df[
        "credit_score"
    ].quantile(0.75)

    high_quality = df[
        df["credit_score"] >= threshold
    ].copy()

    return (
        high_quality,
        threshold,
    )


# ============================================================
# CALCULATE DATA-DRIVEN BENCHMARKS
# ============================================================

def calculate_benchmarks(
    high_quality,
    feature_columns,
):

    benchmarks = {}

    for feature in feature_columns:

        if feature not in high_quality.columns:
            continue

        values = pd.to_numeric(
            high_quality[feature],
            errors="coerce",
        ).dropna()

        if values.empty:
            continue

        # ----------------------------------------------------
        # Higher is better:
        # use 75th percentile of high-quality merchants.
        # ----------------------------------------------------

        if feature in HIGHER_IS_BETTER:

            benchmark = values.quantile(
                0.75
            )

        # ----------------------------------------------------
        # Lower is better:
        # use 25th percentile of high-quality merchants.
        # ----------------------------------------------------

        elif feature in LOWER_IS_BETTER:

            benchmark = values.quantile(
                0.25
            )

        else:
            continue

        benchmarks[feature] = float(
            benchmark
        )

    return benchmarks


# ============================================================
# LOAD MERCHANT
# ============================================================

def get_merchant(
    df,
    merchant_id,
):

    matches = df[
        df["merchant_id"].astype(str)
        == str(merchant_id)
    ]

    if matches.empty:

        raise ValueError(
            f"Merchant '{merchant_id}' "
            f"not found."
        )

    return matches.iloc[0]


# ============================================================
# CREATE FEATURE VECTOR
# ============================================================

def get_feature_vector(
    merchant,
    feature_columns,
):

    features = (
        merchant[feature_columns]
        .astype(float)
        .to_frame()
        .T
    )

    return features


# ============================================================
# PREDICT SCORE
# ============================================================

def predict_score(
    model,
    features,
):

    score = float(
        model.predict(features)[0]
    )

    # Keep score inside the expected
    # 0–1000 range.

    return max(
        0,
        min(
            1000,
            score,
        ),
    )


# ============================================================
# CHECK WHETHER BENCHMARK IS ACTUALLY BETTER
# ============================================================

def is_improvement(
    feature,
    current_value,
    benchmark,
):

    if feature in HIGHER_IS_BETTER:

        return benchmark > current_value

    if feature in LOWER_IS_BETTER:

        return benchmark < current_value

    return False


# ============================================================
# FORMAT VALUES
# ============================================================

def format_value(
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
        "late_settlement_frequency",
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

    if feature == "payment_diversity_score":

        return f"{value:.2f}"

    return f"{value:.2f}"


# ============================================================
# RUN STRESS TEST
# ============================================================

def stress_test(
    merchant_id,
):

    print(
        "\n" + "=" * 70
    )

    print(
        f"STRESS TEST — {merchant_id}"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Load model + features
    # --------------------------------------------------------

    model, feature_columns = (
        load_artifacts()
    )

    # --------------------------------------------------------
    # Load merchant dataset
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # Find benchmark population
    # --------------------------------------------------------

    (
        high_quality,
        score_threshold,
    ) = get_high_quality_merchants(
        df
    )

    print(
        f"Benchmark population: "
        f"{len(high_quality)} merchants"
    )

    print(
        f"High-quality threshold: "
        f"{score_threshold:.1f} credit score"
    )

    # --------------------------------------------------------
    # Calculate benchmarks
    # --------------------------------------------------------

    benchmarks = calculate_benchmarks(
        high_quality,
        feature_columns,
    )

    # --------------------------------------------------------
    # Get requested merchant
    # --------------------------------------------------------

    merchant = get_merchant(
        df,
        merchant_id,
    )

    current_features = (
        get_feature_vector(
            merchant,
            feature_columns,
        )
    )

    # --------------------------------------------------------
    # Current score
    # --------------------------------------------------------

    current_score = predict_score(
        model,
        current_features,
    )

    print(
        f"\nCurrent Score: "
        f"{current_score:.0f}"
    )

    # --------------------------------------------------------
    # Test every feature
    # --------------------------------------------------------

    scenarios = []

    for feature in feature_columns:

        if feature not in benchmarks:
            continue

        current_value = float(
            current_features.iloc[0][feature]
        )

        benchmark = benchmarks[
            feature
        ]

        # ----------------------------------------------------
        # Only test benchmark if it represents
        # an actual improvement.
        # ----------------------------------------------------

        if not is_improvement(
            feature,
            current_value,
            benchmark,
        ):
            continue

        # ----------------------------------------------------
        # Create hypothetical merchant
        # ----------------------------------------------------

        hypothetical = (
            current_features.copy()
        )

        hypothetical.loc[
            hypothetical.index[0],
            feature,
        ] = benchmark

        # ----------------------------------------------------
        # Predict hypothetical score
        # ----------------------------------------------------

        projected_score = predict_score(
            model,
            hypothetical,
        )

        score_change = (
            projected_score
            - current_score
        )

        # ----------------------------------------------------
        # Only keep scenarios that
        # actually improve the score.
        # ----------------------------------------------------

        if score_change <= 0:
            continue

        scenarios.append({

            "feature":
                feature,

            "display_name":
                FEATURE_DISPLAY_NAMES.get(
                    feature,
                    feature,
                ),

            "current_value":
                round(
                    current_value,
                    6,
                ),

            "benchmark_value":
                round(
                    benchmark,
                    6,
                ),

            "current_value_display":
                format_value(
                    feature,
                    current_value,
                ),

            "benchmark_value_display":
                format_value(
                    feature,
                    benchmark,
                ),

            "current_score":
                round(
                    current_score,
                    2,
                ),

            "projected_score":
                round(
                    projected_score,
                    2,
                ),

            "score_improvement":
                round(
                    score_change,
                    2,
                ),

            "benchmark_definition":
                (
                    "Benchmark derived from "
                    "high-quality merchants "
                    "(top 25% by credit score)."
                ),

        })

    # --------------------------------------------------------
    # Rank by score improvement
    # --------------------------------------------------------

    scenarios.sort(
        key=lambda x:
            x["score_improvement"],
        reverse=True,
    )

    top_3 = scenarios[:3]

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print(
        "\nTOP DATA-DRIVEN IMPROVEMENTS"
    )

    print(
        "-" * 70
    )

    if not top_3:

        print(
            "\nNo benchmark-based improvements "
            "were found."
        )

    for index, scenario in enumerate(
        top_3,
        start=1,
    ):

        print(
            f"\n{index}. "
            f"{scenario['display_name']}"
        )

        print(
            f"   Current: "
            f"{scenario['current_value_display']}"
        )

        print(
            f"   Healthy benchmark: "
            f"{scenario['benchmark_value_display']}"
        )

        print(
            f"   Score: "
            f"{scenario['current_score']:.0f}"
            f" → "
            f"{scenario['projected_score']:.0f}"
        )

        print(
            f"   Potential improvement: "
            f"+{scenario['score_improvement']:.1f} points"
        )

    # ========================================================
    # SAVE JSON
    # ========================================================

    result = {

        "merchant_id":
            str(merchant_id),

        "current_score":
            round(
                current_score,
                2,
            ),

        "benchmark_method":
            (
                "Top 25% of merchants "
                "by credit score"
            ),

        "benchmark_score_threshold":
            round(
                score_threshold,
                2,
            ),

        "benchmark_population_size":
            len(high_quality),

        "top_improvements":
            top_3,

        "all_scenarios":
            scenarios,

    }

    output_path = (
        OUTPUT_DIR
        / f"{merchant_id}_stress_test.json"
    )

    with open(
        output_path,
        "w",
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
        )

    print(
        "\nSaved:"
    )

    print(
        f"  ✓ {output_path}"
    )

    return result


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Run data-driven "
            "counterfactual stress testing."
        )
    )

    parser.add_argument(
        "--merchant-id",
        required=True,
        help="Merchant ID",
    )

    args = parser.parse_args()

    stress_test(
        args.merchant_id
    )