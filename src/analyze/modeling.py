import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score
)


def modeling():
    data_path = Path(__file__).parent.parent.parent / "data/final/ibm_df.csv"

    # Load data
    df = pd.read_csv(data_path, parse_dates=["Date"])

    # threshold for defining target
    threshold = 0.005
    df["Target"] = (df["Return"] > threshold).astype(int)

    # Only inlcude variables that are known that day 
    features = [
        "Return_lag",
        "Return_3d_sum",
        "Return_7d_sum",
        "Volatility_3d",
        "Volatility_7d",
        "Interest_lag",
        'Prev_sentiment'
    ]

    X = df[features]
    y = df["Target"]


    # train-test split
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]



    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    # Handle imbalance in classes (for logistic reg, naive bayes and KNN)
    classes = np.unique(y_train)
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=classes,
        y=y_train
    )
    class_weight_dict = dict(zip(classes, class_weights))


    # Models to be tested
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight=class_weight_dict ),
        "Ridge Classifier": RidgeClassifier(),  
        "Naive Bayes": GaussianNB(),
        "KNN Classifier": KNeighborsClassifier(n_neighbors=5),
    }



    # performance storage
    results = []


    # train & evaluate
    for name, model in models.items():
        print(f"{name}:")
        
        # models that require scaling
        if name in ["Logistic Regression", "Ridge Classifier", "KNN Classifier"]:
            X_tr, X_te = X_train_scaled, X_test_scaled
        else:
            X_tr, X_te = X_train, X_test

        model.fit(X_tr, y_train)
        y_pred = model.predict(X_te)

        f1_minority = f1_score(y_test, y_pred, pos_label=0)
        acc = accuracy_score(y_test, y_pred)

        print(f"f1-score (Stock not up): {f1_minority:.4f}")
        print("Preformance Metrics:")
        print(classification_report(y_test, y_pred, digits=4))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        results.append({
            "Model": name,
            "F1_not_up": f1_minority,
            "Accuracy": acc,
        })

    results_df = pd.DataFrame(results)


    # Bar plot of results
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(results_df))

    ax.bar(index, results_df["F1_not_up"], bar_width, label="F1-score (Not Up)")
    ax.bar(
        [i + bar_width for i in index],
        results_df["Accuracy"],
        bar_width,
        label="Accuracy"
    )

    # annotate bars
    for i, row in results_df.iterrows():
        ax.annotate(f"{row['F1_not_up']:.2f}",
                    xy=(i, row['F1_not_up']),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")

        ax.annotate(f"{row['Accuracy']:.2f}",
                    xy=(i + bar_width, row['Accuracy']),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")

    plt.tight_layout()

    # RETURN, don't save
    return results_df, fig




if __name__ == "__main__":
    results_path = Path(__file__).parent.parent.parent / "results"
    results_path.mkdir(parents=True, exist_ok=True)

    results_df, fig = modeling()

    # save results
    fig.savefig(results_path / "classification_results.png")
    plt.close(fig)

    results_df.to_csv(results_path / "classification_results.csv", index=False)

    print("Modeling outputs saved to {results_path}.")