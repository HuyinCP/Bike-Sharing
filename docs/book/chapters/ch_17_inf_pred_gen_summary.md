# 17.7. Summary

**Nguồn web:** [https://learningds.org/ch/17/inf_pred_gen_summary.html](https://learningds.org/ch/17/inf_pred_gen_summary.html)  
**Nguồn tải:** `web-html` | `ch/17/inf_pred_gen_summary`

---

# 17.7. Summary#
Throughout this chapter, we based our development of the theory behind inference and prediction on the urn model. The urn induced a probability distribution on the estimator, such as the sample mean and the least squares regression coefficients. We end this chapter with some cautions about these statistical procedures.
We saw how the SD of an estimator has a factor of the square root of the sample size in the denominator. When samples are large, the SD can be quite small and can lead to rejecting a hypothesis or very narrow confidence intervals. When this happens it’s good to consider the following:
-
Is the difference that you have detected an important difference? That is, a \(p\)-value may be quite small, indicating a surprising result, but the actual effect observed may be unimportant. Statistical significance does not imply practical significance.
-
Keep in mind that these calculations do not incorporate bias, such as non-response bias and measurement bias. The bias might well be larger than any difference due to chance variation in the sampling distribution.
At times, we know the sample is not from a chance mechanism, but it can still be useful to carry out a hypothesis test. In this case, the null model would test whether the sample (and estimator) are as if they were at random. When this test is rejected, we confirm that something nonrandom has led to the observed data. This can be a useful conclusion: that the difference between what we expect and what we observed is not explained by chance.
At other times, the sample consists of the complete population. When this happens, we might not need to make confidence intervals or hypothesis tests because we have observed all values in the population. That is, inference is not required.
However, we can instead place a different interpretation on hypothesis tests: we can suppose that any relation observed between two features was randomly distributed without relation to each other.
We also saw how the bootstrap can be used when we don’t have enough information about the population. The bootstrap is a powerful technique, but it does have limitations:
-
Make sure that the original sample is large and random so that the sample resembles the population.
-
Repeat the bootstrap process many times. Typically 10,000 replications is a reasonable number.
-
The bootstrap tends to have difficulties when:
The estimator is influenced by outliers.
-
The parameter is based on extreme values of the distribution.
-
The sampling distribution of the statistic is far from bell shaped.
Alternatively, we rely on the sampling distribution being approximately normal in shape. At times, the sampling distribution looks roughly normal but has thicker tails. In these situations, the family of \(t\)-distributions might be appropriate to use instead of the normal.
A model is usually only an approximation of underlying reality, and the precision of the statement that \(\theta^*\) exactly equals 0 is at odds with this notion of a model.
The inference depends on the correctness of our model. We can partially check the model assumptions, but some amount of doubt goes with any model. In fact, it often happens that the data suggest more than one possible model, and these models may even be contradictory.
Lastly, at times, the number of hypothesis tests or confidence intervals can be
quite large, and we need to exercise caution to avoid spurious results. This problem is called \(p\)-hacking and is another example of the reproducibility crisis in science described in Chapter 10.  \(P\)-hacking is based on the notion that if we test, say, 100 hypotheses, all of which are true, then we would expect to get a few surprise results and reject a few of these hypotheses. This phenomenon can happen in multiple linear regression when we have a large number of features in a model, and techniques have been developed to limit the dangers of these false discoveries.
We next recap the modeling process with a case study.
