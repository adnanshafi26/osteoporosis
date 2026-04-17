import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "osteoporosis_dataset_10000_final.csv"
OUTPUT_DIR = BASE_DIR / "static" / "graphs"


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    required_cols = {
        "age",
        "gender",
        "bmi",
        "bone_density",
        "bone_type",
        "calcium",
        "vitamin_d",
        "label",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return df


def add_readable_labels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["risk"] = out["label"].map({0: "Low Risk", 1: "High Risk"}).fillna("Unknown")
    out["gender_name"] = out["gender"].map({0: "Female", 1: "Male"}).fillna("Other")
    out["bone_type_name"] = out["bone_type"].map({0: "Type-0", 1: "Type-1", 2: "Type-2", 3: "Type-3"})
    return out


def save_class_distribution(df: pd.DataFrame) -> None:
    counts = df["risk"].value_counts().reindex(["Low Risk", "High Risk"], fill_value=0)

    plt.figure(figsize=(8, 5))
    colors = ["#2E8B57", "#C0392B"]
    bars = plt.bar(counts.index, counts.values, color=colors)
    plt.title("Osteoporosis Risk Distribution")
    plt.xlabel("Risk Class")
    plt.ylabel("Number of Patients")

    for bar in bars:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, y + max(counts.values) * 0.01, f"{int(y)}", ha="center")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "risk_distribution.png", dpi=180)
    plt.close()


def save_age_group_risk(df: pd.DataFrame) -> None:
    bins = [20, 30, 40, 50, 60, 70, 80, 90]
    labels = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89"]

    age_groups = pd.cut(df["age"], bins=bins, labels=labels, include_lowest=True, right=False)
    risk_rate = df.groupby(age_groups, observed=False)["label"].mean() * 100

    plt.figure(figsize=(10, 5))
    plt.plot(risk_rate.index.astype(str), risk_rate.values, marker="o", linewidth=2, color="#1F77B4")
    plt.title("High-Risk Percentage by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("High-Risk Patients (%)")
    plt.ylim(0, min(100, max(5, np.nanmax(risk_rate.values) + 5)))
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "age_group_risk_rate.png", dpi=180)
    plt.close()


def save_bone_density_by_risk(df: pd.DataFrame) -> None:
    low = df.loc[df["risk"] == "Low Risk", "bone_density"]
    high = df.loc[df["risk"] == "High Risk", "bone_density"]

    plt.figure(figsize=(10, 5))
    plt.hist(low, bins=35, alpha=0.7, label="Low Risk", color="#2E8B57")
    plt.hist(high, bins=35, alpha=0.7, label="High Risk", color="#C0392B")
    plt.title("Bone Density Distribution by Risk Class")
    plt.xlabel("Bone Density")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bone_density_by_risk.png", dpi=180)
    plt.close()


def save_bmi_boxplot(df: pd.DataFrame) -> None:
    low = df.loc[df["risk"] == "Low Risk", "bmi"]
    high = df.loc[df["risk"] == "High Risk", "bmi"]

    plt.figure(figsize=(8, 5))
    plt.boxplot([low, high], tick_labels=["Low Risk", "High Risk"], patch_artist=True)
    plt.title("BMI Spread by Risk Class")
    plt.ylabel("BMI")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bmi_boxplot_by_risk.png", dpi=180)
    plt.close()


def save_calcium_vitamin_scatter(df: pd.DataFrame) -> None:
    low = df[df["risk"] == "Low Risk"]
    high = df[df["risk"] == "High Risk"]

    plt.figure(figsize=(9, 6))
    plt.scatter(low["calcium"], low["vitamin_d"], s=15, alpha=0.5, label="Low Risk", color="#2E8B57")
    plt.scatter(high["calcium"], high["vitamin_d"], s=15, alpha=0.5, label="High Risk", color="#C0392B")
    plt.title("Calcium vs Vitamin D by Risk Class")
    plt.xlabel("Calcium")
    plt.ylabel("Vitamin D")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "calcium_vs_vitamin_d_scatter.png", dpi=180)
    plt.close()


