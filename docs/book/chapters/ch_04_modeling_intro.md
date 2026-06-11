# 4. Modeling with Summary Statistics

**Nguồn web:** [https://learningds.org/ch/04/modeling_intro.html](https://learningds.org/ch/04/modeling_intro.html)  
**Nguồn tải:** `web-html` | `ch/04/modeling_intro`

---

# 4. Modeling with Summary Statistics#
We saw in Chapter 2  the importance of data scope and in Chapter 3 the importance of data generation mechanisms, such as one that can be represented by an urn model.  Urn models address one aspect of modeling: they describe chance variation and ensure that the data are representative of the target. Good scope and representative data lay the groundwork for extracting useful information from data, which is the other part of modeling.  This information is often referred to as the signal in the data. We use models to approximate the signal, with the simplest of these being the constant model, where the signal is approximated by a single number, like the mean or median. Other, more complex models summarize relationships between features in the data, such as humidity and particulate matter in air quality (Chapter 12), upward mobility and commute time in communities (Chapter 15), and height and weight of animals (Chapter 18). These more complex models are also approximations built from data.
When a model fits the data well, it can provide a useful approximation to the world or simply a helpful description of the data.
In this chapter, we introduce the basics of model fitting through a loss formulation. We demonstrate how to model patterns in the data by considering the loss that arises from using a simple summary to describe the data, the constant model.
We delve deeper into the connections between the urn model and the fitted model in Chapter 16, where we examine the balance between signal and noise when fitting models, and in Chapter 17, where we tackle the topics of inference, prediction, and hypothesis testing.
The constant model lets us introduce model fitting from the perspective of
loss minimization in a simple context, and it helps us connect summary statistics, like the mean and median, to more complex modeling scenarios in later chapters. We begin with an example that uses data about the late arrival of a bus to introduce the constant model.
