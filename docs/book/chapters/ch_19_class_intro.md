# 19. Classification

**Nguồn web:** [https://learningds.org/ch/19/class_intro.html](https://learningds.org/ch/19/class_intro.html)  
**Nguồn tải:** `web-html` | `ch/19/class_intro`

---

# 19. Classification#
This chapter continues our foray into the fourth stage of the data science lifecycle: fitting and evaluating models to understand the world. So far, we’ve described how to fit a constant model using absolute error (Chapter 4) and simple and multiple linear models using squared error (Chapter 15). We’ve also fit linear models with an asymmetric loss function (Chapter 18) and with regularized loss (Chapter 16). In all of these cases, we aimed to predict or explain the behavior of a numeric outcome—bus wait times, smoke particles in the air, and donkey weights are all numeric variables.
In this chapter we expand our view of modeling. Instead of predicting numeric outcomes, we build models to predict nominal outcomes. These sorts of models enable banks to predict whether a credit card transaction is fraudulent or not, doctors to classify tumors as benign or malignant, and your email service to identify spam and set it aside from your usual emails. This type of modeling is called classification and occurs widely in data science.
Just as with linear regression, we formulate a model, choose a loss function, fit the model by minimizing average loss for our data, and assess the fitted model. But unlike linear regression, our model is not linear; the loss function is not squared error; and our assessment compares different kinds of classification errors. Despite these differences, the overall structure of model fitting carries over to this setting. Together, regression and classification compose the primary approaches for supervised learning, the general task of fitting models based on observed outcomes and covariates.
We begin by introducing an example that we use throughout this chapter.
