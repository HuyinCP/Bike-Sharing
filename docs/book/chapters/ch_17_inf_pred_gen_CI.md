# 17.4. Basics of Confidence Intervals

**Nguồn web:** [https://learningds.org/ch/17/inf_pred_gen_CI.html](https://learningds.org/ch/17/inf_pred_gen_CI.html)  
**Nguồn tải:** `web-html` | `ch/17/inf_pred_gen_CI`

---

# 17.4. Basics of Confidence Intervals#
We have seen that modeling leads to estimates, such as the typical time that a bus is late (Chapter 4), a humidity adjustment to an air quality measurement (Chapter 15), and an estimate of vaccine efficacy (Chapter 2).  These examples are point estimates for unknown values, called parameters: the median lateness of the bus is 0.74 minutes; the humidity adjustment to air quality is 0.21 PM2.5 per humidity percentage point; and the ratio of COVID infection rates in  vaccine efficacy is 0.67. However, a different sample would have produced a different estimate. Simply providing a point estimate doesn’t give a sense of the estimate’s precision. Alternatively, an interval estimate can reflect the estimate’s accuracy. These intervals typically take one of two forms:
-
A bootstrap confidence interval created from the percentiles of the bootstrap sampling distribution
-
A normal confidence interval constructed using the standard error (SE) of the sampling distribution and additional assumptions about the distribution having the shape of a normal curve
We describe these two types of intervals and then give an example.
Recall that the sampling distribution (see Figure 17.1) is a probability distribution that reflects the chance of observing different values of \(\hat{\theta}\). Confidence intervals are constructed from the spread of the sampling distribution of \(\hat{\theta}\), so the endpoints of the interval are random because they are based on \(\hat{\theta}\). These intervals are designed so that 95% of the time the interval covers \(\theta^*\).
As its name suggests, the percentile-based bootstrap confidence interval is created from the percentiles of the bootstrap sampling distribution. Specifically, we compute the quantiles of the sampling distribution of \(\hat{\theta}_B\), where \(\hat{\theta}_B\) is the bootstrapped statistic.
For a 95th percentile interval, we identify the 2.5 and 97.5 quantiles, called \(q_{2.5,B}\) and \(q_{97.5,B}\), respectively, where 95% of the time the bootstrapped statistic is in the interval:
\[
q_{2.5,B} \leq \hat{\theta}_B~ \leq ~ q_{97.5,B}
\]
This bootstrap percentile confidence interval is considered a quick-and-dirty interval. There are many alternatives that adjust for bias, take into consideration the shape of the distribution, and are better suited for small samples.
The percentile confidence interval does not rely on the sampling distribution having a particular shape or the center of the distribution being \(\theta^*\). In contrast, the normal confidence interval often doesn’t require bootstrapping to compute, but it does make additional assumptions about the shape of the sampling distribution of \(\hat{\theta}\).
We use the normal confidence interval when the sampling distribution is well approximated by a normal curve. For a normal probability distribution, with center \(\mu\) and spread \(\sigma\), there is a 95% chance that a random value from this distribution is in the interval \(\mu ~\pm ~ 1.96 \sigma\). Since the center of the sampling distribution is typically \(\theta^*\), the chance is 95% that for a randomly generated \(\hat{\theta}\):
\[|\hat{\theta} -\theta^*| \leq 1.96 SE(\hat{\theta})\]
where \(SE(\hat{\theta})\) is the spread of the sampling distribution of \(\hat{\theta}\). We use this inequality to make a 95% confidence interval for \(\theta^*\):
\[ [ \hat{\theta} ~-~ 1.96 SE(\hat{\theta}),~~~  \hat{\theta} ~ +~ 1.96 SE(\hat{\theta})]\]
Confidence intervals of other sizes can be formed with different multiples of \(SE(\hat{\theta})\), all based on the normal curve. For example, a 99% confidence interval is \(\pm 2.58 SE\), and a one-sided upper 95% confidence interval is \([ \hat{\theta} ~-~ 1.64 SE(\hat{\theta}),~~ \infty]\).
Note
The SD of a parameter estimate is often called the standard error, or SE, to distinguish it from the SD of a sample, population, or one draw from an urn. In this book, we don’t differentiate between them. We call them SDs.
We provide an example of each type of interval next.
Earlier in this chapter we tested the hypothesis that the coefficient for humidity in a linear model for air quality is 0. The fitted coefficient for these data was \(0.21\). Since the null model did not completely specify the data generation mechanism, we resorted to bootstrapping. That is, we used the data as the population, took a sample of 11,226 records with replacement from the bootstrap population, and fitted the model to find the bootstrap sample coefficient for humidity. Our simulation repeated this process 10,000 times to get an approximate bootstrap sampling distribution.
We can use the percentiles of this bootstrap sampling distribution to create a 99% confidence interval for \(\theta^*\). To do this, we find the quantiles, \(q_{0.5}\) and \(q_{99.5}\), of the bootstrap sampling distribution:
q_995 = np.percentile(boot_theta_hat, 99.5, method='lower')
q_005 = np.percentile(boot_theta_hat, 0.05, method='lower')
print(f"Lower 0.05th percentile: {q_005:.3f}")
print(f"Upper 99.5th percentile: {q_995:.3f}")
Lower 0.05th percentile: 0.099
Upper 99.5th percentile: 0.260
Alternatively, since the histogram of the sampling distribution looks roughly normal in shape, we can create a 99% confidence interval based on the normal distribution. First, we find the standard error of \( \hat{\theta} \), which is just the standard deviation of the sampling distribution of \(\hat{\theta}\):
standard_error = np.std(boot_theta_hat)
standard_error
0.02653498609330345
Then, a 99% confidence interval for \(\theta^*\) is \(2.58\) SEs away from the observed \(\hat{\theta}\) in either direction:
print(f"Lower 0.05th endpoint: {theta2_hat - (2.58 * standard_error):.3f}")
print(f"Upper 99.5th endpoint: {theta2_hat + (2.58 * standard_error):.3f}")
Lower 0.05th endpoint: 0.138
Upper 99.5th endpoint: 0.275
These two intervals (bootstrap percentile and normal) are close but clearly not identical. We might expect this given the slight asymmetry in the bootstrapped sampling distribution.
There are other versions of the normal-based confidence interval that reflect the variability in estimating the standard error of the sampling distribution using the SD of the data. And there are still other confidence intervals for statistics that are percentiles, rather than averages. (Also note that for permutation tests, the bootstrap tends not to be as accurate as normal approximations.)
Note
Confidence intervals can be easily misinterpreted as the chance that the parameter \(\theta^*\) is in the interval. However, the confidence interval is created from one realization of the sampling distribution. The sampling distribution gives us a different probability statement; 95% of the time, an interval constructed in this way will contain \(\theta^*\). Unfortunately, we don’t know whether this particular time is one of those that happens 95 times in 100 or not. That is why the term confidence is used rather than probability or chance, and we say that we are 95% confident that the parameter is in our interval.
Confidence intervals and hypothesis tests are related in the following way. If, say, a 95% confidence interval contains the hypothesized value \(\theta^*\), then the \(p\)-value for the test is less than 5%. That is, we can invert a confidence interval to create a hypothesis test. We used this technique in the previous section when we carried out the test that the coefficient for humidity in the air quality model is 0. In this section, we have created a 99% confidence interval for the coefficient (based on the bootstrap percentiles), and since 0 does not belong to the interval, the \(p\)-value is less than 1% and statistical logic would lead us to conclude that the coefficient is not 0.
Another kind of interval estimate is the prediction interval. Prediction intervals focus on the variation in observations rather than the variation in an estimator. We explore these next.
