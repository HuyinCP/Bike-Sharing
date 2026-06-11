# 15.5. Fitting the Multiple Linear Model

**Nguồn web:** [https://learningds.org/ch/15/linear_multi_fit.html](https://learningds.org/ch/15/linear_multi_fit.html)  
**Nguồn tải:** `web-html` | `ch/15/linear_multi_fit`

---

# 15.5. Fitting the Multiple Linear Model#
In the previous section, we considered the case of two explanatory variables; one of these we called \(x\) and the other \(v\). Now we want to generalize the approach to \(p\) explanatory variables. The idea of choosing different letters to represent variables quickly fails us. Instead, we use a more formal and general approach that represents multiple predictors as a matrix, as depicted in Figure 15.3. We call \(\textbf{X}\) the design matrix. Notice that \(\textbf{X}\) has shape \( n \times (p + 1)\).  Each column of \(\textbf{X}\) represents a feature, and each row represents an observation. That is, \(x_{i,j}\) is the measurement taken on observation \(i\) for feature \(j\).
Fig. 15.3 In this design matrix \(X\), each row represents an observation/record and each column a feature/variable#
Note
One technicality: the design matrix is defined as a mathematical matrix,
not a data frame, so you might notice that a matrix doesn’t include the column or row labels that a data frame has.
That said, we usually don’t have to worry about converting dataframes into matrices
since most Python libraries for modeling treat dataframes of numbers as if they were matrices.
For a given observation, say, the second row in \(\textbf{X}\), we approximate the outcome \(y_2\) by the linear combination:
\[
\begin{aligned}
y_2 \approx  \theta_0 + \theta_1 x_{2,1} + \ldots + \theta_p x_{2,p}
\end{aligned}
\]
It’s more convenient to express the linear approximation in matrix notation.
To do this, we write the model parameters as a \(p+1\) column vector \({\boldsymbol{\theta}}\):
\[\begin{split}
{\theta} =
\begin{bmatrix}
\theta_0 \\
\theta_1 \\
\vdots \\
\theta_p
\end{bmatrix}
\end{split}\]
Putting these notational definitions together, we can write the vector of predictions for the entire dataset using matrix multiplication:
\[
{\textbf{X}} {\boldsymbol{\theta}}
\]
If we check the dimensions of \(\textbf{X}\) and \(\boldsymbol{\theta}\), we can confirm that \({\textbf{X}} {\boldsymbol{\theta}}\) is an \(n\)-dimensional column vector.
So the error in using this linear prediction can be expressed as the vector:
\[ \mathbf{e} = \mathbf{y}  - {\textbf{X}} {\boldsymbol{\theta}}\]
where the outcome variable is also represented as a column vector:
\[\begin{split}
\mathbf{y} =
\begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_n
\end{bmatrix}
\end{split}\]
This matrix representation of the multiple linear model can help us find the model that minimizes mean square error. Our goal is to find the model parameters \((\theta_0, \theta_1, \ldots, \theta_p)\) that minimize the mean square error:
\[
\frac{1}{n} \sum_i [y_i - (\theta_0 + \theta_1 x_{i,1} + \cdots + \theta_p x_{i,p})]^2
= \frac{1}{n}  \lVert \mathbf{y} - {\textbf{X}} {\boldsymbol{\theta}} \rVert^2
\]
Here, we use the notation \( \lVert\mathbf{v}\rVert^2 \) for a vector \(\mathbf{v}\) as a
shorthand for the sum of each vector element squared:
\(\lVert\mathbf{v}\rVert^2 = \sum_i v_i^2\).
The square-root, \(\sqrt{\lVert\mathbf{v}\rVert^2}\), corresponds to the length of the vector \(\mathbf{v}\) and is also called the \(\ell_2\) norm of \(\mathbf{v}\). So, minimizing the mean square error is the same thing as finding the shortest error vector.
We can fit our model using calculus as we did for the simple linear model.
However, this approach gets cumbersome, and instead we use a geometric argument that is more intuitive and easily leads to useful properties of the design matrix, errors, and predicted values.
Our goal is to find the parameter vector, which we call \(\boldsymbol{\hat{\theta}}\), that minimizes our average squared loss—we want to make \(\lVert \mathbf{y} - {\textbf{X}} {\boldsymbol{\theta}} \rVert^2\) as small as possible for a given \(\textbf{X}\) and \(\mathbf{y}\).
The key insight is that we can restate this goal in a geometric way.
Since the model predictions and the true outcomes are both vectors, we can think of them as vectors in a vector space.
When we change our model parameters \( {\boldsymbol{\theta}} \), the model makes
different predictions, but any prediction must be a linear combination of the column vectors of \( \mathbf{X} \); that is, the prediction must be in what is called \( \text{span}(\mathbf{X}) \).
This notion is illustrated in Figure 15.4, where the shaded region consists of the possible linear models. Notice that \(\mathbf{y}\) is not entirely captured in \( \text{span}(\mathbf{X}) \); this is typically the case.
Fig. 15.4 In this simplified diagram, the space of all possible model prediction vectors \( \text{span}(\mathbf{X}) \) is illustrated as a gray plane in three-dimensional space, and the observed \( \mathbf{y} \) as a vector#
Although the squared loss can’t be exactly zero because \(  \mathbf{y} \) isn’t in the \( \text{span}(\mathbf{X}) \), we can find the vector that lies as close to \( \mathbf{y} \) as possible while still being in \( \text{span}(\mathbf{X}) \). This vector is called \( \mathbf{\hat{y}} \).
The error is the vector \( \mathbf{e} = \mathbf{y} - \mathbf{\hat{y}} \). Its length \( \lVert\mathbf{e}\rVert \) represents the distance between the true outcome and our model’s prediction.
Visually, \( \mathbf{e} \) has the smallest magnitude when it is perpendicular to the \( \text{span}(\mathbf{X}) \), as shown in
Figure 15.5.
The proof of this fact is omitted, and we rely on the figures to convince you of this fact.
Fig. 15.5 The mean squared error is minimized when the prediction \( \mathbf{\hat{y}} \) lies in \( \text{span}(\mathbf{X}) \) perpendicular to \( \mathbf{{y}} \)#
The fact that the smallest error, \( \mathbf{e} \), must be perpendicular to \(\mathbf{\hat{y}}\) lets us derive a formula for \( \hat{\boldsymbol{\theta}} \) as follows:
\[\begin{split}
\begin{aligned}
\textbf{X} \boldsymbol{\hat{\theta}} + \mathbf{e} &= \mathbf{y}  & (\text{the definition of} \mathbf{y}, \hat{\mathbf{y}}, \mathbf{e} ) \\
{\textbf{X}}^\top \textbf{X} \hat{\boldsymbol{\theta}} + {\textbf{X}}^\top \mathbf{e} &= {\textbf{X}}^\top \mathbf{y}
& (\text{left-multiply by } {\textbf{X}}^\top) \\
{\textbf{X}}^\top \textbf{X} \hat{\boldsymbol{\theta}} &= {\textbf{X}}^\top \mathbf{y}
& (\mathbf{e} \perp \text{span}(\textbf{X})) \\
\boldsymbol{\hat{\theta}} &= ({\textbf{X}}^\top \textbf{X})^{-1} {\textbf{X}}^\top \mathbf{y}
& (\text{left-multiply by } ({\textbf{X}}^\top \textbf{X})^{-1})
\end{aligned}
\end{split}\]
This general approach to derive \(\boldsymbol{\hat{\theta}}\) for the multiple linear model also gives
us \(\hat{\theta}_0\) and \(\hat{\theta}_1\) for the simple linear model. If we set
\({\textbf{X}}\) to be the two-column matrix that contains the intercept column and one feature column, this
formula for \(\boldsymbol{\hat{\theta}}\) and some linear algebra gets the intercept and slope of the least-squares-fitted simple linear model. In fact, if \({\textbf{X}}\) is simply a single column of \(1\)s, then we can use this formula to show that \({\hat{\theta}}\) is just the mean of \(\mathbf{y}\). This nicely ties back to the constant model that we introduced in Chapter 4.
Note
While we can write a simple function to derive the \(\boldsymbol{\hat{\theta}}\) based on the formula
\[
\boldsymbol{\hat{\theta}} = ({\textbf{X}}^\top \textbf{X})^{-1} {\textbf{X}}^\top \mathbf{y}
\]
we recommend leaving the calculation of \(\boldsymbol{\hat{\theta}}\) to the optimally tuned methods provided in the scikit-learn and statsmodels libraries. They handle cases where the design matrix is sparse, highly co-linear, and not invertible.
This solution for \(\boldsymbol{\hat{\theta}}\) (along with the pictures) reveals some useful properties of the fitted coefficients and the predictions:
-
The residuals, \(\mathbf{e}\), are orthogonal to the predicted values, \(\hat{\mathbf{y}}\).
-
The average of the residuals is 0, if the model has an intercept term.
-
The variance of the residuals is just the MSE.
These properties explain why we examine plots of the residuals against the predictions. When we fit a multiple linear model, we also plot the residuals against variables that we are considering adding to the model. If they showed a linear pattern, then we would consider adding them to the model.
In addition to examining the SD of the errors, the ratio of the MSE for a multiple linear model to the MSE for the constant model gives a measure of the model fit. This is called the multiple \(R^2\) and is defined as:
\[
R^2 =  1 - \frac {\lVert \mathbf{y} - {\textbf{X}}{\boldsymbol{\hat{\theta}}} \rVert^2}
{\lVert {\mathbf{y}} - \bar{y} \rVert^2}
\]
As the model fits the data closer and closer, the multiple \(R^2\) gets nearer to 1. That might seem like a good thing, but there can be problems with this approach because \(R^2\) continues to grow even as we add meaningless features to our model, as long as the features expand the \(\text{span}(\textbf{X})\). To account for the size of a model, we often adjust the numerator and denominator in \(R^2\) by the number of fitted coefficients in the models. That is, we normalize the numerator by \(1/[n-(p+1)]\) and the denominator by \(1/(n-1)\). Better approaches to selecting a model are covered in Chapter 16.
Next, we consider a social science example where there are many variables available to us for modeling.
