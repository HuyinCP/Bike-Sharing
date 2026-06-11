# Modeling Summary

**Nguồn web:** [https://learningds.org/ch/04/modeling_summary.html](https://learningds.org/ch/04/modeling_summary.html)  
**Nguồn tải:** `github-ipynb` | `ch/04/modeling_summary.ipynb`

---

(sec:modeling_summary)=
# Summary

We introduced the constant model: a model that
summarizes the data by a single value. To fit the constant model, we chose
a loss function that measured how well a given constant fits a data value, and
we computed the average loss over all of the data values. We saw that depending
on the choice of loss function, we get a different minimizing value:
we found that the mean minimizes the average squared error (MSE), and the median
minimizes the average absolute error (MAE). We also discussed how we can
incorporate context and knowledge of our problem to pick a loss function.

The idea of fitting models through loss minimization ties simple summary
statistics---like the mean, median, and mode---to more complex modeling
situations. The steps we took to model our data apply to many modeling
scenarios:

1. Select the form of a model (such as the constant model).
2. Select a loss function (such as absolute error).
3. Fit the model by minimizing the loss over all the data (such as average loss).

For the rest of this book, our modeling techniques expand upon one or
more of these steps. We introduce new models, new loss functions, and
new techniques for minimizing loss.

The next chapter revisits the study of a bus arriving late at its stop. This time, we present the problem as a case study and visit all stages of the data science lifecycle. By going through these stages, we make some unusual discoveries; when we augment our analysis by considering data scope and using an urn to simulate a rider arriving at the bus stop, we find that modeling bus lateness is not the same as modeling the rider's experience waiting for a bus.
