import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    average_precision_score,
    precision_score,
    recall_score,
)
import lightgbm as lgb


def create_sample_data():
    """创建示例数据"""
    np.random.seed(42)
    n_samples = 5000
    data = pd.DataFrame(
        {
            "time_spent_A": np.random.exponential(10, n_samples),
            "time_spent_B": np.random.exponential(8, n_samples),
            "time_spent_C": np.random.exponential(12, n_samples),
            "category_presented": np.random.choice(["A", "B", "C"], n_samples),
            "clicked": np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
        }
    )
    return data


# 2. 数据加载
# data = pd.read_csv("your_data.csv")
data = create_sample_data()
data["category_presented"] = data["category_presented"].astype("category")


# 3. 特征工程
def create_features(df):
    X = df.copy()

    # 核心特征（必须记住的）
    X["total_time"] = X["time_spent_A"] + X["time_spent_B"] + X["time_spent_C"]
    X["ratio_A"] = X["time_spent_A"] / X["total_time"]
    X["is_matched"] = (
        X[["time_spent_A", "time_spent_B", "time_spent_C"]]
        .idxmax(axis=1)
        .str.replace("time_spent_", "")
        == X["category_presented"]
    ).astype(int)
    X["time_on_presented"] = np.select(
        [
            X["category_presented"] == "A",
            X["category_presented"] == "B",
            X["category_presented"] == "C",
        ],
        [X["time_spent_A"], X["time_spent_B"], X["time_spent_C"]],
        default=0,
    )
    X["ratio_on_presented"] = X["time_on_presented"] / X["total_time"]

    return X


# 4. 数据划分
X = data[["time_spent_A", "time_spent_B", "time_spent_C", "category_presented"]]
y = data["clicked"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train_feat = create_features(X_train)
X_test_feat = create_features(X_test)

# 5. 模型训练
model = lgb.LGBMClassifier(
    objective="binary",
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    verbosity=-1,
)
model.fit(X_train_feat, y_train)

# 6. 模型评估
y_pred = model.predict(X_test_feat)
y_pred_proba = model.predict_proba(X_test_feat)[:, 1]

# 基础指标
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)  # 重命名变量避免冲突

# PR-AUC相关计算
avg_precision = average_precision_score(y_test, y_pred_proba)

# 评估不同阈值下的表现
thresholds_to_test = [0.2, 0.4, 0.5, 0.6, 0.8]
print("不同阈值下的性能指标:")
print("阈值\t精确率\t召回率\tF1分数\tFPR\tTPR")
for threshold in thresholds_to_test:
    y_pred_thresh = (y_pred_proba >= threshold).astype(int)
    precision_val = precision_score(y_test, y_pred_thresh)
    recall_val = recall_score(y_test, y_pred_thresh)
    f1_val = 2 * (precision_val * recall_val) / (precision_val + recall_val + 1e-10)

    # 计算混淆矩阵元素
    tp = ((y_pred_thresh == 1) & (y_test == 1)).sum()
    tn = ((y_pred_thresh == 0) & (y_test == 0)).sum()
    fp = ((y_pred_thresh == 1) & (y_test == 0)).sum()
    fn = ((y_pred_thresh == 0) & (y_test == 1)).sum()

    # 计算TPR(真正率/召回率)和FPR(假正率)
    tpr = tp / (tp + fn + 1e-10)  # 召回率
    fpr = fp / (fp + tn + 1e-10)  # 假正率

    print(
        f"{threshold:.1f}\t{precision_val:.4f}\t{recall_val:.4f}\t{f1_val:.4f}\t{fpr:.4f}\t{tpr:.4f}"
    )

print("\n" + "=" * 60)
print("模型性能汇总:")
print("=" * 60)
print(f"准确率: {accuracy:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")
print(f"平均精度(AP): {avg_precision:.4f}")

print("步骤6: 特征重要性分析...")
feature_importance = pd.DataFrame(
    {"feature": X_train_feat.columns, "importance": model.feature_importances_}
).sort_values("importance", ascending=False)

print("\n特征重要性排序 (前15):")
print(feature_importance.head(15))
ap_by_category = {}

categories = X_test_feat["category_presented"].unique()
for category in categories:
    mask = X_test_feat["category_presented"] == category
    y_true_cat = y_test[mask]
    y_pred_proba_cat = y_pred_proba[mask]
    ap_cat = average_precision_score(y_true_cat, y_pred_proba_cat)
    ap_by_category[category] = ap_cat
    print(f"类别 {category} 的平均精度(AP): {ap_cat:.4f}")
