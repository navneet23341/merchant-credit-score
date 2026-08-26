from pathlib import Path
import json
import warnings

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

from sklearn.model_selection import (
    train_test_split,
    KFold,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    f1_score,
    accuracy_score,
    classification_report,
)
from xgboost import XGBRegressor, XGBClassifier


warnings.filterwarnings("ignore")


# ============================================================
# PATHS / CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "ml_training_data.csv"
ARTIFACT_DIR = BASE_DIR / "ml" / "artifacts"

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20
N_SPLITS = 5


# ============================================================
# EXACT 15 CREDIT SIGNALS
# ============================================================

FEATURE_COLUMNS = [
    "monthly_revenue",
    "revenue_growth_rate",
    "revenue_consistency",
    "refund_rate",
    "chargeback_rate",
    "settlement_velocity_days",
    "customer_repeat_rate",
    "payment_diversity_score",
    "peak_season_ratio",
    "failed_payment_rate",
    "avg_transaction_value",
    "transaction_volume_monthly",
    "dispute_resolution_rate",
    "late_settlement_frequency",
    "revenue_concentration_risk",
]

REGRESSION_TARGET = "credit_score"
CLASSIFICATION_TARGET = "credit_tier"


# ============================================================
# HELPERS
# ============================================================

def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ============================================================
# 1. LOAD DATA
# ============================================================

print_section("1. LOADING TRAINING DATA")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")

print("\nColumns:")
for column in df.columns:
    print(f"  - {column}")


# ============================================================
# 2. VALIDATE DATASET STRUCTURE
# ============================================================

print_section("2. VALIDATING DATASET")

required_columns = (
    FEATURE_COLUMNS
    + [
        REGRESSION_TARGET,
        CLASSIFICATION_TARGET,
    ]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "\nMissing required columns:\n"
        + "\n".join(
            f"  - {column}"
            for column in missing_columns
        )
    )


print(
    f"✓ Found all {len(FEATURE_COLUMNS)} signal features"
)

print(
    f"✓ Found regression target: {REGRESSION_TARGET}"
)

print(
    f"✓ Found classification target: {CLASSIFICATION_TARGET}"
)


# ============================================================
# 3. SELECT FEATURES AND TARGETS
# ============================================================

print_section("3. SELECTING MODEL FEATURES")

X = df[FEATURE_COLUMNS].copy()

y_regression = df[
    REGRESSION_TARGET
].copy()

y_classification = df[
    CLASSIFICATION_TARGET
].copy()


print("\nFeatures used by model:")

for i, feature in enumerate(FEATURE_COLUMNS, start=1):
    print(f"{i:2}. {feature}")


# ============================================================
# 4. DATA CLEANING
# ============================================================

print_section("4. CLEANING DATA")

# Convert all 15 signals to numeric
for feature in FEATURE_COLUMNS:

    X[feature] = pd.to_numeric(
        X[feature],
        errors="coerce",
    )


# Replace infinite values
X = X.replace(
    [np.inf, -np.inf],
    np.nan,
)


# Make score numeric
y_regression = pd.to_numeric(
    y_regression,
    errors="coerce",
)


# Remove invalid rows
valid_rows = (
    X.notna().all(axis=1)
    & y_regression.notna()
    & y_classification.notna()
)

invalid_count = (~valid_rows).sum()

if invalid_count > 0:

    print(
        f"Removing {invalid_count} invalid rows."
    )

    X = X.loc[valid_rows]

    y_regression = (
        y_regression.loc[valid_rows]
    )

    y_classification = (
        y_classification.loc[valid_rows]
    )


# Reset indices
X = X.reset_index(drop=True)

y_regression = (
    y_regression.reset_index(drop=True)
)

y_classification = (
    y_classification.reset_index(drop=True)
)


print(
    f"✓ Final dataset: {len(X)} merchants"
)


# ============================================================
# 5. CHECK CLASS DISTRIBUTION
# ============================================================

print_section("5. CREDIT TIER DISTRIBUTION")

tier_distribution = (
    y_classification.value_counts()
)

print(tier_distribution)

print("\nPercentages:")

