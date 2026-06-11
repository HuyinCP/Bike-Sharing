# 15.9. Summary

**Nguồn web:** [https://learningds.org/ch/15/linear_summary.html](https://learningds.org/ch/15/linear_summary.html)  
**Nguồn tải:** `web-html` | `ch/15/linear_summary`

---

# 15.9. Summary#
Linear models help us describe relationships between features.
We discussed the simple linear model and extended it to linear models in multiple
variables.
Along the way, we applied mathematical techniques that are widely useful
in modeling—calculus to minimize loss for
the simple linear model and matrix geometry for the multiple linear model.
Linear models may seem basic, but they are used for all sorts of tasks today.
And they are flexible enough to allow us to include categorical features as well as
nonlinear transformations of variables, such as log transformations, polynomials, and ratios.
Linear models have the advantage of being broadly interpretable for nontechnical people,
yet sophisticated enough to capture many common patterns in data.
It can be tempting to throw all of the variables available to us into a model to get the “best fit possible.” But we should keep in mind the geometry of least squares when fitting models. Recall that \(p\) explanatory variables can be thought of as \(p\) vectors in \(n\)-dimensional space, and if these vectors are highly correlated, then the projections onto this space will be similar to projections onto smaller spaces made up of fewer vectors. This implies that:
-
Adding more variables may not provide a large improvement in the model.
-
Interpretation of the coefficients can be difficult.
-
Several models can be equally effective in predicting/explaining the response variable.
If we are concerned with making inferences, where we want to interpret/understand the model, then we should err on the side of simpler models.
On the other hand, if our primary concern is the predictive ability of a model, then we tend not to concern ourselves with the number of coefficients and their interpretation. But this “black box” approach can lead to models that, say, overly depend on anomalous values in the data or models that are inadequate in other ways. So be careful with this approach, especially when the predictions may be harmful to people.
In this chapter, we used linear models in a descriptive way. We introduced a few notions for deciding when to include a feature in a model by examining residuals for patterns, comparing the size of standard errors and the change in the multiple \(R^2\). Oftentimes, we settled for a
simpler model that was easier to interpret. In the next chapter, we look at other, more formal tools for choosing the features to include in a model.
