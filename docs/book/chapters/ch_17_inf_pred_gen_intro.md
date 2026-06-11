# 17. Theory for Inference and Prediction

**Nguồn web:** [https://learningds.org/ch/17/inf_pred_gen_intro.html](https://learningds.org/ch/17/inf_pred_gen_intro.html)  
**Nguồn tải:** `web-html` | `ch/17/inf_pred_gen_intro`

---

# 17. Theory for Inference and Prediction#
When you want to generalize your findings beyond descriptions for your collection of data to a larger setting, the data needs to be representative of that larger world. For example, you may want to predict air quality at a future time based on a sensor reading (Chapter 12); test whether an incentive improves the productivity of contributors based on experimental findings (Chapter 3); or construct an interval estimate for the amount of time you might spend waiting for a bus (Chapter 5). We touched on all of these scenarios in earlier chapters. In this chapter, we’ll formalize the framework for making predictions and inferences.
At the core of this framework is the notion of a distribution, be it a population, empirical (aka sample), or probability distribution. Understanding the connections between these distributions is central to the basics of hypothesis testing, confidence intervals, prediction bands, and risk. We begin with a brief review of the urn model, introduced in Chapter 3; then we introduce formal definitions of hypothesis tests, confidence intervals, and prediction bands. We use simulation in our examples, including the bootstrap as a special case. We wrap up the chapter with formal definitions of expectation, variance, and standard error—essential concepts in the theory of testing, inference, and prediction.