print(
    (
        y_classification.value_counts(
            normalize=True
        ) * 100
    ).round(2)
)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

print_section("6. TRAIN / TEST SPLIT")

(
    X_train,
    X_test,
    y_reg_train,
    y_reg_test,
    y_cls_train,
    y_cls_test,
) = train_test_split(

    X,
    y_regression,
    y_classification,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y_classification,
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples:  {len(X_test)}"
)


# ============================================================
# 7. ENCODE CREDIT TIERS
# ============================================================

print_section("7. ENCODING CREDIT TIERS")

tier_labels = sorted(
    y_classification.unique()
)

tier_to_id = {
    tier: index
    for index, tier in enumerate(tier_labels)
}

id_to_tier = {
    index: tier
    for tier, index in tier_to_id.items()
}


print("Tier mapping:")

for tier, index in tier_to_id.items():
    print(f"  {index} → {tier}")


y_cls_train_encoded = (
    y_cls_train.map(tier_to_id)
)

y_cls_test_encoded = (
    y_cls_test.map(tier_to_id)
)


# ============================================================
# 8. CREATE REGRESSION MODEL
# ============================================================

print_section("8. BUILDING REGRESSION MODEL")

regression_model = XGBRegressor(

    n_estimators=400,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.85,

    colsample_bytree=0.85,

    objective="reg:squarederror",

    eval_metric="rmse",

    random_state=RANDOM_STATE,

    n_jobs=-1,
)


# ============================================================
# 9. CREATE CLASSIFICATION MODEL
# ============================================================

print_section("9. BUILDING CLASSIFICATION MODEL")

classification_model = XGBClassifier(

    n_estimators=400,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.85,

    colsample_bytree=0.85,

    objective="multi:softprob",

    num_class=len(tier_labels),

    eval_metric="mlogloss",

    random_state=RANDOM_STATE,

    n_jobs=-1,
)


# ============================================================
# 10. 5-FOLD CV — REGRESSION
# ============================================================

print_section(
    "10. 5-FOLD CROSS VALIDATION — REGRESSION"
)

reg_cv = KFold(

    n_splits=N_SPLITS,

    shuffle=True,

    random_state=RANDOM_STATE,
)


reg_cv_scores = np.sqrt(

    -cross_val_score(

        regression_model,

        X_train,

        y_reg_train,

        cv=reg_cv,

        scoring="neg_mean_squared_error",

        n_jobs=-1,
    )
)


print("\nFold RMSE:")

for i, score in enumerate(
    reg_cv_scores,
    start=1,
):

    print(
        f"  Fold {i}: {score:.4f}"
    )


reg_cv_mean = reg_cv_scores.mean()

reg_cv_std = reg_cv_scores.std()


print(
    f"\nMean CV RMSE: {reg_cv_mean:.4f}"
)

print(
    f"CV RMSE Std:  {reg_cv_std:.4f}"
)


# ============================================================
# 11. 5-FOLD CV — CLASSIFICATION
# ============================================================

print_section(
    "11. 5-FOLD CROSS VALIDATION — CLASSIFICATION"
)

cls_cv = StratifiedKFold(

    n_splits=N_SPLITS,

    shuffle=True,

    random_state=RANDOM_STATE,
)


cls_cv_scores = cross_val_score(

    classification_model,

    X_train,

    y_cls_train_encoded,

    cv=cls_cv,

    scoring="f1_macro",

    n_jobs=-1,
)


print("\nFold Macro F1:")

for i, score in enumerate(
    cls_cv_scores,
    start=1,
):

    print(
        f"  Fold {i}: {score:.4f}"
    )


cls_cv_mean = cls_cv_scores.mean()

cls_cv_std = cls_cv_scores.std()


print(
    f"\nMean CV Macro F1: {cls_cv_mean:.4f}"
)

print(
    f"CV F1 Std:        {cls_cv_std:.4f}"
)


# ============================================================
# 12. TRAIN FINAL REGRESSION MODEL
# ============================================================

print_section(
    "12. TRAINING FINAL REGRESSION MODEL"
)

