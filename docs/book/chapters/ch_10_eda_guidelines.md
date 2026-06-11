# 10.5. Guidelines for Exploration

**Nguồn web:** [https://learningds.org/ch/10/eda_guidelines.html](https://learningds.org/ch/10/eda_guidelines.html)  
**Nguồn tải:** `web-html` | `ch/10/eda_guidelines`

---

# 10.5. Guidelines for Exploration#
So far in this chapter, we have introduced the notion of feature types;
seen how the feature type can help to figure out what plot to make; and
described how to read distributions and relationships in a visualization.
EDA relies on building these skills and flexibly developing your understanding of the data.
You saw EDA in action in Chapter 9 when we developed checks for data quality and feature
transformations to improve their usefulness in data analysis. Following are questions to guide you when making plots to explore the data:
-
How are the values of Feature X distributed?
-
How do Feature X and Feature Y relate to each other?
-
Is the distribution of Feature X the same across subgroups defined by Feature Z?
-
Are there any unusual observations in X? In the combination of (X,Y)? In X
for a subgroup of Z?
As you answer each of these questions, it is important to tie your answer
back to the features measured and the context. It is also important to adopt an active,
inquisitive approach to the investigation. To guide your
explorations, ask yourself “what next” and “so what” questions, such as the
following:
-
Do you have reason to expect that one group/observation might be different?
-
Why might your finding about shape matter?
-
What additional comparison might bring added value to the investigation?
-
Are there any potentially important features to create comparisons
with/against?
In this process, it’s important to step away from the computer at times to mull over your findings. You may want to read additional literature on the subject or go to an expert in the field to discuss your findings. For example, there could be good reasons for an unusual observation and someone in the field can help clear up and provide more background.
We put these guidelines into practice with a concrete example of EDA next.
