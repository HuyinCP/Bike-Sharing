# 18.5. Summary

**Nguồn web:** [https://learningds.org/ch/18/donkey_summary.html](https://learningds.org/ch/18/donkey_summary.html)  
**Nguồn tải:** `web-html` | `ch/18/donkey_summary`

---

# 18.5. Summary#
In this case study, we demonstrated the different purposes of modeling: description, inference, and prediction. For description, we sought a simple, understandable model. We handcrafted this model, beginning with our findings from the exploratory phase of the analysis. Every action we took to include a feature in the model, collapse categories, or transform a feature amounts to a decision we made while investigating the data.
In modeling a natural phenomenon such as the weight of a donkey, we would ideally make use of physical and statistical models. In this case, the physical model is the representation of a donkey by a cylinder.
An inquisitive reader might have pointed out that we could have used this representation directly to estimate the weight of a donkey (cylinder) from its length and girth (since girth is \(2\pi r\)):
\[ weight \propto girth^2 \times length\]
This physical model suggests that the log-transformed weight is approximately linear in girth  and length:
\[ \log(weight) \propto 2\log(girth) +  \log(length)\]
Given this physical model, you might wonder why we did not use logarithmic or square transformations in fitting our model. We leave you to investigate such a model in greater detail. But generally, if the range of values measured is small, then the log function is roughly linear. To keep our model simple, we chose not to make these transformations given the strength of the statistical model seen by the high correlation between girth and weight.
We did a lot of data dredging in this modeling exercise. We examined all possible models built from linear combinations of the numeric features, and we examined coefficients of dummy variables to decide whether to collapse categories.
When we create models using an iterative approach like this,
it is extremely important that we set aside data to assess the model.
Evaluating the model on new data reassures us that the model we chose works well.
The data that we set aside did not enter into any decision making when building the model, so it gives us a good sense of how well the model works for making predictions.
We should keep the data scope and its potential biases described earlier in mind. Our model has done well on the test set, but the test and train sets come from the same data collection process. We expect our model to work well in practice as long as the scope remains the same for new data.
Finally, this case study shows how fitting models is often a balance between
simplicity and complexity and between physical and statistical
models. A physical model can be a good starting point in modeling, and a
statistical model can inform a physical model. As data scientists, we needed to
make judgment calls at each step in the analysis. Modeling is both an art and a
science.
This case study and several chapters preceding it have focused on fitting linear models. Next, we consider a different kind of modeling for the situation when the response variable we are explaining or predicting is qualitative, not quantitative.
