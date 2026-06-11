# 15. Linear Models

**Nguồn web:** [https://learningds.org/ch/15/linear_intro.html](https://learningds.org/ch/15/linear_intro.html)  
**Nguồn tải:** `web-html` | `ch/15/linear_intro`

---

# 15. Linear Models#
At this point in the book,
we’ve covered the four stages of the data science lifecycle to different extents.
We’ve talked about formulating questions and obtaining and cleaning data, and we’ve used exploratory data analysis to better understand the data. In this chapter, we extend the constant model introduced in Chapter 4 to the linear model. Linear models are a popular tool in the last stage of the lifecycle: understanding the world.
Knowing how to fit linear models opens the door to all kinds of useful data analyses.
We can use these models to make predictions—for example,
environmental scientists developed a linear model to predict air quality based on air sensor measurements and weather conditions (see Chapter 12).
In that case study, understanding how measurements from two instruments varied
enabled us to calibrate inexpensive sensors and improve their air quality readings.
We can also use these models to make inferences about the form of a relationship between features—for example,
veterinarians used a linear model (see Chapter 18) to infer the coefficients for length and girth for a donkey’s weight: \( Length ~+ ~ 2 \times Girth ~-~175 \).
In that case study, the model enables vets working in the field to prescribe medication for sick donkeys.
Models can also help describe relationships and provide insights—for example, in this chapter, we explore relationships between factors correlated with upward mobility, such as commute time, income inequality, and the quality of K–12 education. We carry out a descriptive analysis that follows an analysis social scientists have used to shape public conversation and inform policy recommendations.
We start by describing the simple linear model, which
summarizes the relationship between two features with a line.
We explain how to fit this line to data using the loss minimization approach introduced in Chapter 4.
Then we introduce the multiple linear model, which models one feature using multiple, other features.
To fit such a model, we use linear algebra and reveal the geometry behind fitting a linear model with squared error loss.
Finally, we cover feature engineering techniques that let us include categorical features and transformed features when building models.
