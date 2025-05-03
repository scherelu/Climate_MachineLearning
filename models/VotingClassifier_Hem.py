"""
This script implements the voting classifier ensemble method offered by the scikit-learn library to
analyze the annual data set, targeting the 'hemisphere' feature

    - Author: Ludwig Scherer
    - Date: 05/01/2025
"""

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read in the datasets
annual = pd.read_csv("./data/annual/annual_data_trim.csv")
monthly = pd.read_csv("./data/monthly/monthly_data_trim.csv")

# split into north and south
north_annual = annual[annual['hemisphere'] == 'north']
south_annual = annual[annual['hemisphere'] == 'south']

# get unique countries for each hemisphere
north_countries = north_annual['country'].unique()
south_countries = south_annual['country'].unique()

## due to disproportionate number of northern countries in data (142 N vs 66 S): downsample northern dataframe
# select country names randomly from northern countries until we have as many northern as southern countries
sampled_north_countries = np.random.choice(north_countries, size=len(south_countries), replace=False)

north_balanced = north_annual[north_annual['country'].isin(sampled_north_countries)]

# merge the two dataframes (now the number of northern and southern countries is equal)
balanced_df = pd.concat([north_balanced, south_annual]).sort_values(['year']).reset_index(drop=True)

features = [
    'year', 'temp_change_c', 'absol_temp_c', 'co2_mean', 'co2_growth', 'ch4_mean', 'ch4_growth'
    # ,'extent_global', 'area_global', 'extent_change_global', 'area_change_global'
]

target = 'hemisphere'

# sepcify features for testing and target feature
X = balanced_df[features]
y = balanced_df[target]

# encode labels to numeric
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# split data into 80/20, with stratiying to keep proportion 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# classifiers
clf_gb = GradientBoostingClassifier(random_state=1)
clf_rf = RandomForestClassifier(random_state=1)
clf_lr = Pipeline([('scaler', StandardScaler()), ('lr', LogisticRegression(max_iter=1000, random_state=1))])
clf_svc = Pipeline([('scaler', StandardScaler()), ('svc', SVC(probability=True, random_state=1))])
clf_knn = Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier())])

# fit and predict individual models
clf_gb.fit(X_train, y_train)
y_pred_gb = clf_gb.predict(X_test)
acc_gb = accuracy_score(y_test, y_pred_gb)

clf_rf.fit(X_train, y_train)
y_pred_rf = clf_rf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred_rf)

clf_lr.fit(X_train, y_train)
y_pred_lr = clf_lr.predict(X_test)
acc_lr = accuracy_score(y_test, y_pred_lr)

clf_svc.fit(X_train, y_train)
y_pred_svc = clf_svc.predict(X_test)
acc_svc = accuracy_score(y_test, y_pred_svc)

clf_knn.fit(X_train, y_train)
y_pred_knn = clf_knn.predict(X_test)
acc_knn = accuracy_score(y_test, y_pred_knn)


# voting classifier
vclf = VotingClassifier(
    estimators=[
        ('gb', clf_gb),
        ('rf', clf_rf),
        ('lr', clf_lr),
        ('svc', clf_svc),
        ('knn', clf_knn)
    ],
    voting='soft'
)

vclf.fit(X_train, y_train)
y_pred_vclf = vclf.predict(X_test)
acc_vclf = accuracy_score(y_test, y_pred_vclf)

# print accuracies
print(f"\nIndividual Model Accuracies:")
print(f"Gradient Boosting Accuracy: {acc_gb:.3f}")
print(f"Random Forest Accuracy:    {acc_rf:.3f}")
print(f"Logistic Regression Accuracy: {acc_lr:.3f}")
print(f"SVC Accuracy:              {acc_svc:.3f}")
print(f"KNN Accuracy:              {acc_knn:.3f}")
print(f"\nVoting Classifier Accuracy: {acc_vclf:.3f}")

# detailed report for ensemble
print("\nVoting Classifier Classification Report:")
print(classification_report(y_test, y_pred_vclf))
print("\nVoting Classifier Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_vclf))

# confusion matrix heatmap graph for VotingClassifier
conf_mat = confusion_matrix(y_test, y_pred_vclf)
plt.figure(figsize=(6, 5))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.title('Voting Classifier Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()