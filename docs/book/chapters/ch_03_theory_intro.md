# 3. Simulation and Data Design

**Nguồn web:** [https://learningds.org/ch/03/theory_intro.html](https://learningds.org/ch/03/theory_intro.html)  
**Nguồn tải:** `web-html` | `ch/03/theory_intro`

---

# 3. Simulation and Data Design#
In this chapter, we develop the basic theoretical foundation needed to reason about how data is sampled and the implications on bias and variance. We build this foundation not on the dry equations of classic statistics but on the story of an urn filled with marbles. We use the computational tools of simulation to reason about the properties of selecting marbles from the urn and what they tell us about data collection in the real world. We connect the simulation process to common statistical distributions (the dry equations), but the basic tools of simulation enable us to go beyond what can be directly modeled using equations.
As an example, we study how the pollsters failed to predict the outcome of the US presidential election in 2016. Our simulation study uses the actual votes cast in Pennsylvania. We simulate the sampling variation for a poll of these six million voters to uncover how response bias can skew polls and see how simply collecting more data would not have helped.
In a second simulation study, we examine a controlled experiment that demonstrated the efficacy of a COVID-19 vaccine but also launched a heated debate on the relative efficacy of vaccines. Abstracting the experiment to an urn model gives us a tool for studying assignment variation in randomized controlled experiments. Through simulation, we find the expected outcome of the clinical trial. Our simulation, along with careful examination of the data scope, debunks claims of vaccine ineffectiveness.
A third example uses simulation to imitate a measurement process. When we compare the fluctuations in our artificial measurements of air quality to real measurements, we can evaluate the appropriateness of the urn to model fluctuations in air quality measurements. This comparison creates the backdrop against which we calibrate PurpleAir monitors so that they can more accurately measure air quality in times of low humidity, like during fire season.
However, before we tackle some of the most significant data debates of our time, we first start small, very small, with the story of a few marbles sitting in an urn.
