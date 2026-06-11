# 20.2. Minimizing Huber Loss

**Nguồn web:** [https://learningds.org/ch/20/gd_example.html](https://learningds.org/ch/20/gd_example.html)  
**Nguồn tải:** `web-html` | `ch/20/gd_example`

---

# 20.2. Minimizing Huber Loss#
Huber loss combines absolute loss and squared loss to get a function that is differentiable (like squared loss) and less sensitive to outliers (like absolute loss):
\[\begin{split}
L(\theta, \textbf{y}) = \frac{1}{n} \sum_{i=1}^n \begin{cases}
\frac{1}{2}(y_i - \theta)^2 &  | y_i - \theta | \le \gamma \\
\gamma (|y_i - \theta| - \frac{1}{2} \gamma ) & \text{otherwise}
\end{cases}
\end{split}\]
Since Huber loss is differentiable, we can use gradient descent. We first find the gradient of the average Huber loss:
\[\begin{split}
\nabla_{\theta} L(\theta, \textbf{y}) = \frac{1}{n} \sum_{i=1}^n \begin{cases}
-(y_i - \theta) &  | y_i - \theta | \le \gamma \\
- \gamma \cdot \text{sign} (y_i - \theta) & \text{otherwise}
\end{cases}
\end{split}\]
We create the functions huber_loss and grad_huber_loss to compute the average loss and its gradient. We write these functions to have signatures that enable us to specify the parameter as well as the observed data that we average over and the transition point of the loss function:
def huber_loss(theta, dataset, gamma=1):
d = np.abs(theta - dataset)
return np.mean(
np.where(d <= gamma,
(theta - dataset)**2 / 2.0,
gamma * (d - gamma / 2.0))
)
def grad_huber_loss(theta, dataset, gamma=1):
d = np.abs(theta - dataset)
return np.mean(
np.where(d <= gamma,
-(dataset - theta),
-gamma * np.sign(dataset - theta))
)
Next, we write a simple implementation of gradient descent. The signature of our function includes the loss function, its gradient, and the data to average over. We also supply the learning rate.
def minimize(loss_fn, grad_loss_fn, dataset, alpha=0.2, progress=False):
'''
Uses gradient descent to minimize loss_fn. Returns the minimizing value of
theta_hat once theta_hat changes less than 0.001 between iterations.
'''
theta = 0
while True:
if progress:
print(f'theta: {theta:.2f} | loss: {loss_fn(theta, dataset):.3f}')
gradient = grad_loss_fn(theta, dataset)
new_theta = theta - alpha * gradient
if abs(new_theta - theta) < 0.001:
return new_theta
theta = new_theta
Recall that the bus delays dataset consists of over 1,000 measurements of how many minutes late the northbound C-line buses are in arriving at the stop at 3rd Avenue and Pike Street in Seattle:
delays = pd.read_csv('data/seattle_bus_times_NC.csv')
In Chapter 4, we fit a constant model to these data for absolute loss and squared loss. We found that absolute loss yielded the median and square the mean of the data:
print(f"Mean:   {np.mean(delays['minutes_late']):.3f}")
print(f"Median: {np.median(delays['minutes_late']):.3f}")
Mean:   1.920
Median: 0.742
Now we use the gradient descent algorithm to find the minimizing constant model for Huber loss:
%%time
theta_hat = minimize(huber_loss, grad_huber_loss, delays['minutes_late'])
print(f'Minimizing theta: {theta_hat:.3f}')
print()
Minimizing theta: 0.701
CPU times: user 93 ms, sys: 4.24 ms, total: 97.3 ms
Wall time: 140 ms
The optimizing constant for Huber loss is close to the value that minimizes absolute loss. This comes from the shape of the Huber loss function. It is linear in the tails and so is not affected by outliers like with absolute loss and unlike with squared loss.
Warning
We wrote our minimize function to demonstrate the idea behind the algorithm. In practice, you will want to use well-tested, numerically sound implementations of an optimization algorithm. For example, the scipy package has a minimize method that we can use to find the minimizer of average loss, and we don’t even need to compute the gradient. This algorithm is likely to be much faster than any one that we might write. In fact, we used it in Chapter 18 when we created our own asymmetric modification of quadratic loss for the special case where we wanted the loss to be greater for errors on one side of the minimum than the other.
More generally, we typically stop the algorithm when \( \theta^{(t)} \) doesn’t
change much between iterations. In our function, we stop when \( \theta^{(t+1)} - \theta^{(t)} \) is less than 0.001. It is also common to stop the search after
a large number of steps, such as 1,000. If the algorithm has not arrived at the
minimizing value after 1,000 iterations, then the algorithm might be diverging
because the learning rate is too large or the minimum might exist in the limit
at \( \pm \infty \).
Gradient descent gives us a general way to minimize average loss when we cannot
easily solve for the minimizing value analytically or when the minimization is
computationally expensive. The algorithm relies on two important properties of
the average loss function: that it is both convex and differentiable in \( \boldsymbol{\theta} \). We discuss how the algorithm relies on these properties
next.
