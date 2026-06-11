# 19.5. From Probabilities to Classification

**Nguồn web:** [https://learningds.org/ch/19/class_dr.html](https://learningds.org/ch/19/class_dr.html)  
**Nguồn tải:** `web-html` | `ch/19/class_dr`

---

# 19.5. From Probabilities to Classification#
We started this chapter by presenting a binary classification problem where we want to model a nominal response variable. At this point, we have used logistic regression to model proportions or probabilities, and we’re now ready to return to the original problem: we use the predicted probabilities to classify records. For our example, this means that for a tree of a particular diameter, we use the fitted coefficients from the logistic regression to estimate the chance it is fallen. If the chance is high, we classify a tree as fallen; otherwise, we classify it as standing. But we need to choose a threshold for making this decision rule.
The sklearn logistic regression model’s predict function implements the basic decision rule: predict 1 if the predicted probability \( p > 0.5 \). Otherwise, predict 0. We’ve overlaid this decision rule on top of the model predictions as a dotted line:
X_plt = pd.DataFrame(
{"log_diam": np.linspace(X["log_diam"].min(), X["log_diam"].max(), 50)}
)
p_hats = lr_model.predict_proba(X_plt)
X_orig = np.exp(X_plt["log_diam"])
fig = px.scatter(
tree_bins, x="diameter", y="proportion", size="count", log_x=True,
labels={"diameter": "Tree diameter (cm)", "proportion": "Proportion down"},
width=550, height=250,
)
fig.add_trace(go.Scatter(
x=X_orig, y=p_hats[:, 1], line=dict(color="orange", width=3),
mode="lines", name="Model predictions",
))
fig.add_trace(go.Scatter(
x=X_orig, y=np.repeat(0.5, len(X_orig)),
line=dict(color="black", width=3, dash="dashdot"),
name="Decision rule",
))
fig
In this section, we consider a more general decision rule. For some choice of \(\tau\), predict 1 if the model’s predicted probability \( p > \tau \), otherwise predict 0. By default, sklearn sets \( \tau = 0.5 \). Let’s explore what happens when \( \tau \) is set to other values.
Choosing an appropriate value for \(\tau\) depends on our goals. Suppose we want to maximize accuracy. The accuracy of a classifier is the fraction of correct predictions. We can compute the accuracy for different thresholds, meaning different \( \tau \) values:
def threshold_predict(model, X, threshold):
return np.where(model.predict_proba(X)[:, 1] > threshold, 1.0, 0.0)
def accuracy(threshold, X, y):
return np.mean(threshold_predict(lr_model, X, threshold) == y)
thresholds = np.linspace(0, 1, 200)
accs = [accuracy(t, X, y) for t in thresholds]
To understand how accuracy changes with respect to \(\tau\), we make a plot:
fig = px.line(x=thresholds, y=accs, width=450, height=250)
fig.add_trace(
go.Scatter(
x=[0.5, 0.5],
y=[0.3, 0.8],
mode="lines",
name="𝛕 = 0.5",
showlegend=True,
)
)
fig.update_xaxes(title="Threshold")
fig.update_yaxes(title="Accuracy")
Notice that the threshold with the highest accuracy isn’t exactly at 0.5. In practice, we should use cross-validation to select the threshold (see Chapter 16).
The threshold that maximizes accuracy could be a value other than 0.5 for many reasons, but a common one is class imbalance, where one category is more frequent than another. Class imbalance can lead to a model that classifies a record as belonging to the more common category. In extreme cases (like fraud detection) when only a tiny fraction of the data contain a particular class, our models can achieve high accuracy by simply always predicting the frequent class without learning what makes a good classifier for the rare class. There are techniques for managing class imbalance, such as:
-
Resampling the data to reduce or eliminate the class imbalance
-
Adjusting the loss function to put a larger penalty on the smaller class
In our example, the class imbalance is not that extreme, so we continue without these adjustments.
The problem of class imbalance explains why accuracy alone is often not how we want to judge a model. Instead, we want to differentiate between the types of correct and incorrect classifications. We describe these next.
## 19.5.1. The Confusion Matrix#
A convenient way to visualize errors in a binary classification is to look at the confusion matrix.  The confusion matrix compares what the model predicts with the actual outcomes. There are two types of error in this situation:
False-positives
When the actual class is 0 (false) but the model predicts 1 (true)
False-negatives
When the actual class is 1 (true) but the model predicts 0 (false)
Ideally, we would like to minimize both kinds of errors, but we often need to manage the balance between these two sources.
Note
The terms positive and negative come from disease testing, where a test indicates the presence of a disease, is called a positive result. This can be a bit confusing because having a disease doesn’t seem like something positive at all. And \(y=1\) denotes the “positive” case. To keep things straight, it’s a good idea to confirm your understanding of what \(y=1\) stands for in the context of your data.
scikit-learn has a function to compute and plot the confusion matrix:
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y, lr_model.predict(X))
mat
array([[377,  49],
[104, 129]])
import plotly.figure_factory as ff
fig = ff.create_annotated_heatmap(
z=mat,
x=["False", "True"],
y=["False", "True"],
showscale=False,
colorscale=px.colors.sequential.gray_r,
)
fig.update_layout(font=dict(size=16), width=300, height=250)
# Add Labels
fig.add_annotation(
x=0,
y=0,
text="True negative",
yshift=30,
showarrow=False,
font=dict(color="white", size=14),
)
fig.add_annotation(
x=1,
y=0,
text="False positive",
yshift=30,
showarrow=False,
font=dict(color="black", size=14),
)
fig.add_annotation(
x=0,
y=1,
text="False negative",
yshift=30,
showarrow=False,
font=dict(color="black", size=14),
)
fig.add_annotation(
x=1,
y=1,
text="True positive",
yshift=30,
showarrow=False,
font=dict(color="black", size=14),
)
fig.update_xaxes(title="Predicted")
fig.update_yaxes(title="Actual", autorange="reversed")
Ideally, we want to see all of the counts in the diagonal squares True Negative and True Positive. That means we have correctly classified everything. But this is rarely the case, and we need to assess the size of the errors. For this, it’s easier to compare rates than counts. Next, we describe different rates and when we might prefer to prioritize one or the other.
## 19.5.2. Precision Versus Recall#
In some settings, there might be a much higher cost to missing positive cases.  For example, if we are building a classifier to identify tumors,
we want to make sure that we don’t miss any malignant tumors. Conversely, we’re less concerned about classifying a benign tumor as malignant because a pathologist would still need to take a closer look to verify the malignant classification. In this case, we want to have a high true positive rate among the records that are actually positive. The rate is called sensitivity, or recall:
\[
\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}} = \frac{\text{True Positives}}{\text{Actually True}}
\]
Higher recall runs the risk of predicting true on false records (false positives).
On the other hand, when classifying email as spam (positive) or ham (negative), we might be annoyed if an important email gets thrown into our spam folder. In this setting, we want high precision, the accuracy of the model for positive predictions:
\[
\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} = \frac{\text{True Positives}}{\text{Predicted True}}
\]
Higher-precision models are often more likely to predict that true observations are negative (higher false-negative rate).
A common analysis compares the precision and recall at different thresholds:
from sklearn import metrics
precision, recall, threshold = (
metrics.precision_recall_curve(y, lr_model.predict_proba(X)[:, 1]))
tpr_df = pd.DataFrame({"threshold":threshold,
"precision":precision[:-1], "recall": recall[:-1], })
To see how precision and recall relate, we plot them both against the threshold \( \tau \):
fig = go.Figure()
fig.add_trace(go.Scatter(x=tpr_df["threshold"], y=tpr_df["precision"], name="Precision"))
fig.add_trace(go.Scatter(x=tpr_df["threshold"], y=tpr_df["recall"], name="Recall",
line=dict(dash='dash')))
fig.update_layout(width=550, height=250,
xaxis_title="Threshold", yaxis_title="Proportion")
fig
Another common plot used to evaluate the performance of a classifier is the precision-recall curve, of PR curve for short. It plots the precision-recall pairs for each threshold:
fig = px.line(tpr_df, x="recall", y="precision",
labels={"recall":"Recall","precision":"Precision"})
fig.update_layout(width=450, height=250, yaxis_range=[0, 1])
fig
Notice that the righthand end of the curve reflects the imbalance in the sample. The precision matches the fraction of fallen trees in the sample, 0.35. Plotting multiple PR curves for different models can be particularly useful for comparing models.
Using precision and recall gives us more control over what kinds of errors matter.
As an example, let’s suppose we want to ensure that at least 75% of the fallen trees are classified as fallen. We can find the threshold where this occurs:
fall75_ind = np.argmin(recall >= 0.75) - 1
fall75_threshold = threshold[fall75_ind]
fall75_precision = precision[fall75_ind]
fall75_recall = recall[fall75_ind]
print(f'Threshold: {fall75_threshold:.2}')
print(f'Precision: {fall75_precision:.2}')
print(f'Recall:    {fall75_recall:.2}')
Threshold: 0.33
Precision: 0.59
Recall:    0.81
We find that about 41% (1 – precision) of the trees that we classify as fallen are actually standing. In addition, we find the fraction of trees below this threshold to be:
print("Proportion of samples below threshold:",
f"{np.mean(lr_model.predict_proba(X)[:,1] < fall75_threshold):0.2f}")
Proportion of samples below threshold: 0.52
So, we have classified 52% of the samples as standing (negative). Specificity (also called true negative rate) measures the proportion of data belonging to the negative class that the classifier labels as negative:
\[
\text{Specificity} = \frac{\text{True Negatives}}{\text{True Negatives} + \text{False Positives}} = \frac{\text{True Negatives}}{\text{Predicted False}}
\]
The specificity for our threshold is:
act_neg = (y == 0)
true_neg = (lr_model.predict_proba(X)[:,1] < fall75_threshold) & act_neg
print(f"Specificity: {np.sum(true_neg) / np.sum(act_neg):0.2f}")
Specificity: 0.70
In other words, 70% of the trees classified as standing are actually standing.
As we’ve seen, there are several ways to use the 2-by-2 confusion matrix. Ideally, we want accuracy, precision, and recall to all be high. This happens when most predictions fall along the diagonal for the table, so our predictions are nearly all correct–true negatives and true positives. Unfortunately, in most scenarios our models will have some amount of error. In our example, trees of the same diameter include a mix of fallen and standing, so we can’t perfectly classify trees based on their diameter. In practice, when data scientists choose a threshold, they need to consider their context to decide whether to prioritize precision, recall, or specificity.
