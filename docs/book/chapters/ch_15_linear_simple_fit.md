# 15.3. Fitting the Simple Linear Model

**Nguồn web:** [https://learningds.org/ch/15/linear_simple_fit.html](https://learningds.org/ch/15/linear_simple_fit.html)  
**Nguồn tải:** `web-html` | `ch/15/linear_simple_fit`

---

# 15.3. Fitting the Simple Linear Model#
We stated earlier in this chapter that when we minimize the average loss over the data:
\[
\frac{1}{n} \sum_{i}[y_i - (\theta_0 + \theta_1 x_i)]^2
\]
the best-fitting line has intercept and slope:
\[\begin{split}
\begin{aligned}
\hat{\theta}_0 &= \bar{y} - \hat{\theta}_1 \bar{x} \\
\hat{\theta}_1 &= r({\mathbf{x}},{\mathbf{y}}) \frac{SD({\mathbf{y}})}{SD({\mathbf{x}})}
\end{aligned}
\end{split}\]
In this section, we use calculus to derive these results.
With the simple linear model, the mean squared error is a function of two model parameters, the intercept and slope. This means that if we use calculus to find the minimizing parameter values, we need to find the partial derivatives of the MSE with respect to \(\theta_0\) and \(\theta_1\). We can also find these minimizing values through other techniques:
Gradient descent
We can use numerical optimization techniques, such as gradient descent, when the loss function is more complex and it’s faster to find an approximate solution that’s pretty accurate (see Chapter 20).
Quadratic formula
Since the average loss is a quadratic function of \( \theta_0\) and \( \theta_1 \), we can use the quadratic formula (along with some algebra) to solve for the minimizing parameter values.
Geometric argument
Later in this chapter, we use a geometric interpretation of least squares to fit multiple linear models. This approach relates to the Pythagorean theorem and has several intuitive benefits.
We choose calculus to optimize the simple linear model since it is quick and straightforward. To begin, we take the partial derivatives of the sum of squared errors with respect to each parameter (we can ignore the e\(1/n\) in the MSE because it doesn’t affect the location of the minimum):
\[\begin{split}
\begin{aligned}
\frac{\partial}{\partial \theta_0} \sum_{i}[y_i - (\theta_0 + \theta_1 x_i)]^2
&=  \sum_{i} 2 (y_i - \theta_0 - \theta_1 x_i ) (-1)\\
& \\
\frac{\partial}{\partial \theta_1} \sum_{i}[y_i - (\theta_0 + \theta_1 x_i)]^2,
&= \sum_{i} 2 (y_i - \theta_0 - \theta_1 x_i) (-x_i)
\end{aligned}
\end{split}\]
Then we set the partial derivatives equal to 0 and simplify a bit by multiplying both sides of the equations by \(-1/2\) to get:
\[\begin{split}
\begin{aligned}
0   &= \sum_{i} (y_i - \hat{\theta}_0 - \hat{\theta}_1 x_i) \\
0   &= \sum_{i} (y_i - \hat{\theta}_0 - \hat{\theta}_1 x_i)x_i \\
\end{aligned}
\end{split}\]
These equations are called the normal equations.
In the first equation, we see that \(\hat{\theta}_0\) can be represented as a function of \(\hat{\theta}_1\):
\[
\hat{\theta}_0 = \bar{y} - \hat{\theta}_1 \bar{x}
\]
Plugging this value into the second equation gives us:
\[\begin{split}
\begin{aligned}
0   &= \sum_{i} (y_i - \bar y + \hat{\theta}_1 \bar x - \hat{\theta}_1 x_i ) x_i \\
&= \sum_{i} [(y_i - \bar y) - \hat{\theta}_1 ( x_i - \bar x)]x_i \\
\hat{\theta}_1  &= \frac{\sum_{i} (y_i - \bar y)x_i} {\sum_{i}( x_i - \bar x)x_i} \\
\end{aligned}
\end{split}\]
After some algebra, we can represent \(\hat{\theta}_1\) in terms of quantities that we are familiar with:
\[
\hat{\theta}_1 = r({\mathbf{x}},{\mathbf{y}}) \frac{SD({\mathbf{y}})}{SD({\mathbf{x}})}
\]
As shown earlier in this chapter, this representation says that a point on the fitted line at \(x\) can be written as follows:
\[
\hat{\theta}_0 + \hat{\theta}_1 x
= \bar{y} + r({\mathbf{x}},{\mathbf{y}}) SD({\mathbf{y}}) \frac{(x - \bar{x})}{SD({\mathbf{x}})}
\]
We have derived the equation  for the least squares line that we used in the previous section. There, we used the pandas built-in methods to compute
\(SD(\mathbf{x})\), \(SD(\mathbf{y})\), and \(r(\mathbf{x}, \mathbf{y})\),
to easily calculate the equation for this line.
However, in practice we recommend using the functionality provided in scikit-learn to do the model fitting:
from sklearn.linear_model import LinearRegression
y = GA['pm25pa']
x = GA[['pm25aqs']]
reg = LinearRegression().fit(x, y)
Our fitted model is:
print(f"Model: PA estimate = {reg.intercept_:.2f} + {reg.coef_[0]:.2f}AQS")
Model: PA estimate = -3.36 + 2.10AQS
Notice that we provided y as an array and x as a data frame to LinearRegression. We will soon see why when we fit multiple explanatory features in a model.
The LinearRegression method offers numerically stable algorithms to fit linear models by least squares. This is especially important when fitting multiple variables, which we introduce next.
