import numpy as np
import pandas as pd
from graphviz import Digraph
import matplotlib.pyplot as plt

# Node class for the Decision Tree
class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None, entropy=None, n_samples=None):
        self.feature_index = feature_index  # Index of feature to split on
        self.threshold = threshold          # Threshold value for the split. 
        self.left = left                    # Left subtree
        self.right = right                  # Right subtree
        self.value = value                  # Class label for leaf nodes. For ex. drugA, drugB, vs 
        self.entropy = entropy              # Entropy of the node.
        self.n_samples = n_samples          # Number of samples in the node.

class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.root = None

    def entropy(self, y):
        classes, counts = np.unique(y, return_counts=True)  # Find unique values in y and their counts
        probabilities = counts / len(y) # Get the probability of each unique value
        entropy = -np.sum(probabilities * np.log2(probabilities)) # Calculate the entropy
        return entropy
    
    def information_gain(self, X, y, feature_index, threshold):
        # Split data based on the given feature and threshold
        # left_mask is a boolean array that is True for samples that are lte to the threshold
        left_mask = X[:, feature_index] <= threshold
        right_mask = ~left_mask # Invert the left mask.

        # Calculate entropy for the left and right subsets
        left_entropy = self.entropy(y[left_mask])
        right_entropy = self.entropy(y[right_mask])

        # Calculate information gain
        total_entropy = self.entropy(y)
        p_left = np.sum(left_mask) / len(y)
        p_right = 1 - p_left
        information_gain = total_entropy - (p_left * left_entropy + p_right * right_entropy)

        return information_gain
    
    # Recursive splitting
    def split(self, X, y, depth):
        n_samples, n_features = X.shape # n_samples = num of rows in X, n_features = num of columns in X
        unique_classes = np.unique(y) # unique_classes is an array of the unique values in y

        # Check for stopping criteria
        if depth == self.max_depth or len(unique_classes) == 1:
            # Create a leaf node with the most common class
            return Node(value=unique_classes[0], entropy=self.entropy(y), n_samples=n_samples)

        # Find the best split with the highest information gain
        best_gain = 0
        best_feature = None
        best_threshold = None
        for feature_index in range(n_features):
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                gain = self.information_gain(X, y, feature_index, threshold)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_index
                    best_threshold = threshold

        # Split the data based on the best feature and threshold
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        left_subtree = self.split(X[left_mask], y[left_mask], depth + 1)
        right_subtree = self.split(X[right_mask], y[right_mask], depth + 1)

        # Create a decision node
        return Node(feature_index=best_feature, threshold=best_threshold, left=left_subtree, right=right_subtree, entropy=self.entropy(y), n_samples=n_samples)

    # This method creates the root node by calling the split method. Implements training
    def fit(self, X, y):
        self.root = self.split(X, y, depth=0)

    # Prediction
    def predict_one(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature_index] <= node.threshold:
            return self.predict_one(x, node.left)
        else:
            return self.predict_one(x, node.right)

    def predict(self, X):
        return [self.predict_one(x, self.root) for x in X]

    def visualize_tree(self, node, dot=None):
        if dot is None:
            dot = Digraph(comment='Decision Tree')

        if node.value is not None:
            dot.node(str(id(node)), f'Class {node.value}\nEntropy: {-node.entropy}\nSamples: {node.n_samples}')
        else:
            if node.feature_index is not None and node.feature_index == 2 or  node.feature_index == 3:
                node.threshold = levels[node.threshold]

            dot.node(str(id(node)), f'Feature: {features[node.feature_index]}\nThreshold: {node.threshold}\nEntropy: {node.entropy}\nSamples: {node.n_samples}')

            if node.left is not None:
                dot = self.visualize_tree(node.left, dot)
                dot.edge(str(id(node)), str(id(node.left)), label='<= '+str(node.threshold))

            if node.right is not None:
                dot = self.visualize_tree(node.right, dot)
                dot.edge(str(id(node)), str(id(node.right)), label='> '+str(node.threshold))

        return dot
    
# Read the data from the CSV file
df = pd.read_csv('drug200.csv')

# The features are the columns from "Age" to "Na_to_K"
features = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']

# Convert the data to numpy arrays
X = df.loc[:, 'Age':'Na_to_K'].to_numpy()

# Convert the categorical features to numerical values
levels = ['LOW', 'NORMAL', 'HIGH']
levelsEnum = enumerate(levels) # Enumerate the levels, 0 is LOW, 1 is NORMAL, 2 is HIGH

for col in range(2, 4): # Rows 2 and 3 are the categorical features
    for row in range(len(X)):
        if X[row, col] == levels[0]:
            X[row, col] = 0
        elif X[row, col] == levels[1]:
            X[row, col] = 1
        elif X[row, col] == levels[2]:
            X[row, col] = 2
    
# The "Drug" column is the target/label
y = df['Drug'].to_numpy()

n_samples = len(X)
n_train = int(0.8 * n_samples)
n_val = n_samples - n_train

validation_errors = []
decision_trees = []

# Split the data into training and validation sets. Apply 5-fold cross validation
for i in range(5):
    # Split the dataset into training and validation sets
    X_val = X[i*n_val:(i+1)*n_val]
    y_val = y[i*n_val:(i+1)*n_val]
    X_train = np.concatenate((X[:i*n_val], X[(i+1)*n_val:]))
    y_train = np.concatenate((y[:i*n_val], y[(i+1)*n_val:]))

    # Create and train the decision tree
    tree = DecisionTree(max_depth=5)
    tree.fit(X_train, y_train)
    decision_trees.append(tree)

    # Make predictions on the val set
    predictions = tree.predict(X_val)

    # Calculate the accuracy
    accuracy = np.sum(predictions == y_val) / len(y_val)

    # Calculate the validation error
    validation_error = 1 - accuracy
    validation_errors.append(validation_error)

# Calculate the average validation error
average_validation_error = np.mean(validation_errors)
print('Average validation error:', round(average_validation_error, 4))

# Visualize the decision tree with the lowest validation error
lowest_error_index = np.argmin(validation_errors)
tree = decision_trees[lowest_error_index]
dot = tree.visualize_tree(tree.root)

# Save the tree visualization as an image
dot.render('decision_tree', format='png', cleanup=True)

# Plot the training and validation errors
plt.bar([0,1,2,3,4], validation_errors, label='Validation Error')
plt.xlabel('Validation Set Index')
plt.ylabel('Error Rate')
plt.title('Validation Errors vs. Set Index')
plt.legend()
plt.show()