# 12.6. Creating a Model to Correct PurpleAir Measurements

**Nguồn web:** [https://learningds.org/ch/12/pa_modeling.html](https://learningds.org/ch/12/pa_modeling.html)  
**Nguồn tải:** `web-html` | `ch/12/pa_modeling`

---

# 12.6. Creating a Model to Correct PurpleAir Measurements#
Now that we’ve explored the relationship between PM2.5 readings from AQS and PurpleAir sensors,
we’re ready for the final step of the analysis: creating a model that corrects PurpleAir measurements.
Barkjohn’s original analysis fits many models to the data in order to find the most appropriate one.
In this section, we fit a simple linear model using the techniques from Chapter 4.
We also briefly describe the final model Barkjohn chose for real-world use.
Since these models use methods that we introduce later in the book,
we won’t explain the technical details very deeply here. Instead, we encourage you to revisit this section after reading Chapter 15.
First, let’s go over our modeling goals.
We want to create a model that predicts PM2.5 as accurately as possible.
To do this, we build a model that adjusts PurpleAir measurements based on AQS measurements.
We treat the AQS measurements as the true PM2.5 values because
they are taken from carefully calibrated instruments and are
actively used by the US government for decision making. So we have reason to
trust the AQS PM2.5 values as being precise and close to the truth.
After we build the model that adjusts the PurpleAir measurements using AQS, we then flip the model around and use it to predict the true air quality in the future from PurpleAir measurements when we don’t have a nearby AQS instrument.
This is a calibration scenario.
Since the AQS measurements are close to the truth, we fit the more variable PurpleAir measurements to them;
this is the calibration procedure.
Then we use the calibration curve to correct future PurpleAir measurements.
This two-step process is encapsulated in the upcoming simple linear model and its flipped form.
First, we fit a line to predict a PA measurement from the ground truth, as recorded by an AQS instrument:
\[ \text{PA} \approx b + m\text{AQS} \]
Next, we flip the line around to use a PA measurement to predict the air quality:
\[ \text{True Air Quality} \approx -b/m + 1/m \text{PA} \]
The scatter plot and histograms that we made during our exploratory data analysis suggest that
the PurpleAir measurements are more variable, which supports the calibration approach.
And we saw that the PurpleAir measurements are about twice as high as the AQS measurements,
which suggests that \( m \) may be close to 2 and \(1/m\) close to \( 1/2 \).
Why Two Steps?
This calibration procedure might seem a bit roundabout.
Why not fit a linear model that directly uses PurpleAir to predict AQS?
That seems a lot easier, and we wouldn’t need to invert anything.
Since AQS measurements are “true” (or close to it), they have no error.
Intuitively, a linear model works conditionally on the value of the variable on the x-axis,
and minimizes the error in the \( y \) direction: \( y-(b + mx) \).
So we place the accurate measurements on the x-axis to fit the line, called the calibration curve.
Then, in the future, we invert the line to
predict the truth from our instrument’s measurement. That’s why this process is also called inverse regression.
Calibration is a reasonable thing to do only when the pairs of measurements are highly correlated.
As a simpler example, let’s say we want to calibrate a scale.
We could do this by placing known weights—say, 1 kg, 5 kg,
and 10 kg—onto the scale and seeing what the scale reports.
We typically repeat this a few times, each time getting slightly different measurements from the scale.
If we discover that our scale is often 10% too high (\(y=1.1x\)), then when we weigh something in the future, we adjust our scale’s reading downward by 90% (\(1/1.1 = 0.9\)). Analogously, the AQS measurements are the known quantities, and our model checks
what the PurpleAir sensor reports.
Now let’s fit the model. Following the notion from Chapter 4, we choose a loss function and minimize the average error. Recall that a loss function measures how far away our model is from the actual data. We use squared loss, which in this case is \( [PA - (b+mAQS)]^2 \). And to fit the model to our data, we minimize the average squared loss over our data:
\[
\begin{aligned}
\frac{1}{n} \sum_{i = 1}^{n} [PA_i - (b + mAQS_i]^2
\end{aligned}
\]
We use the linear modeling functionality provided by scikit-learn to do this. (Again, don’t worry about these details for now.)
from sklearn.linear_model import LinearRegression
AQS, PA = full_df[['pm25aqs']], full_df['pm25pa']
model = LinearRegression().fit(AQS, PA)
m, b = model.coef_[0], model.intercept_
By inverting the line, we get the estimate:
print(f"True Air Quality Estimate = {-b/m:.2} + {1/m:.2}PA")
True Air Quality Estimate = 1.4 + 0.53PA
This is close to what we expected. The adjustment to PurpleAir measurements is about \( 1/2 \).
The model that Barkjohn settled on incorporated the relative humidity:
\[
\begin{aligned}
\text{PA} \approx b + m_1 \text{AQS} + m_2 \text{RH}
\end{aligned}
\]
This is an example of a multivariable linear regression model—it uses
more than one variable to make predictions. We can fit it by minimizing the average squared error over the data:
\[
\begin{aligned}
\frac{1}{n} \sum_{i = 1}^{n} [PA_i - (b + m_1AQS_i + m_2 RH_i]^2
\end{aligned}
\]
Then we invert the calibration to find the prediction model using the following equation:
\[
\begin{aligned}
\text{True Air Quality} &\approx - \frac{b}{m_1} + \frac{1}{m_1} \text{PA}
- \frac{m_2}{m_1} \text{RH}
\end{aligned}
\]
We fit this model and check the coefficients:
AQS_RH, PA = full_df[['pm25aqs', 'rh']], full_df['pm25pa']
model_h = LinearRegression().fit(AQS_RH, PA)
[m1, m2], b = model_h.coef_, model_h.intercept_
print(f"True Air Quality Estimate = {-b/m:1.2} + {1/m1:.2}PA + {-m2/m1:.2}RH")
True Air Quality Estimate = 5.7 + 0.53PA + -0.088RH
In Chapters 15 and 16, we will learn how to compare these two models by examining things like the size of and patterns in prediction error. For now, we note that the model that incorporates relative humidity performs the best.
