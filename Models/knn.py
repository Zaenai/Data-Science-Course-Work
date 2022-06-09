# Import necessary modules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import os
import pandas as pd
# Loading data
print("running knn...")

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', "features", "AllFeaturesDroped.csv"))
featureData = pd.read_csv(path)

# Create feature and target arrays
X = featureData.iloc[:, :5]#Get the feature columns
y = featureData["type"]
 
# Split into training and test set
X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size = 0.2, random_state=42)

print("y_train type counts:", y_train.value_counts())
print("y_test type counts:", y_test.value_counts())

knn = KNeighborsClassifier(n_neighbors=4)
scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
print(scores)
print(scores.mean())
# search for an optimal value of K for KNN

# list of integers 1 to 30
# integers we want to try
# k_range = range(1, 31)

# # list of scores from k_range
# k_scores = []

# # 1. we will loop through reasonable values of k
# for k in k_range:
#     print(f"Testing for k={k}")
#     # 2. run KNeighborsClassifier with k neighbours
#     knn = KNeighborsClassifier(n_neighbors=k)
#     # 3. obtain cross_val_score for KNeighborsClassifier with k neighbours
#     knn.fit(X_train, y_train)
#     k_scores.append(knn.score(X_test, y_test))
#     #scores = cross_val_score(knn, X, y, cv=5, scoring='accuracy')
#     # 4. append mean of scores for k neighbors to k_scores list
#     #k_scores.append(scores.mean())
# print(k_scores)
# # plot the value of K for KNN (x-axis) versus the cross-validated accuracy (y-axis)
# plt.plot(k_range, k_scores)
# plt.xlabel('Value of K for KNN')
# plt.ylabel('Cross-Validated Accuracy')