def save_bone_type_stacked_bar(df: pd.DataFrame) -> None:
    pivot = (
        df.pivot_table(index="bone_type_name", columns="risk", values="id", aggfunc="count", fill_value=0)
        .reindex(["Type-0", "Type-1", "Type-2", "Type-3"])
        .fillna(0)
    )

    low_vals = pivot.get("Low Risk", pd.Series([0] * len(pivot), index=pivot.index))
    high_vals = pivot.get("High Risk", pd.Series([0] * len(pivot), index=pivot.index))

    plt.figure(figsize=(9, 5))
    plt.bar(pivot.index, low_vals, label="Low Risk", color="#2E8B57")
    plt.bar(pivot.index, high_vals, bottom=low_vals, label="High Risk", color="#C0392B")
    plt.title("Risk Distribution Across Bone Types")
    plt.xlabel("Bone Type")
    plt.ylabel("Number of Patients")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "risk_by_bone_type_stacked.png", dpi=180)
    plt.close()


def save_correlation_heatmap(df: pd.DataFrame) -> None:
    numeric_cols = ["age", "bmi", "bone_density", "calcium", "vitamin_d", "label"]
    corr = df[numeric_cols].corr()

    plt.figure(figsize=(8, 6))
    im = plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=30, ha="right")
    plt.yticks(range(len(numeric_cols)), numeric_cols)
    plt.title("Feature Correlation Heatmap")

    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_correlation_heatmap.png", dpi=180)
    plt.close()


def save_fracture_dataset_counts(project_root: Path) -> None:
    fracture_root = project_root / "BoneFractureDataset"
    subsets = ["training", "testing"]
    classes = ["fractured", "not_fractured"]

    counts = []
    for subset in subsets:
        for cls in classes:
            cls_dir = fracture_root / subset / cls
            if cls_dir.exists():
                image_count = len([p for p in cls_dir.iterdir() if p.is_file()])
            else:
                image_count = 0
            counts.append({"subset": subset, "class": cls, "count": image_count})

    data = pd.DataFrame(counts)

    if data["count"].sum() == 0:
        return

    train = data[data["subset"] == "training"].set_index("class")["count"]
    test = data[data["subset"] == "testing"].set_index("class")["count"]

    classes_order = ["fractured", "not_fractured"]
    train = train.reindex(classes_order, fill_value=0)
    test = test.reindex(classes_order, fill_value=0)

    x = np.arange(len(classes_order))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x - width / 2, train.values, width, label="Training", color="#4C78A8")
    plt.bar(x + width / 2, test.values, width, label="Testing", color="#F58518")
    plt.xticks(x, ["Fractured", "Not Fractured"])
    plt.title("Fracture X-ray Image Counts by Subset")
    plt.ylabel("Number of Images")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fracture_dataset_counts.png", dpi=180)
    plt.close()


def get_model_predictions(df: pd.DataFrame):
    features = ["age", "gender", "bmi", "bone_density", "bone_type", "calcium", "vitamin_d"]
    target = "label"

    x = df[features]
    y = df[target]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=250,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    return y_test.to_numpy(), y_pred, y_prob


def save_71_osteoporosis_prediction_results(y_true: np.ndarray, y_pred: np.ndarray) -> None:
    true_counts = pd.Series(y_true).value_counts().reindex([0, 1], fill_value=0)
    pred_counts = pd.Series(y_pred).value_counts().reindex([0, 1], fill_value=0)

    x_labels = ["Low Risk", "High Risk"]
    x = np.arange(len(x_labels))
    width = 0.35

    plt.figure(figsize=(9, 5.5))
    plt.bar(x - width / 2, true_counts.values, width, label="Actual", color="#4C78A8")
    plt.bar(x + width / 2, pred_counts.values, width, label="Predicted", color="#F58518")
    plt.xticks(x, x_labels)
    plt.ylabel("Number of Patients")
    plt.title("7.1 Osteoporosis Prediction Results")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "7_1_osteoporosis_prediction_results.png", dpi=180)
    plt.close()


