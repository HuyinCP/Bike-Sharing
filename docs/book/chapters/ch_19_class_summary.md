# 19.6. Summary

**Nguồn web:** [https://learningds.org/ch/19/class_summary.html](https://learningds.org/ch/19/class_summary.html)  
**Nguồn tải:** `web-html` | `ch/19/class_summary`

---

# 19.6. Summary#
In this chapter, we fit simple logistic regressions with one explanatory variable, but we can easily include other variables in the model by adding more features to our design matrix. For example, if some predictors are categorical, we can include them as one-hot encoded features. These ideas carry over directly from Chapter 15. The technique of regularization (Chapter 16) also applies to logistic regression. We will integrate all of these modeling techniques—including using a train-test split to assess the model and cross-validation to choose the threshold—in the case study in Chapter 21 that develops a model to classify fake news.
Logistic regression is a cornerstone in machine learning since it naturally
extends to more complex models. For example, logistic regression is one of the
basic components of a neural network. When the response variable has more than
two categories, logistic regression can be extended to multinomial logistic
regression. Another extension of logistic regression for modeling counts is
called Poisson regression. These different forms of regression are related to
maximum likelihood, where the underlying model for the response is binomial,
multinomial, or Poisson, respectively, and the goal is to optimize the
likelihood of the data over the parameters of the respective distribution. This
family of models is also known as generalized linear models. In all of these
scenarios, closed form solutions for minimizing loss don’t exist, so
optimization of the average loss relies on numerical methods, which we cover in
the next chapter.
