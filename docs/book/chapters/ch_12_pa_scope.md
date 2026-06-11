# 12.1. Question, Design, and Scope

**Nguồn web:** [https://learningds.org/ch/12/pa_scope.html](https://learningds.org/ch/12/pa_scope.html)  
**Nguồn tải:** `web-html` | `ch/12/pa_scope`

---

# 12.1. Question, Design, and Scope#
Ideally, measures of air quality should be both accurate and timely.
Inaccurate or biased measurements can mean people do not take air condition as seriously as they should.
Delayed alerts can expose people to harmful air. The context provided in the introduction about the popularity of inexpensive air quality sensors got us wondering about their quality and usefulness.
Two different kinds of instruments measure a natural phenomenon—the amount of particulate matter in the air. The AQS sensor has the advantage of small measurement error and negligible bias (see Chapter 2). On the other hand, the PurpleAir instrument is less accurate; the measurements have greater variability and are also biased.  Our inital question is: can we use the AQS measurements to make the PurpleAir measurements better?
We are in the situation where we have a lot of data available to us. We have access to a small number of high-quality measurements from AQS, and we can get data from thousands of PurpleAir sensors. To narrow the focus of our question, we consider how we might use these two sources of data to improve PurpleAir measurements.
The data from these two sources includes the locations of the sensors. So we can try to pair them up, finding a PurpleAir sensor close to each AQS sensor. If they’re close, then these sensors are essentially measuring the same air.
We can treat the AQS sensors as the ground truth (because they are so accurate) and study the variation in the PurpleAir measurements given the true air quality.
Even though there are relatively few pairs of collocated AQS and PurpleAir sensors, it seems reasonable to generalize any relationship we find to other PurpleAir sensors.
If there’s a simple relationship between AQS and PurpleAir measurements, then we can use this relationship to adjust measurements from any PurpleAir sensor so that they are more accurate.
We have narrowed down our question quite a bit: can we model the relationship between
PurpleAir sensor readings and neighboring AQS sensor readings?
If yes, then hopefully we can use the model to improve PurpleAir readings. Spoiler alert: indeed we can!
This case study nicely integrates the concepts introduced in this part of the book.
It gives us an opportunity to see how data scientists wrangle, explore, and visualize data in a real-world setting. In particular, we see how a large, less-accurate dataset can amplify the usefulness of a small, accurate dataset.
Combining large and small datasets like this is particularly exciting to data scientists and applies broadly to other domains ranging from social science to medicine.
In the next section, we begin our wrangling by finding the pairs of AQS and PurpleAir sensors that are near each other.  We focus specifically on readings for PM2.5 particles, which are particles that are smaller than 2.5 micrometers in diameter.
These particles are small enough to be inhaled into the lungs, pose the greatest
risk to health, and are especially common in wood smoke.
