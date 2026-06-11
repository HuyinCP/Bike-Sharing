# 1.1. The Stages of the Lifecycle

**Nguồn web:** [https://learningds.org/ch/01/lifecycle_cycle.html](https://learningds.org/ch/01/lifecycle_cycle.html)  
**Nguồn tải:** `web-html` | `ch/01/lifecycle_cycle`

---

# 1.1. The Stages of the Lifecycle#
Figure 1.1 shows the data science lifecycle.
The lifecycle is divided into four stages: Ask a Question, Obtain Data,
Understand the Data, and Understand the World.
We’ve purposefully made these stages broad.
In our experience, the mechanics of the lifecycle change frequently.
Computer scientists and statisticians continue to build new software packages and programming languages
for working with data, and they develop new methodologies that are more specialized.
Despite these changes, we’ve found that almost every data project consists of these four stages:
Fig. 1.1 The four high-level stages of the data science lifecycle.
The arrows indicate how the stages can lead into one another.#
Ask a Question
Asking good questions is at the heart of data science, and recognizing
different kinds of questions guides us in our analyses.
We cover four categories of questions:
descriptive, exploratory, inferential, and predictive.
For example, “How have house prices changed over time?” is descriptive in nature, whereas
“Which aspects of houses are related to sale price?” is exploratory.
Narrowing down a broad question into one that can be answered with data is a key element of this first stage in the lifecycle. It can involve consulting the people participating in a study, figuring out how to measure something, and designing data collection protocols.
A clear and focused research question helps us determine the data we need,
the patterns to look for, and how to interpret results. It can also help us refine our question, recognize the type of question being asked, and plan the data collection phase of the lifecycle.
Obtain Data
When data are expensive and hard to gather and when our goal is to generalize from the data to the world, we aim to define precise protocols for collecting the data. Other times, data are cheap and easily accessed.
This is especially true for online data sources.
For example, Twitter lets people quickly download millions of data points.
When data are plentiful, we can start an analysis by obtaining and exploring the data, and then honing a research question.
In both situations, most data have missing or unusual values and other anomalies that we need to account for. No matter the source, we need to check the data quality. Considering the scope of the data is equally important; for example, we identify how representative the data are and look for potential sources of bias in the collection process. These considerations help us determine how much faith we can place in our findings. And, typically, we must manipulate the data before we can analyze it more formally. We may need to modify structure, clean data values, and transform measurements to prepare for analysis.
Understand the Data
After obtaining and preparing data, we want to carefully examine them, and exploratory data analysis is often key. In our explorations, we make plots to uncover interesting patterns and summarize the data visually. We also continue to look for problems with the data.
As we search for patterns and trends, we use summary statistics and build statistical models, like linear and logistic regression.
In our experience, this stage of the lifecycle is highly iterative.
Understanding the data can also lead us back to earlier stages in the data science lifecycle. We may find that we need to modify or redo the data cleaning and manipulation, acquire more data to supplement our analysis, or refine our research question given the limitations of the data. The descriptive and exploratory analyses that we carry out in this stage may adequately answer our question, or we may need to go on to the next stage in order to make generalizations beyond our data.
Understand the World
When our goals are purely descriptive or exploratory, the analysis ends at the Understand the Data stage of the lifecycle.
At other times, we aim to quantify how well the trends we find generalize beyond our data.
We may want to use a model that we have fit to our data to make inferences about the world or give predictions for future observations.
To draw inferences from a sample to a population, we use
statistical techniques like A/B testing and confidence intervals.
And to make predictions for future observations, we create prediction intervals and use train-test splits of the data.
Note
Understanding the differences between exploration, inference, prediction, and causation can be a challenge.
We can easily slip into confusing a correlation found in data with a causal relationship.
For example, an exploratory or inferential analysis might look for correlations in response to the question “Do people who have a greater exposure to air pollution have a higher rate of lung disease?” Whereas a causal question might ask “Does giving an award to a Wikipedia contributor increase productivity?” We typically cannot answer causal questions unless we have a randomized experiment (or approximate one). We point out these important distinctions throughout the book.
For each stage of the lifecycle, we explain theoretical concepts, introduce data technologies and statistical methodologies, and show how they work in practical examples.
Throughout, we rely on authentic data and analyses by other data scientists, not made-up data, so you can learn how to perform your own data acquisition, cleaning, exploration, and formal analyses, and draw sound conclusions. Each chapter in this book tends to focus on one stage of the data science lifecycle, but we also include chapters with case studies that demonstrate the full lifecycle.