regression_model.fit(

    X_train,

    y_reg_train,
)


# ============================================================
# 13. TRAIN FINAL CLASSIFICATION MODEL
# ============================================================

print_section(
    "13. TRAINING FINAL CLASSIFICATION MODEL"
)

classification_model.fit(

    X_train,

    y_cls_train_encoded,
)


# ============================================================
# 14. REGRESSION TEST METRICS
# ============================================================

print_section(
    "14. REGRESSION — HOLDOUT TEST"
)

reg_predictions = (
    regression_model.predict(X_test)
)


rmse = np.sqrt(
    mean_squared_error(
        y_reg_test,
        reg_predictions,
    )
)


mae = mean_absolute_error(
    y_reg_test,
    reg_predictions,
)


r2 = r2_score(
    y_reg_test,
    reg_predictions,
)


print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R²:   {r2:.4f}")


# ============================================================
# 15. CLASSIFICATION TEST METRICS
# ============================================================

print_section(
    "15. CLASSIFICATION — HOLDOUT TEST"
)

cls_predictions_encoded = (
    classification_model.predict(X_test)
)


cls_predictions = [

    id_to_tier[int(prediction)]

    for prediction
    in cls_predictions_encoded

]


macro_f1 = f1_score(

    y_cls_test,

    cls_predictions,

    average="macro",
)


weighted_f1 = f1_score(

    y_cls_test,

    cls_predictions,

    average="weighted",
)


accuracy = accuracy_score(

    y_cls_test,

    cls_predictions,
)


print(
    f"Macro F1:    {macro_f1:.4f}"
)

print(
    f"Weighted F1: {weighted_f1:.4f}"
)

print(
    f"Accuracy:    {accuracy:.4f}"
)


print("\nClassification Report:")

print(
    classification_report(

        y_cls_test,

        cls_predictions,

        zero_division=0,
    )
)


# ============================================================
# 16. SAVE METRICS
# ============================================================

print_section(
    "16. SAVING METRICS"
)


metrics = {

    "model_version": "1.0",

    "random_state": RANDOM_STATE,

    "dataset": {

        "total_samples": int(len(X)),

        "training_samples": int(
            len(X_train)
        ),

        "test_samples": int(
            len(X_test)
        ),

        "feature_count": len(
            FEATURE_COLUMNS
        ),

        "features": FEATURE_COLUMNS,
    },

    "regression": {

        "model": "XGBRegressor",

        "cross_validation": {

            "folds": N_SPLITS,

            "rmse_mean": float(
                reg_cv_mean
            ),

            "rmse_std": float(
                reg_cv_std
            ),

            "fold_rmse": [

                float(score)

                for score
                in reg_cv_scores

            ],
        },

        "holdout_test": {

            "rmse": float(rmse),

            "mae": float(mae),

            "r2": float(r2),
        },
    },

    "classification": {

        "model": "XGBClassifier",

        "classes": tier_labels,

        "cross_validation": {

            "folds": N_SPLITS,

            "macro_f1_mean": float(
                cls_cv_mean
            ),

            "macro_f1_std": float(
                cls_cv_std
            ),

            "fold_macro_f1": [

                float(score)

                for score
                in cls_cv_scores

            ],
        },

        "holdout_test": {

            "macro_f1": float(
                macro_f1
            ),

            "weighted_f1": float(
                weighted_f1
            ),

            "accuracy": float(
                accuracy
            ),
        },
    },
}


save_json(

    metrics,

    ARTIFACT_DIR
    / "metrics.json",
)


# ============================================================
# 17. SAVE MODELS
# ============================================================

print_section(
    "17. SAVING MODELS"
)


joblib.dump(

    regression_model,

    ARTIFACT_DIR
    / "regression_model.pkl",
)


joblib.dump(

    classification_model,

    ARTIFACT_DIR
    / "classification_model.pkl",
)


# Backend default model
joblib.dump(

    regression_model,

    ARTIFACT_DIR
    / "model.pkl",
)


# Save exact feature ordering
joblib.dump(

    FEATURE_COLUMNS,

    ARTIFACT_DIR
    / "feature_columns.pkl",
)


