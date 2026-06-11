# 16. Model Selection

**Nguồn web:** [https://learningds.org/ch/16/ms_intro.html](https://learningds.org/ch/16/ms_intro.html)  
**Nguồn tải:** `web-html` | `ch/16/ms_intro`

---

# 16. Model Selection#
So far when we fit models, we have used a few strategies to decide which features to include:
-
Assess model fit with residual plots.
-
Connect the statistical model to a physical model.
-
Keep the model simple.
-
Compare improvements in the standard deviation of the residuals and in the MSE between increasingly complex models.
For example, when we examined the one-variable model of upward mobility in Chapter 15, we found curvature in the residual plot. Adding a second variable greatly improved the fit in terms of average loss (MSE and, relatedly, multiple \(R^2\)), but some curvature remained in the residuals. A seven-variable model made little improvement over the two-variable model in terms of a decrease in MSE, so although the two-variable model still showed some patterns in the residuals, we opted for this simpler model.
As another example, when we model the weight of a donkey in Chapter 18, we will take guidance from a physical model. We’ll ignore the donkey’s appendages and draw on the similarity between a barrel and a donkey’s body to begin fitting a model that explains weight by its length and girth (comparable to a barrel’s height and circumference). We’ll then continue to adjust that model
by adding categorical features related to the donkey’s physical condition and age, collapsing categories, and excluding other possible features to keep the model simple.
The decisions we make in building these models are based on judgment calls, and in
this chapter we augment these with more formal criteria.
To begin, we provide an example that shows why it’s typically not a good idea to include too many features in a model. This phenomenon, called overfitting, often leads to models that follow the data too closely and capture some of the noise in the data. Then, when new observations come along, the predictions are worse than those from a simpler model. The remainder of the chapter provides techniques, such as the train-test split, cross-validation, and regularization, for limiting the impact of overfitting. These techniques are especially helpful when there are a large number of potential features to include in a model. We also provide a synthetic example, where we know the true model, to explain the concepts of model variance and bias and how they relate to over- and underfitting.
