import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score
)
from sklearn.utils.class_weight import compute_class_weight
from pathlib import Path

# Set Paths
results_path = Path(__file__).parent.parent.parent / "results"
results_path.mkdir(parents=True, exist_ok=True)  # create if needed

data_path = Path(__file__).parent.parent.parent / "data/final/ibm_df.csv"

# Load data
df = pd.read_csv(data_path, parse_dates=["Date"])

# a return under threshold is labeled not up
threshold = 0.005

# define prediction variable
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
        max_iter=1000, class_weight=class_weight_dict
    ),

    "Ridge Classifier": RidgeClassifier(),  
    
    "Naive Bayes": GaussianNB(),
    
    "KNN Classifier": KNeighborsClassifier(n_neighbors=5),
}



model_names = []
f1_minority_scores = []
accuracy_scores = []


# Train deploy, & evaluate model
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

    model_names.append(name)
    f1_minority_scores.append(f1_minority)
    accuracy_scores.append(acc)



# Bar plot of results
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = range(len(model_names))
bars1 = ax.bar(index, f1_minority_scores, bar_width, label='F1-score (Not Up)')
bars2 = ax.bar([i + bar_width for i in index], accuracy_scores, bar_width, label='Accuracy')

ax.set_xlabel('Model')
ax.set_ylabel('Score')
ax.set_title('Binary Classification Results for IBM Stock Movements')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(model_names)
ax.set_ylim(0, 1)
ax.legend()

# Annotate
for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f'{h:.2f}', 
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom'
        )

plt.tight_layout()
plt.savefig(results_path / "classification_results.png")