# Save tier mapping
joblib.dump(

    {
        "tier_to_id": tier_to_id,

        "id_to_tier": id_to_tier,
    },

    ARTIFACT_DIR
    / "tier_mapping.pkl",
)


print(
    "✓ regression_model.pkl"
)

print(
    "✓ classification_model.pkl"
)

print(
    "✓ model.pkl"
)

print(
    "✓ feature_columns.pkl"
)

print(
    "✓ tier_mapping.pkl"
)


# ============================================================
# 18. SHAP EXPLAINABILITY
# ============================================================

print_section(
    "18. SHAP ANALYSIS"
)


explainer = shap.TreeExplainer(

    regression_model
)


shap_values = explainer.shap_values(

    X_test
)


# ------------------------------------------------------------
# Save SHAP values
# ------------------------------------------------------------

shap_df = pd.DataFrame(

    shap_values,

    columns=FEATURE_COLUMNS,
)


shap_df.to_csv(

    ARTIFACT_DIR
    / "shap_values.csv",

    index=False,
)


# ------------------------------------------------------------
# SHAP SUMMARY PLOT
# ------------------------------------------------------------

plt.figure()

shap.summary_plot(

    shap_values,

    X_test,

    show=False,
)


plt.title(
    "SHAP Feature Impact — Credit Score"
)


plt.tight_layout()


plt.savefig(

    ARTIFACT_DIR
    / "shap_summary.png",

    dpi=200,

    bbox_inches="tight",
)


plt.close()


print(
    "✓ shap_summary.png"
)


# ============================================================
# 19. FEATURE IMPORTANCE
# ============================================================

print_section(
    "19. FEATURE IMPORTANCE"
)


importance_df = pd.DataFrame({

    "feature": FEATURE_COLUMNS,

    "importance":
        regression_model.feature_importances_,

})


importance_df = (
    importance_df
    .sort_values(
        "importance",
        ascending=True,
    )
)


plt.figure(
    figsize=(10, 7)
)


plt.barh(

    importance_df["feature"],

    importance_df["importance"],
)


plt.xlabel(
    "XGBoost Feature Importance"
)

plt.ylabel(
    "Credit Signal"
)

plt.title(
    "Feature Importance — Credit Score"
)


plt.tight_layout()


plt.savefig(

    ARTIFACT_DIR
    / "feature_importance.png",

    dpi=200,

    bbox_inches="tight",
)


plt.close()


print(
    "✓ feature_importance.png"
)


# ============================================================
# 20. SAVE TEST PREDICTIONS
# ============================================================

print_section(
    "20. SAVING TEST PREDICTIONS"
)


predictions_df = X_test.copy()


predictions_df[
    "actual_credit_score"
] = y_reg_test.values


predictions_df[
    "predicted_credit_score"
] = reg_predictions


predictions_df[
    "score_error"
] = (
    y_reg_test.values
    - reg_predictions
)


predictions_df[
    "actual_credit_tier"
] = y_cls_test.values


predictions_df[
    "predicted_credit_tier"
] = cls_predictions


predictions_df.to_csv(

    ARTIFACT_DIR
    / "test_predictions.csv",

    index=False,
)


print(
    "✓ test_predictions.csv"
)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print_section(
    "MODEL TRAINING COMPLETE 🚀"
)


print("\nREGRESSION")
print(
    f"  CV RMSE:   {reg_cv_mean:.4f}"
)
print(
    f"  Test RMSE: {rmse:.4f}"
)
print(
    f"  Test MAE:  {mae:.4f}"
)
print(
    f"  Test R²:   {r2:.4f}"
)


print("\nCLASSIFICATION")
print(
    f"  CV Macro F1:   {cls_cv_mean:.4f}"
)
print(
    f"  Test Macro F1: {macro_f1:.4f}"
)
print(
    f"  Test Accuracy:  {accuracy:.4f}"
)


print("\nARTIFACTS")

for artifact in sorted(
    ARTIFACT_DIR.iterdir()
):

    print(
        f"  ✓ {artifact.name}"
    )


print(
    "\nEverything ready for backend integration."
)