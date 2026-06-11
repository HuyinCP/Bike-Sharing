# 16.1. Overfitting

**Nguồn web:** [https://learningds.org/ch/16/ms_overfitting.html](https://learningds.org/ch/16/ms_overfitting.html)  
**Nguồn tải:** `web-html` | `ch/16/ms_overfitting`

---

# 16.1. Overfitting#
When we have many features available to include in a model, choosing which ones to include or exclude rapidly gets complicated. In the upward mobility example in Chapter 15, we chose two of the seven variables to fit the model, but there are 21 pairs of features that we could have examined and fitted for a two-variable model.
And there are over one hundred models to choose from if we consider all one-, two-, …, seven-variable models.
It can be hard to examine hundreds of residual plots, to decide how simple is simple, and to settle on a model.
Unfortunately, the notion of minimizing MSE isn’t entirely helpful either. With each variable that we add to a model, the MSE typically gets smaller. Recall from the geometric perspective of model fitting (Chapter 15) that adding a feature to a model adds an \(n\)-dimensional vector to the feature space, and the error between the outcome vector and its projection into the space spanned by the explanatory variables shrinks. We might view this as a good thing because our model fits the data more closely, but there is a danger in overfitting.
Overfitting happens when the model follows the data too closely and picks up the variability in the random noise in the outcome. When this happens, new observations are not well-predicted. An example helps clarify this idea.
## 16.1.1. Example: Energy Consumption#
In this example, we examine a dataset that contains information from utility bills for a private residence in Minnesota. We have records of the monthly gas usage in a home (cubic feet) and the average temperature that month (degrees Farenheit).1 We first read in the data:
heat_df = pd.read_csv("data/utilities.csv", usecols=["temp", "ccf"])
heat_df
temp
ccf
0
29
166
1
31
179
2
15
224
...
...
...
96
76
11
97
55
32
98
39
91
99 rows × 2 columns
Let’s begin by looking at a scatter plot of gas consumption as a function of temperature:
fig = make_subplots(rows=1, cols=2)
fig.add_trace(
go.Scatter(x=heat_df['temp'], y=heat_df['ccf'], mode="markers"),
row=1, col=1)
fig.update_xaxes(title='Temperature (<sup>o</sup>F)', row=1, col=1)
fig.update_yaxes(title='Gas consumption (ft^3)', row=1, col=1)
fig.add_trace(
go.Scatter(x=heat_df['temp'], y=heat_df['ccf'], mode="markers"),
row=1, col=2)
fig.update_xaxes(type="log", title='Temperature (<sup>o</sup>F)', row=1, col=2)
fig.update_layout(height=250, width=500, showlegend=False)
fig.show()
The relationship shows curvature (left plot), but when we try to straighten it with a log transformation (right plot) a different curvature arises in the low-temperature region. Additionally, there are two unusual points. When we refer back to the documentation, we find that these points represent recording errors, so we remove them.
Let’s see if a quadratic curve can capture the relationship between gas usage and temperature.
Polynomials are still considered linear models. They are linear in their polynomial features. For example, we can express a quadratic model as:
\[
\theta_0 + \theta_1 x + \theta_2 x^2
\]
This model is linear in the features \(x\) and \(x^2\), and in matrix notation we can write this model as \({\textbf{X}} {\boldsymbol{\theta}}\), where
\( \textbf{X} \) is the design matrix:
\[\begin{split}
\left\lceil
\begin{matrix}
1 & x_1 & x_1^2\\
1 & x_2 & x_2^2\\
\vdots & \vdots & \vdots\\
1 & x_n & x_n^2\\
\end{matrix}
\right\rceil
\end{split}\]
We can create the polynomial features of the design matrix with the PolynomialFeatures tool in scikit-learn:
y = heat_df['ccf']
X = heat_df[['temp']]
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(X)
poly_features
array([[  29.,  841.],
[  31.,  961.],
[  15.,  225.],
...,
[  76., 5776.],
[  55., 3025.],
[  39., 1521.]])
We set the parameter include_bias to False because we plan to fit the polynomial with the LinearRegression method in scikit-learn, and by default it includes the constant term in the model. We fit the polynomial with:
from sklearn.linear_model import LinearRegression
model_deg2 = LinearRegression().fit(poly_features, y)
To get a quick idea as to the quality of the fit, let’s overlay the fitted quadratic on the scatter plot and also look at the residuals:
The quadratic captures the curve in the data quite well, but the residuals show a slight upward trend in the temperature range of 70°F to 80°F, which indicates some lack of fit. There is also some funneling in the residuals, where the variability in gas consumption is greater in the colder months. We might expect this behavior since we have only the monthly average temperature.
For comparison, we fit a few more models with higher-degree polynomials and collectively examine the fitted curves:
poly12 = PolynomialFeatures(degree=12, include_bias=False)
poly_features12 = poly12.fit_transform(X)
degrees = [1, 2, 3, 6, 8, 12]
mods = [LinearRegression().fit(poly_features12[:, :deg], y)
for deg in degrees]
Warning
We use the polynomial features in this section to demonstrate over-fitting, but
directly fitting the \(x, x^2, x^3, \ldots\) polynomials is not advisable in
practice. Unfortunately, these polynomial features tend to be highly
correlated. For example, the correlation between \(x\) and \(x^2\) for the energy
data is 0.98. Highly correlated features give unstable coefficients, where a
small change in an x-value can lead to a large change in the coefficients of
the polynomial. Also, when the x-values are large, the normal equations
are poorly conditioned and the coefficients can be difficult to interpret and
compare.
A better practice is to use polynomials that have been constructed to be
orthogonal to one another. These polynomials fill the same space as the
original polynomials, but they are uncorrelated with one another and give a
more stable fit.
Let’s place all of the polynomial fits on the same graph so that we can see how the higher-degree polynomials bend more and more strangely:
We can also visualize the different polynomial fits in separate facets:
The degree 1 curve (the straight line) in the upper-left facet misses the curved pattern in the data. The degree 2 curve begins to capture it, and the degree 3 curve looks like an improvement, but notice the upward bend at the right side of the plot. The polynomials of degrees 6, 8, and 12 follow the data increasingly closely, as they get increasingly curvy. These polynomials seem to fit spurious bumps in the data. Altogether, these six curves illustrate under- and overfitting. The fitted line in the upper left underfits and misses the curvature entirely. And the degree 12 polynomial in the bottom right definitely overfits with a wiggly pattern that we don’t think makes sense in this context.
In general, as we add more features, models get more complex and the MSE drops, but at the same time,
the fitted model grows increasingly erratic and sensitive to the data.
When we overfit, the model follows the data too closely, and predictions are poor for new observations. One simple technique to assess a fitted model is to compute the MSE on new data, data that were not used in building the model. Since we don’t typically have the capacity to acquire more data, we set aside some of the original data to evaluate the fitted model. This technique is the topic of the next section.
1
These data are from Daniel T. Kaplan, Statistical Modeling: A Fresh Approach (CreateSpace Independent Publishing Platform, 2009).