def save_72_model_accuracy_performance_analysis(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> None:
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_prob)

    fpr, tpr, _ = roc_curve(y_true, y_prob)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    metric_names = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    metric_vals = [accuracy, precision, recall, f1, auc]
    bars = axes[0].bar(metric_names, metric_vals, color=["#2E8B57", "#1F77B4", "#F58518", "#C0392B", "#7F3C8D"])
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("Score")
    axes[0].set_title("Performance Metrics")
    axes[0].tick_params(axis="x", rotation=20)
    for bar in bars:
        val = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.3f}", ha="center", fontsize=9)

    axes[1].plot(fpr, tpr, color="#1F77B4", linewidth=2, label=f"ROC Curve (AUC = {auc:.3f})")
    axes[1].plot([0, 1], [0, 1], "--", color="#888888", label="Random Classifier")
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].set_title("ROC Curve")
    axes[1].legend(loc="lower right")
    axes[1].grid(alpha=0.25)

    fig.suptitle("7.2 Model Accuracy and Performance Analysis", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "7_2_model_accuracy_and_performance_analysis.png", dpi=180)
    plt.close(fig)


def save_73_osteoporosis_risk_assessment_output(y_prob: np.ndarray) -> None:
    # Convert model probabilities to report-friendly risk levels.
    bins = [0.0, 0.35, 0.7, 1.000001]
    labels = ["Low", "Medium", "High"]
    risk_levels = pd.cut(y_prob, bins=bins, labels=labels, include_lowest=True, right=False)
    counts = pd.Series(risk_levels).value_counts().reindex(labels, fill_value=0)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    axes[0].hist(y_prob, bins=30, color="#4C78A8", alpha=0.85, edgecolor="white")
    axes[0].axvline(0.35, color="#F58518", linestyle="--", linewidth=2, label="Low/Medium Threshold")
    axes[0].axvline(0.70, color="#C0392B", linestyle="--", linewidth=2, label="Medium/High Threshold")
    axes[0].set_xlabel("Predicted Risk Probability")
    axes[0].set_ylabel("Patient Count")
    axes[0].set_title("Risk Probability Distribution")
    axes[0].legend()

    bar_colors = ["#2E8B57", "#F2B134", "#C0392B"]
    bars = axes[1].bar(labels, counts.values, color=bar_colors)
    axes[1].set_ylabel("Patient Count")
    axes[1].set_title("Risk Category Summary")
    for bar in bars:
        val = int(bar.get_height())
        axes[1].text(bar.get_x() + bar.get_width() / 2, val + max(counts.values) * 0.01, str(val), ha="center")

    fig.suptitle("7.3 Osteoporosis Risk Assessment Output", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "7_3_osteoporosis_risk_assessment_output.png", dpi=180)
    plt.close(fig)


def main() -> None:
    ensure_output_dir()
    df = add_readable_labels(load_dataset())

    save_class_distribution(df)
    save_age_group_risk(df)
    save_bone_density_by_risk(df)
    save_bmi_boxplot(df)
    save_calcium_vitamin_scatter(df)
    save_bone_type_stacked_bar(df)
    save_correlation_heatmap(df)

    project_root = BASE_DIR.parent
    save_fracture_dataset_counts(project_root)

    y_true, y_pred, y_prob = get_model_predictions(df)
    save_71_osteoporosis_prediction_results(y_true, y_pred)
    save_72_model_accuracy_performance_analysis(y_true, y_pred, y_prob)
    save_73_osteoporosis_risk_assessment_output(y_prob)

    print(f"Graphs generated successfully in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()